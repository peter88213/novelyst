[Project homepage](../index) > [Instructions for use](../usage) > [Online help](help) > Command reference: Scene menu

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

### Properties of a new scene

- *Normal* type
- *Outline* completion status
- *Staged* mode
- No viewpoint character assigned
- No arc or tag assigned
- No date/time set

--- 

## Set Type

**Set the [type](basic_concepts) of the selected scene**

This can be *Normal*, *Notes*, *Todo*, or *Unused*.

### Type change for multiple scenes

- Either select multiple scenes, or
- select a parent node (part or chapter)

--- 

## Set Status

**Set the [scene completion status](basic_concepts)**

This can be *Outline*, *Draft*, *1st Edit*, *2nd Edit*, or *Done*.

### Status change for multiple scenes

- Either select multiple scenes, or
- select a parent node (part, chapter, or Narrative)

--- 

## Set Mode

**Set the scene's [mode of discourse](basic_concepts)**

This can be *staged*, *explaining*, *descriptive*, or *summarizing*.

### Mode change for multiple scenes

- Either select multiple scenes, or
- select a parent node (part, chapter, or Narrative)

--- 

## Export scene descriptions for editing 

**Export an ODT document**

This will generate a new OpenDocument text document (odt) containing a
**full synopsis** with part/chapter headings and scene descriptions that can
be edited and written back to project format. File name suffix is
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

Only "normal" scenes get a row in the scene list. Scenes of the "Unused", "Notes", or "ToDo" 
type are omitted.

Scenes beginning with `<HTML>` or `<TEX>` are omitted.

File name suffix is `_scenelist`.

--- 

[<< Previous](chapter_menu) -- [Next >>](characters_menu)