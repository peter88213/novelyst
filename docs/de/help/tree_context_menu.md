[Project homepage](../index) > [Instructions for use](../usage) > [Online-Hilfe](help) > Baumansicht Kontextmenü

--- 

# Baumansicht Kontextmenü

When right-clicking on a tree element in the left pane, a Kontextmenü opens. 

Greyed-out entries are not available, e.g. due to "project lock".

---

## Buch/Recherche/Planung Kontextmenü entries

### Abschnitt hinzufügen

Hinzufügens a new scene.

- The new scene is placed at the next free position after the selection.
- The new scene has an auto-generated title. You can change it in the right pane.

#### Properties of a new scene

- *Normal* type
- *Gliederung* completion status
- *Staged* mode
- No viewpoint character assigned
- No arc or tag assigned
- No date/time set

### Kapitel hinzufügen

Hinzufügens a new chapter.

- The new chapter is placed at the next free position after the selection.
- The new chapter has an auto-generated title. You can change it in the right pane.

### Kapitel hochstufen

Converts the selected chapter into a part. 

- Kapitels that follow the selected one to the next part will be placed below the new part.

### Teil hinzufügen

Hinzufügens a new part.
- The new part is placed at the next free position after the selection.
- The new part has an auto-generated title. You can change it in the right pane.

### Teil herabstufen

Converts the selected part into a chapter.

- The chapters of the part together with the converted part are allocated to the preceding part, if there is one.

### Teilung aufheben

Removes the selected part but keep its chapters.

- The chapters of the removed part are allocated to the preceding part, if there is one. 

### Löschen

Löschens the selected tree element and its children. 

- Teils and chapters are gelöscht.
- Abschnitts are marked "unused" and moved to the "Papierkorb" chapter. 

### Typ wählen

Sets the [type](basic_concepts) of the selected scene. This can be *Normal*, *Notizen*, *Planung*, or *Unbenutzt*.

- Select a parent node to set the type for multiple scenes.

### Status setzen

Sets the [completion status](basic_concepts) of the selected scene.

- Select a parent node to set the status for multiple scenes.

### Modus bestimmen

Sets the [mode of discourse](basic_concepts) of the selected scene. This can be *szenisch*, *erklärend*, *beschreibend*, or *zusammenfassend*.

- Select a parent node to set the mode for multiple scenes.

### Mit dem vorhergehenden zusammenfassen

Joins two scenes, if within the same chapter, of the same type, and with the same viewpoint.

- Neu title = title of the prevoius scene & title of the selected scene
- The scene contents are concatenated, separated by a paragraph separator.
- Beschreibungs are concatenated, separated by a paragraph separator.
- Ziele are concatenated, separated by a paragraph separator.
- Konflikts are concatenated, separated by a paragraph separator.
- Ausgangs are concatenated, separated by a paragraph separator.
- Notizen are concatenated, separated by a paragraph separator.
- Figurenlistes are merged.
- Schauplatzlistes are merged.
- Gegenstandslistes are merged.
- [Bogen](arcs) assignments are merged.
- [Bogen](arcs) point associations] are moved to the joined scene, if any.
- Abschnitt durations are added.

### Kapitelebene anzeigen

Hides the scenes by collapsing the tree, so that only parts and chapters are visible.

### Aufklappen

Shows a whole branch by expanding the selected tree element.

### Einklappen

Hides the child elements of the selected tree element.

### Alles aufklappen

Shows the whole tree.

### Alle einklappen

Hides all tree elements except the main categories.

---

## Figuren/Schauplätze/Gegenstände Kontextmenü entries

### Hinzufügen

Hinzufügens a new character/location/item.

- The new element is placed after the selected one.
- The new element has an auto-generated title. You can change it in the right pane.
- The status of newly created characters is *minor*.

### Löschen

Löschens the selected character/location/item.

### Status setzen

Sets the selected character's status. This can be *major* or *minor*.

- Select the *Figuren* root node to set the status for all characters.

---

[<< Zurück](tools_menu) -- [First >>](file_menu)