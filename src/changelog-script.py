from os.path import isdir, realpath
import argparse
import os
import json
from string import Template

import logging

logger = logging.getLogger("FCC")


class WritableDirectoryAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values

        if not isdir(prospective_dir):
            os.mkdir(prospective_dir)

        if os.access(prospective_dir, os.W_OK):
            setattr(namespace, self.dest, realpath(prospective_dir))
            return

        raise argparse.ArgumentTypeError(
            "%s is not a writeable directory" % (prospective_dir,)
        )


format_templates = {
    "md": {
        "message": "Generating Markdown Changelog",
        "separator": "\n---\n",
        "version": Template("\n## $version\n"),
        "category": Template("\n### $category\n\n"),
        "change": Template("- $change$more$by\n"),
        "url": Template("[$text]($target)"),
    },
    "ingame": {
        "message": "Generating In-game Changelog",
        "separator": "---------------------------------------------------------------------------------------------------\n",
        "version": Template("Version: $version\n"),
        "date": Template("Date: $date\n"),
        "category": Template("\n  $category\n"),
        "change": Template("    - $change$more$by\n"),
        "more_url": Template("$target"),
        "by_url": Template("$text"),
    },
    "forum": {
        "message": "Generating Factorio Forum Changelog",
        "version": Template("[size=150][b]$version[/b][/size]\n"),
        "category": Template("\n[b]$category[/b]\n"),
        "list_start": "[list]\n",
        "list_end": "[/list]\n",
        "change": Template("[*] $change$more$by\n"),
        "url": Template("[url=$target]$text[/url]"),
    },
}

format_filenames = {
    "md": "Changelog.md",
    "ingame": "changelog.txt",
    "forum": "changelog_forum.txt",
}

change_defaults = {"more": "", "by": ""}


def entries_formatter(template, entries, entries_type):
    entries_output = " more: " if entries_type == "more" else " by "
    if not isinstance(entries, list):
        entries = [entries]
    for i, entry in enumerate(entries):
        if i:
            entries_output += ", "
        if isinstance(entry, dict):
            text = next(iter(entry))
            if "url" in template:
                entries_output += template["url"].substitute(
                    text=text, target=entry[text]
                )
            else:
                entries_output += template[f"{entries_type}_url"].substitute(
                    text=text, target=entry[text]
                )
        else:
            entries_output += entry
    return entries_output


def change_formater(template, changes):
    changes_output = template["list_start"] if "list_start" in template else ""
    for change in changes:
        if isinstance(change, dict):
            more_text = (
                entries_formatter(template, change["more"], "more")
                if "more" in change
                else ""
            )
            by_text = (
                entries_formatter(template, change["by"], "by")
                if "by" in change
                else ""
            )
            changes_output += template["change"].substitute(
                change=change["change"], more=more_text, by=by_text
            )
        else:
            changes_output += template["change"].substitute(
                change_defaults, change=change
            )
    changes_output += template["list_end"] if "list_end" in template else ""
    return changes_output


def version_formatter(template, version, data):
    version_output = ""
    if "separator" in template:
        version_output += template["separator"]
    version_output += template["version"].substitute(version=version)
    if "date" in template and "date" in data:
        version_output += template["date"].substitute(date=data["date"])
    if "Categories" in data:
        for category, category_data in data["Categories"].items():
            version_output += template["category"].substitute(category=category)
            version_output += change_formater(template, category_data)
    if "Changes" in data:
        version_output += template["category"].substitute(category="Other")
        version_output += change_formater(template, data["Changes"])
    return version_output


def create_changelog(args):
    changelog = json.load(args.input_file)

    for output_format in args.formats:
        format_template = format_templates[output_format]
        logger.info(format_template["message"])
        with open(
            os.path.join(args.output_dir, format_filenames[output_format]),
            "w",
            encoding="utf-8",
        ) as output_file:
        for version, data in changelog.items():
                output_file.write(version_formatter(format_template, version, data))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")
    parser = argparse.ArgumentParser(description="Factorio changelog generator")
    parser.add_argument(
        "output_dir",
        nargs="?",
        help="Directory where the files will be written",
        default=".",
        action=WritableDirectoryAction,
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        help="JSON file to parse for changes",
        default="changelog.json",
        type=argparse.FileType("r"),
    )
    parser.add_argument(
        "-f",
        "--formats",
        help="Which format[s] should be generated",
        default=["md", "ingame"],
        choices=["md", "ingame", "forum"],
        nargs="+",
    )
    parser.add_argument("-v", "--verbose", help="Output verbosity", action="count")
    args = parser.parse_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    create_changelog(args)
