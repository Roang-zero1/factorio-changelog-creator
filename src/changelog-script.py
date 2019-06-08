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
    },
    "ingame": {
        "message": "Generating In-game Changelog",
        "separator": "---------------------------------------------------------------------------------------------------\n",
        "version": Template("Version: $version\n"),
        "date": Template("Date: $date\n"),
    },
    "forum": {
        "message": "Generating Factorio Forum Changelog",
        "version": Template("\n[size=150][b]$version[/b][/size]\n"),
    },
}


def format_version(template, version, data):
  version_output = ""
    if "separator" in template:
        version_output += template["separator"]
    version_output += template["version"].substitute(version=version)
    if "date" in template and "date" in data:
        version_output += template["date"].substitute(date=data["date"])
  return version_output


def create_changelog(args):
  changelog = json.load(args.input_file)

  for output_format in args.formats:
    format_template = format_templates[output_format]
    logger.info(format_template["message"])
    for version, data in changelog.items():
      print(format_version(format_template, version, data))


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
