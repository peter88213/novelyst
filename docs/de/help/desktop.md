[Project homepage](../index) > [Instructions for use](../usage) > [Online-Hilfe](help) > Desktop overview

--- 

# Desktop overview


The *novelyst* desktop is divided into three panes:

![Desktop](../Screenshots/desktop01.png)

## Project tree

The project tree in the left pane shows the organization of the project.

- The tree elements are color-coded according to the scene type (see [Basic concepts](basic_concepts)). *Normal* type scenes are highlighted according to the selected coloring mode (see *Programmeinstellungen* in the [Extras-Menü](tools_menu)).
- The order of the columns can be changed (see *Programmeinstellungen* in the [Extras-Menü](tools_menu)).
- Right-clicking on a tree element opens a [Kontextmenü](tree_context_menu) with several options. 

---

### Project tree structure

- The **Buch** branch contains the parts, chapters, and scenes that belong to the novel Manuskript.
- The **Figuren/Schauplätze/Gegenstände** branches contain descriptions of the story world's elements that can be associated with the book's scenes.
- The **Recherche** branch contains all *Notizen* type parts with chapters and scenes intended for the documentation of the story world.
- The **Planung** branch contains all *Planung* type parts with chapters and scenes intended to build the dramaturgical structure of the story. This is the right place for planning plot points, archetypes, character arcs, and so on. 

---

### Project tree operation

---

#### Browse the tree

- **F11** selects a node back in the tree browsing history.
- **F12** selects a node forward in the tree browsing history.

On Windows, the "Forward" and "Back" mouse buttons (if any) may also work.

---

#### Move parts, chapters, and scenes

Drag and drop while pressing the **Alt** key. Be aware, there is no "Undo" feature. 

---

#### Löschen parts, chapters, and scenes

Select item and hit the **Del** key.

- When deleting a part, chapter oder scene, the scenes are moved to the _Papierkorb_ chapter at the bottom. 
- The _Papierkorb_ chapter is created automatically, if needed. 
- When deleting the _Papierkorb_ chapter, all scenes are gelöscht.

- The type of chapters and scenes, as well as the editing status of the scenes are color coded and can be changed via Kontextmenü.
- Within chapters, scenes of the same type and with the same viewpoint can be joined.
- "Notizen" and "To do" type chapters can be exported to a separate ODT document. 

---

## Content viewer

The **Content viewer** in the middle pane shows the part/chapter/scene contents with their titles as headings.

- You can open or close the content viewer with **Ansicht > Textbetrachter anzeigen/verbergen** or **Ctrl-T**.
- On opening, the windows shows the text, where the tree is selected.
- When changing the tree selection, the text moves along.
- However, the text can be scrolled independently with the verical scrollbar, or the mousewheel. 
- You can select text with the mouse, and copy it to the clipboard with **Ctrl-C**.
- You cannot edit the text. For this, you might want to install an editor plugin, such as [novelyst_editor](https://peter88213.github.io/novelyst_editor/).
- Abschnitt text is color-coded according to the scene type (see [Basic concepts](basic_concepts)).
- With the **Markup anzeigen** checkbox scene markup such as bold, italics, and language can be shown/hidden.

---

## Properties
The **Properties** in the right pane show properties/metadata of the element selected in the project tree. 

- You can open or close the element properties window with **Ansicht > Eigenschaften anzeigen/verbergen** or **Ctrl-Alt-T**.
- On opening, the windows shows the editable properties of the selected element.
- You can detach or dock the element properties window with **Ansicht > Eigenschaften abtrennen/andocken** or **Ctrl-Alt-D**.
- On closing the detached window, the properties are docked again.


