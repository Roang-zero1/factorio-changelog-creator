# Changelog Script #
This is a quick and dirty lua script for generating changelog for Factorio mods in various formats.

# Usage #
Run the script from the command line. If no parameters are given, it will look for a file named `changelog.lua` in the
directory it was called from and it will output into the same directory.  
The possible parameters are:
- `changelog-path`: This is the path to read the changelog from. It has to be a Lua file in the format outlined bellow.
- `out-path`: This is a path to a directory that the outputs will be stored in. If it doesn't exist, it will be created.

Note that due to Lua being weird, the directory is created using `mkdir`, so don't be surprised if it tells you
something, it's probably correct.

After the command finishes, three files will be created in the output directory, each being the changelog in a different
format.
- `changelog_forum.txt`: The syntax forums.factorio.com uses
- `changelog.md`: A markdown syntax that should work both on mods.factorio.com and GitHub
- `changelog.txt`: The syntax the game uses - this is what should be left in the mod

# Format #
The changelog definition file should return a table containing tables representing the individual versions.

The format of the inner tables is this:
```
{
	name = "0.1.0", -- Mandatory
	date = "16. 12. 2017", -- Optional, can be anything
	
	"Change in the default category", -- Changes declared directly in this table will be put into the 'Other' category
	-- ...
	
	Category = { -- Categories are defined using their name, any name can be used, except name and date
		"Change in category",
	},
	-- ...
}
```

Changes can be declared as simple strings, or as a table in the following format:
```
{
	"Change description", -- Mandatory
	more = "https://link.to.nowhere.com", -- Optional
	by = "Name", -- Optional
}
```
`more` and `by` work in the same way, but have different meanings: `more` is a link with more information and `by` is
the author of the change.  
They can be either a string that will be used directly, or a table of such strings, which will then be put into a
comma-separated list. The table can also define these strings on string keys. In this case the key will be used as the
text and the value as the link target. If this is not possible `more` will use the value and `by` will use the key.

# Notes #
If the Other category is the only one and categories are not necessary for the target format, the changes will be put
in a list with no mention of a category.
