# Factorio Changelog Creator

This is a quick and dirty python script for generating changelog for Factorio mods in various formats.

## Quick install

Install latest version from PYPI

```code:: bash
pip install factorio-changelog-creator
```

Install the current dev version from _GitHub_

```code:: bash
pip install git+https://github.com/Roang-zero1/factorio-changelog-creator.git
```

## Usage

Get the script file and put it somewhere on your computer.

Run the script from the command line using `factorio-changelog-creator`. If no parameters are given, it will look for a file named `changelog.json` in the directory it was called from and it will output into the same directory.

There is a command line help available, which can be outputted with `factorio-changelog-creator -h`.

```text
usage: factorio-changelog-creator [-h]
                                  [-f {md,ingame,forum} [{md,ingame,forum} ...]]
                                  [-v]
                                  [output_dir] [input_file]

Factorio changelog generator

positional arguments:
  output_dir            Directory where the files will be written
  input_file            JSON file to parse for changes

optional arguments:
  -h, --help            show this help message and exit
  -f {md,ingame,forum} [{md,ingame,forum} ...], --formats {md,ingame,forum} [{md,ingame,forum} ...]
                        Which format[s] should be generated
  -v, --verbose         Output verbosity
```

By default the markdown and in-game changelog will be generated. The forum changelog can be generated with `python3 changelog-script.py -f forum`.

- `changelog_forum.txt`: The syntax forums.factorio.com uses
- `CHANGELOG.md`: A markdown syntax that should work both on mods.factorio.com and GitHub
- `changelog.txt`: The syntax the game uses - this is what should be left in the mod

## Format

The changelog definition file should be a JSON file containing a dictionary of version dictionaries.

The format of the dictionary is this:

```json
{
  "0.1.0": {
    "date": "2019-06-08", -- Optional, can be anything

    "Changes": ["Change without category"], --Changes will be put in the Other Category

    "Categories": { -- Categories may be any string
      "Features": ["Change in category"]
    }
  }
}
```

Changes can be declared as simple strings, or as a table in the following format:

```json
{
  "change": "Change description", -- Mandatory
  "more": "https://link.to.nowhere.com", -- Optional
  "by": "Name", -- Optional
}
```

`more` and `by` work in the same way, but have different meanings: `more` is a link with more information and `by` is
the author of the change.
They can be either a single entry or a list of entries, the list will be outputted comma-separated.
Each entry may either be a plain string that will be directly used or a dictionary with a single entry in the format:

```json
{
  "url_text": "url_target"
}
```

Depending on the format either a link will be generated of if this in not possible `more` will use the `url_target` value and `by` will use the `url_text`.

## Acknowledgement

Initial Lua implementation by theRustyKnife/factorio-changelog-script
