from os.path import isdir, realpath
import argparse
import os
import json


class WritableDirectoryAction(argparse.Action):
  def __call__(self, parser, namespace, values, option_string=None):
    prospective_dir = values

    if not isdir(prospective_dir):
      os.mkdir(prospective_dir)

    if os.access(prospective_dir, os.W_OK):
      setattr(namespace, self.dest, realpath(prospective_dir))
      return

    raise argparse.ArgumentTypeError('%s is not a writeable directory' % (
        prospective_dir,
    ))


def format_markdown(input):
  print("Markdown")


def format_ingame(input):
  print("ingame")


def format_forum(input):
  print("forum")


def create_changelog(args):
  changelog = json.load(args.input_file)
  print(changelog)
  formaters = {
      'md': format_markdown,
      'ingame': format_ingame,
      'forum': format_forum
  }
  for output_format in args.formats:
    formaters[output_format](changelog)


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Factorio changelog generator")
  parser.add_argument(
      "output_dir",
      nargs='?',
      help="Directory where the files will be written",
      default=".",
      action=WritableDirectoryAction
  )
  parser.add_argument(
      "input_file",
      nargs='?',
      help="JSON file to parse for changes",
      default="changelog.json",
      type=argparse.FileType('r')
  )
  parser.add_argument(
      "-f",
      "--formats",
      help="Which format[s] should be generated",
      default=['md', 'ingame'],
      choices=['md', 'ingame', 'forum'],
      nargs='+'
  )
  args = parser.parse_args()
  create_changelog(args)
