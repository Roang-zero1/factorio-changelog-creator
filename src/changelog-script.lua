local _M = {}


local DEFAULT_CATEGORY = "Other"


local function dirname(path) return path:gmatch('.*[/\\]')() or './'; end

local function normalize_more(value)
	if type(value) == 'string' then
		return {{
			text = value,
			target = value,
		}}
		
	elseif type(value) == 'table' then
		local res = {}
		for k, v in pairs(value) do
			if type(k) == 'number' then
				k = v
			end
			table.insert(res, {
				text = k,
				target = v,
			})
		end
		return res
	end
end

local function normalize_change(value)
	if type(value) == 'string' then
		return {description = value}
		
	elseif type(value) == 'table' then
		return {
			description = value[1],
			more = value.more and normalize_more(value.more),
			by = value.by and normalize_more(value.by),
		}
	end
end

local ignored_fields = {name = true, date = true}
local function normalize(version)
	local res = {
		name = version.name,
		date = version.date,
		changes = {},
	}
	
	for k, v in pairs(version) do
		if ignored_fields[k] then -- Skip these
		elseif type(k) == 'number' then
			res.changes[DEFAULT_CATEGORY] = res.changes[DEFAULT_CATEGORY] or {}
			table.insert(res.changes[DEFAULT_CATEGORY], normalize_change(v))
		elseif type(k) == 'string' then
			res.changes[k] = {}
			if type(v) == 'string' then
				table.insert(res.changes[k], normalize_change(v))
			else
				for _, change in pairs(v) do
					table.insert(res.changes[k], normalize_change(change))
				end
			end
		end
	end
	
	return res
end

local function default_only(version)
	return next(version.changes) == DEFAULT_CATEGORY and next(version.changes, DEFAULT_CATEGORY) == nil
end

local function get_more_by(args)
	local change, more_f, by_f = args.change, args.more_f, args.by_f
	local more, by
	if change.more then
		for _, v in pairs(change.more) do
			more = more and more..", " or ""
			more = more..more_f(v)
		end
	end
	if change.by then
		for _, v in pairs(change.by) do
			by = by and by..", " or ""
			by = by..by_f(v)
		end
	end
	return ((more or by) and " (" or "")..
		(more or "")..(by and ("by "..by) or "")..
		((more or by) and ")" or "")
end


local formats = {
	factorio = function(out, version)
		out "---------------------------------------------------------------------------------------------------"
		out("Version: "..version.name)
		if version.date then out("Date: "..version.date); end
		
		for category, changes in pairs(version.changes) do
			out("  "..category..":")
			for _, change in pairs(changes) do
				local more_by = get_more_by{
					change=change,
					more_f=function(v) return v.target; end,
					by_f=function(v) return v.text; end,
				}
				out("    - "..change.description..more_by)
			end
		end
	end,
	
	md = function(out, version)
		out("## "..version.name.." ##")
		
		local categories = not default_only(version)
		for category, changes in pairs(version.changes) do
			if categories then out("### "..category.." ###"); end
			for _, change in pairs(changes) do
				local more_by = get_more_by{
					change=change,
					more_f=function(v) return "["..v.text.."]("..v.target..")"; end,
					by_f=function(v) return (v.text == v.target) and v.text or ("["..v.text.."]("..v.target..")"); end,
				}
				out(" - "..change.description..more_by)
			end
		end
		
		out("")
	end,
	
	forum = function(out, version)
		out("[size=150][b]"..version.name.."[/b][/size]")
		local categories = not default_only(version)
		for category, changes in pairs(version.changes) do
			if categories then out("[b]"..category.."[/b]"); end
			out "[list]"
			for _, change in pairs(changes) do
				local more_by = get_more_by{
					change=change,
					more_f=function(v) return "[url="..v.target.."]"..v.text.."[/url]"; end,
					by_f=function(v) return (v.text == v.target) and v.text or "[url="..v.target.."]"..v.text.."[/url]"; end,
				}
				out("[*]"..change.description..more_by)
			end
			out "[/list]"
		end
	end
}


function _M.format(log, format)
	local res = ""
	local function out(s) res = res..s.."\n"; end
	
	for _, version in ipairs(log) do
		formats[format or 'md'](out, normalize(version))
	end
	
	print(res)
	
	return res
end

for name, _ in pairs(formats) do
	_M[name] = function(log) return _M.format(log, name) end
end


-- Run when launched from the command line
if arg and arg[0] then
	local input = require(arg[1] or 'changelog')
	local out_dir = arg[2] or dirname(arg[0])
	
	local file
	
	file = io.open(out_dir..'changelog.txt', 'w')
	file:write(_M.factorio(input))
	file:close()
	
	file = io.open(out_dir..'changelog.md', 'w')
	file:write(_M.md(input))
	file:close()
	
	file = io.open(out_dir..'changelog_forum.txt', 'w')
	file:write(_M.forum(input))
	file:close()
	
	print("Done.")
end


return _M
