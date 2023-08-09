[Project homepage](../index) > [Instructions for use](../usage) > [Online-Hilfe](help) > Command reference: Exportieren-Menü

--- 

# Exportieren-Menü 

**Datei export**

---

## Manuskript zum Bearbeiten

This will write parts, chapters, and scenes into a new OpenDocument
text document (odt) with invisible chapter and scene sections (to be
seen in the Navigator). Datei name suffix is `_Manuskript`.

-   Only "normal" chapters and scenes are exported. Kapitels and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Abschnitts beginning with `<HTML>` or `<TEX>` are not exported.
-   Comments within scenes are written back as scene titles 
    if surrounded by `~`.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   Interspersed HTML, TEX, or RTF commands for yWriter are taken over unchanged.
-   Gobal variables and project variables from yWriter are not resolved.
-   Kapitels and scenes can neither be rearranged nor gelöscht.
-   With *OpenOffice/LibreOffice Writer*, you can split scenes by inserting headings or a scene divider:
    -  *Heading 1* → Neu part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → Neu chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Abschnitt divider. Optionally, you can append the 
       scene title to the scene divider. You can also add a description, separated by `|`.
    - **Note:** Exportieren documents with split scenes from *Writer* to yw7 not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.


---

## Notizen-Kapitel zum Bearbeiten

This will write "Notizen" parts and chapters with child scenes into a new 
OpenDocument text document (odt) with invisible chapter and scene 
sections (to be seen in the Navigator). Datei name suffix is `_notes`.

-   Comments within scenes are written back as scene titles
    if surrounded by `~`.
-   Kapitels and scenes can neither be rearranged nor gelöscht.
-   With *OpenOffice/LibreOffice Writer*, you can split scenes by inserting headings or a scene divider:
    -  *Heading 1* → Neu part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → Neu chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Abschnitt divider. Optionally, you can append the 
       scene title to the scene divider. You can also add a description, separated by `|`.
    - **Note:** Exportieren documents with split scenes from *Writer* to yw7 not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Planungs-Kapitel zum Bearbeiten

This will write "Planung" parts and chapters with child scenes into a new 
OpenDocument text document (odt) with invisible chapter and scene 
sections (to be seen in the Navigator). Datei name suffix is `_todo`.

-   Comments within scenes are written back as scene titles
    if surrounded by `~`.
-   Kapitels and scenes can neither be rearranged nor gelöscht.
-   With *OpenOffice/LibreOffice Writer*, you can split scenes by inserting headings or a scene divider:
    -  *Heading 1* → Neu part title. Optionally, you can add a description, separated by `|`.
    -  *Heading 2* → Neu chapter title. Optionally, you can add a description, separated by `|`.
    -  `###` → Abschnitt divider. Optionally, you can append the 
       scene title to the scene divider. You can also add a description, separated by `|`.
    - **Note:** Exportieren documents with split scenes from *Writer* to yw7 not more than once.      
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Manuskript mit sichtbaren Markierungen zum Korrekturlesen

This will write parts, chapters, and scenes into a new OpenDocument
text document (odt) with visible scene markers. Datei name suffix is
`_proof`.

-   Only "normal" chapters and scenes are exported. Kapitels and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Abschnitts beginning with `<HTML>` or `<TEX>` are not exported.
-   Interspersed HTML, TEX, or RTF commands are taken over unchanged.
-   The document contains scene `[ScID:x]` markers.
    **Do not touch lines containing the markers** if you want to
    be able to write the document back to *yw7* format.
-   Kapitels and scenes can neither be rearranged nor gelöscht.
-   With *OpenOffice/LibreOffice Writer*, you can split scenes by inserting headings or a scene divider:
    -   *Heading 1* → Neu part title. Optionally, you can add a description, separated by `|`.
    -   *Heading 2* → Neu chapter title. Optionally, you can add a description, separated by `|`.
    -   `###` → Abschnitt divider. Optionally, you can append the 
        scene title to the scene divider. You can also add a description, separated by `|`.
    -   **Note:** Exportieren documents with split scenes from *Writer* to yw7 not more than once.      
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Manuskript ohne Markierungen (nur Exportieren)

This will write parts, chapters, and scenes into a new OpenDocument
text document (odt).

-   The document is placed in the same folder as the project.
-   Document's **filename**: `<project name>.odt`.
-   Only "normal" chapters and scenes are exported. Kapitels and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Abschnitts beginning with `<HTML>` or `<TEX>` are not exported.
-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   yWriter comments with special marks (like `/*@en this is an endnote. */`) 
    are converted into footnotes or endnotes. Markup:
    - `@fn*` -- simple footnote, marked with an astersik
    - `@fn` -- numbered footnote
    - `@en` -- numbered endnote   
-   Interspersed HTML, TEX, or RTF commands are removed.
-   Gobal variables and project variables are not resolved.
-   Teil titles appear as first level heading.
-   Kapitel titles appear as second level heading.
-   Abschnitt titles appear as navigable comments pinned to the beginning of
    the scene.
-   Abschnitts are separated by `* * *`. The first line is not
    indented.
-   Beginning from the second paragraph, paragraphs begin with
    indentation of the first line.
-   Abschnitts marked "attach to previous scene" appear like
    continuous paragraphs.
-   Paragraphs starting with `> ` are formatted as quotations.
-   Text markup: Bold and italics are supported. Other highlighting such
    as underline and strikethrough are lost.

---

## Kurzzusammenfassung (nur Exportieren)

This will write a brief synopsis with part, chapter, and scenes titles into a new 
OpenDocument text document.  Datei name suffix is `_brf_synopsis`.
 
-   Only "normal" chapters and scenes are exported. Kapitels and
    scenes marked "unused", "todo" or "notes" are not exported.
-   Only scenes that are intended for RTF export in yWriter will be
    exported.
-   Titels of scenes beginning with `<HTML>` or `<TEX>` are not exported.
-   Teil titles appear as first level heading.
-   Kapitel titles appear as second level heading.
-   Abschnitt titles appear as plain paragraphs.

---

## Bögen (nur Exportieren)

This will write arc-defining "Planung" parts and chapters with child scenes into a new 
OpenDocument text document (odt). Datei name suffix is `_arcs`.

The document contains:
- Teil titles (first level heading, only if the part's first chapter defines an arc)
- Bogen titles (second level heading)
- Bogen descriptions
- Point titles (third level heading)
- Links to the associated scene, if any
- Point descrptions.
- Point contents.


---

## Querverweise (nur Exportieren)

This will generate a new OpenDocument text document (odt) containing
navigable cross references. Datei name suffix is `_xref`. The cross
references are:

-   Abschnitts per character,
-   scenes per location,
-   scenes per item,
-   scenes per tag,
-   characters per tag,
-   locations per tag,
-   items per tag.

---

## Verschleierter Text zur Wortzählung

This will generate a text file (txt) containing all "normal" scenes 
(without headings), where the characters are replaced with "x". 
It generates the same word count as you see displayed in *novelyst*. 

---

## Figuren/Schauplätze/Gegenstände-Datumndateien

This will create a set of XML files containing the project's characters, 
locations, and items with all their properties. 
These files can be used to export the characters, locations, 
and items to another project (also with yWriter 7).

To import XML-Datumndateis from another project, use the **Importieren** command
in the **Figuren**, **Schauplätze**, or **Gegenstände**-Menü. 


---

[<< Zurück](project_notes_menu) -- [Vor >>](tools_menu)