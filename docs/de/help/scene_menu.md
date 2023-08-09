[Project homepage](../index) > [Instructions for use](../usage) > [Online-Hilfe](help) > Command reference: Abschnitt-Menü

--- 

# Abschnitt-Menü 

**Abschnitt operation**

--- 

## Hinzufügen

**Hinzufügen a new scene**

You can add a scene to the tree with **Abschnitt > Hinzufügen**.
- The new scene is placed at the next free position after the selection, if possible.
- Otherwise, no new scene is generated.  
- The new scene has an auto-generated title. You can change it in the right pane.

### Properties of a new scene

- *Normal* type
- *Gliederung* completion status
- *Staged* mode
- No viewpoint character assigned
- No arc or tag assigned
- No date/time set

--- 

## Typ wählen

**Set the [type](basic_concepts) of the selected scene**

This can be *Normal*, *Notizen*, *Planung*, or *Unbenutzt*.

### Type change for multiple scenes

- Either select multiple scenes, or
- select a parent node (part or chapter)

--- 

## Status setzen

**Set the [scene completion status](basic_concepts)**

This can be *Gliederung*, *Entwurf*, *1. Überarbeitung*, *2. Überarbeitung*, or *Fertiggestellt*.

### Status change for multiple scenes

- Either select multiple scenes, or
- select a parent node (part, chapter, or Buch)

--- 

## Modus bestimmen

**Set the scene's [mode of discourse](basic_concepts)**

This can be *szenisch*, *erklärend*, *beschreibend*, or *zusammenfassend*.

### Modus change for multiple scenes

- Either select multiple scenes, or
- select a parent node (part, chapter, or Buch)

--- 

## Abschnittsbeschreibungen zum Bearbeiten exportieren 

**Exportieren an ODT document**

This will generate a new OpenDocument text document (odt) containing a
**full synopsis** with part/chapter headings and scene descriptions that can
be edited and written back to project format. Datei name suffix is
`_scenes`.

--- 

## Abschnittsliste exportieren (Tabelle) 

**Exportieren an ODS document**

This will generate a new OpenDocument spreadsheet (ods) listing the following:

- Hyperlink to the Manuskript's scene section
- Abschnitt title
- Abschnitt description
- Tags
- Abschnitt notes
- A/R
- Ziel
- Konflikt
- Ausgang
- Sequential scene number
- Wörter total
- Rating 1
- Rating 2
- Rating 3
- Rating 4
- Word count
- Letter count
- Status
- Figuren
- Schauplätze
- Gegenstände

Only "normal" scenes get a row in the scene list. Abschnitts of the "Unbenutzt", "Notizen", or "ToDo" 
type are omitted.

Abschnitts beginning with `<HTML>` or `<TEX>` are omitted.

Datei name suffix is `_scenelist`.

--- 

[<< Zurück](chapter_menu) -- [Vor >>](characters_menu)