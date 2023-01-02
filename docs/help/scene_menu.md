[Project homepage](../index) > [Instructions for use](../usage) > Command reference: Scene menu

--- 

# Scene menu 

**Scene operation**

--- 

## Add

**Add a new scene**

You can add a scene to the tree with **Scene > Add**.
- The new scene is placed at the next free position after the selection, if possible.
- Otherwise, no new scene is generated.  
- The new scene has an auto-generated title. You can change it in the right pane.

--- 

## Set Type

**Set the scene type**

--- 

## Set Status

**Set the scene completion status**

--- 

## Set Style

**Set the scene style**

--- 

## Export scene descriptions for editing 

**Export an ODT document**

This will generate a new OpenDocument text document (odt) containing a
**full synopsis** with part/chapter headings and scene descriptions that can
be edited and written back to yWriter format. File name suffix is
`_scenes`.

--- 

## Export scene list (spreadsheet) 

**Export an ODS document**

This will generate a new OpenDocument spreadsheet (ods) listing the following:

- Hyperlink to the manuscript's scene section
- Scene title
- Scene description
- Tags
- Scene notes
- A/R
- Goal
- Conflict
- Outcome
- Sequential scene number
- Words total
- Rating 1
- Rating 2
- Rating 3
- Rating 4
- Word count
- Letter count
- Status
- Characters
- Locations
- Items

Only "normal" scenes that would be exported as RTF in yWriter get a 
row in the scene list. Scenes of the "Unused", "Notes", or "ToDo" 
type are omitted.

Scenes beginning with `<HTML>` or `<TEX>` are omitted.

File name suffix is `_scenelist`.

--- 

[<< Previous](chapter_menu) -- [Next >>](characters_menu)