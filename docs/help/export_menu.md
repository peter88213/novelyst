[Project homepage](../index) > [Instructions for use](../usage) > [Online help](help) > Command reference: Export menu

--- 

# Export menu 

**File export**

---

## Manuscript for editing

This will write parts, chapters, and scenes into a new OpenDocument
text document (odt) with invisible chapter and scene sections (to be
seen in the Navigator). File name suffix is `_manuscript`.

-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Comments within scenes are written back as scene titles 
    if surrounded by `~`.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   Interspersed HTML, TEX, or RTF commands for yWriter are taken over unchanged.
-   Gobal variables and project variables from yWriter are not resolved.
-   Chapters and scenes can neither be rearranged nor deleted.
-   With *OpenOffice/LibreOffice Writer*, you can split scenes by inserting headings or a scene divider:
    -  *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Scene divider. Optionally, you can append the 
       scene title to the scene divider. You can also add a description, separated by `|`.
    - **Note:** Export documents with split scenes from *Writer* to yw7 not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.


---

## Notes chapters for editing

This will write "Notes" parts and chapters with child scenes into a new 
OpenDocument text document (odt) with invisible chapter and scene 
sections (to be seen in the Navigator). File name suffix is `_notes`.

-   Comments within scenes are written back as scene titles
    if surrounded by `~`.
-   Chapters and scenes can neither be rearranged nor deleted.
-   With *OpenOffice/LibreOffice Writer*, you can split scenes by inserting headings or a scene divider:
    -  *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Scene divider. Optionally, you can append the 
       scene title to the scene divider. You can also add a description, separated by `|`.
    - **Note:** Export documents with split scenes from *Writer* to yw7 not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Todo chapters for editing

This will write "Todo" parts and chapters with child scenes into a new 
OpenDocument text document (odt) with invisible chapter and scene 
sections (to be seen in the Navigator). File name suffix is `_todo`.

-   Comments within scenes are written back as scene titles
    if surrounded by `~`.
-   Chapters and scenes can neither be rearranged nor deleted.
-   With *OpenOffice/LibreOffice Writer*, you can split scenes by inserting headings or a scene divider:
    -  *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Scene divider. Optionally, you can append the 
       scene title to the scene divider. You can also add a description, separated by `|`.
    - **Note:** Export documents with split scenes from *Writer* to yw7 not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Manuscript with visible structure tags for proof reading

This will write parts, chapters, and scenes into a new OpenDocument
text document (odt) with visible scene markers. File name suffix is
`_proof`.

-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Interspersed HTML, TEX, or RTF commands are taken over unchanged.
-   The document contains chapter and scene headings. However, changes will not be written back.
-   The document contains scene `[ScID:x]` markers.
    **Do not touch lines containing the markers** if you want to
    be able to write the document back to *yw7* format.
-   Chapters and scenes can neither be rearranged nor deleted.
-   When editing the document, you can split scenes by inserting headings or a scene divider:
    -   *Heading 1* → New part title. Optionally, you can add a description, separated by `|`.
    -   *Heading 2* → New chapter title. Optionally, you can add a description, separated by `|`.
    -   `###` → Scene divider. Optionally, you can append the 
        scene title to the scene divider. You can also add a description, separated by `|`.
    -   **Note:** Export documents with split scenes from *Writer* to yw7 not more than once.      
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Manuscript without tags (export only)

This will write parts, chapters, and scenes into a new OpenDocument
text document (odt).

-   The document is placed in the same folder as the project.
-   Document's **filename**: `<project name>.odt`.
-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   yWriter comments with special marks (like `/*@en this is an endnote. */`) 
    are converted into footnotes or endnotes. Markup:
    - `@fn*` -- simple footnote, marked with an astersik
    - `@fn` -- numbered footnote
    - `@en` -- numbered endnote   
-   Interspersed HTML, TEX, or RTF commands are removed.
-   Gobal variables and project variables are not resolved.
-   Part titles appear as first level heading.
-   Chapter titles appear as second level heading.
-   Scene titles appear as navigable comments pinned to the beginning of
    the scene.
-   Scenes are separated by `* * *`. The first line is not
    indented.
-   Starting from the second paragraph, paragraphs begin with
    indentation of the first line.
-   Scenes marked "attach to previous scene" appear like
    continuous paragraphs.
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Brief synopsis (export only)

This will write a brief synopsis with part, chapter, and scenes titles into a new 
OpenDocument text document.  File name suffix is `_brf_synopsis`.
 
-   Only "normal" chapters and scenes are exported. Chapters and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Titles of scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Part titles appear as first level heading.
-   Chapter titles appear as second level heading.
-   Scene titles appear as plain paragraphs.

---

## Arcs (export only)

This will write arc-defining "Todo" parts and chapters with child scenes into a new 
OpenDocument text document (odt). File name suffix is `_arcs`.

The document contains:
- Part titles (first level heading, only if the part's first chapter defines an arc)
- Arc titles (second level heading)
- Arc descriptions
- Point titles (third level heading)
- Links to the associated scene, if any
- Point descrptions.
- Point contents.


---

## Cross references (export only)

This will generate a new OpenDocument text document (odt) containing
navigable cross references. File name suffix is `_xref`. The cross
references are:

-   Scenes per character,
-   scenes per location,
-   scenes per item,
-   scenes per tag,
-   characters per tag,
-   locations per tag,
-   items per tag.

---

## Obfuscated text for word count

This will generate a text file (txt) containing all "normal" scenes 
(without headings), where the characters are replaced with "x". 
It generates the same word count as you see displayed in *novelyst*. 

---

## Characters/locations/items data files

This will create a set of XML files containing the project's characters, 
locations, and items with all their properties. 
These files can be used to export the characters, locations, 
and items to another project (also with yWriter 7).

To import XML data files from another project, use the **Import** command
in the **Characters**, **Locations**, or **Items** menu. 

---

## Show Plot list

Show scenes, arcs, plot structure, and plot points.
This will generate a list-formatted HTML file, and launch your system's web browser for displaying it. 

- The Report is a temporary file, auto-deleted on program exit.
- If needed, you can have your web browser save or print it.

---

[<< Previous](project_notes_menu) -- [Next >>](tools_menu)