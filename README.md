# Changelog Script #
This is a quick and dirty lua script for generating changelog for Factorio mods in various formats.

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
