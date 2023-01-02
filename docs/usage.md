[Project homepage](https://peter88213.github.io/novelyst) > Instructions for use

--- 

The *novelyst* Python program provides a tree view for *.yw7* novel projects.

# Instructions for use

## Launch the program

The included installation script prompts you to create a shortcut on the desktop. 

You can either

- launch the program by double-clicking on the shortcut icon, or
- launch the program by dragging a *.yw7* project file and dropping it on the shortcut icon.


# Online help

## Command reference

### [File menu](https://peter88213.github.io/novelyst/help/file_menu)
### [View menu](https://peter88213.github.io/novelyst/help/view_menu)
### [Part menu](https://peter88213.github.io/novelyst/help/part_menu)
### [Chapter menu](https://peter88213.github.io/novelyst/help/chapter_menu)
### [Scene menu](https://peter88213.github.io/novelyst/help/scene_menu)
### [Characters menu](https://peter88213.github.io/novelyst/help/characters_menu)
### [Locations menu](https://peter88213.github.io/novelyst/help/locations_menu)
### [Items menu](https://peter88213.github.io/novelyst/help/items_menu)
### [Project notes menu](https://peter88213.github.io/novelyst/help/project_notes_menu)
### [Export menu](https://peter88213.github.io/novelyst/help/export_menu)
### [Tools menu](https://peter88213.github.io/novelyst/help/tools_menu)


# Tree view operation

### Move parts, chapters, and scenes

Drag and drop while pressing the **Alt** key. Be aware, there is no "Undo" feature. 
- When moving a normal chapter from the narrative to the "Research" branch, be sure to
  change its type to "Notes".

### Delete parts, chapters, and scenes

Select item and hit the **Del** key.

- When deleting a part, chapter oder scene, the scenes are moved to the _Trash_ chapter at the bottom. 
- The _Trash_ chapter is created automatically, if needed. 
- When deleting the _Trash_ chapter, all scenes are deleted.



### Reports

You can have *novelyst* generate a variety of reports. These are list-formatted HTML files, 
displayed with your system's web browser. They are temporary files, auto-deleted on program exit.
If needed, you can have your web browser save or print them.

### ODF export

The same *export* functions are used here as are implemented as *import* functions in the 
*LibreOffice*/*OpenOffice* *yWriter import/export* extensions.

Please refer to the extension's help text. 


### A note about formatting text

It is assumed that very few types of text markup are needed for a novel text:

- *Emphasized* (usually shown as italics).
- *Strongly emphasized* (usually shown as capitalized).
- *Citation* (paragraph visually distinguished from body text).

When exporting to ODT format, *novelyst* replaces these formattings as follows: 

- Text with `[i]Italic markup[/i]` is formatted as *Emphasized*.
- Text with `[b]Bold markup[/b]` is formatted as *Strongly emphasized*. 
- Paragraphs starting with `> ` are formatted as *Quote*.

## License

This is Open Source software, and *novelyst* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst/blob/main/LICENSE) file.

