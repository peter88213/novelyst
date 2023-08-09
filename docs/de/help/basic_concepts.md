[Project homepage](../index) > [Instructions for use](../usage) > [Online-Hilfe](help) > Basic concepts

--- 

# Basic concepts

---

## Teil/chapter/scene types

Each parts, chapter, and scene  is of a type that can be changed via Kontextmenü or Teil/Kapitel/Abschnitt-Menü. 
The type can be *Normal*, *Notizen*, *Planung*, or *Unbenutzt*.

### Normal

- "Normal" type parts, chapters, and scenes are counted. The totals are displayed in the status bar.
- "Normal" type scenes are exported to the Manuskript and included in the word count. 
- "Normal" type parts and chapters can have subelements of each type. 
- "Normal" type tree elements are color coded according to the [coloring mode settings](tools_menu#coloring-mode).

### Unbenutzt

You can mark parts, chapters, and scenes as unused to exclude them from word count totals and export.

- The subelements of unused parts and chapters are unused as well.
- If you mark a scene "Unbenutzt", its properties are preserved. 
- Unbenutzt tree elements are displayed in gray.

### Notizen

You can mark parts, chapters, and scenes as "Notizen" to exclude them from word count and regular export. 
Such elements may contain background information or research data.

- "Notizen" type chapters and scenes can be subelements of the "Buch" or "Recherche" branch. 
- The subelements of "Notizen" parts and chapters are of the "Notizen" type as well.
- Alle "Notizen" type parts are placed in the "Recherche" branch.
- Alle "Notizen" type chapters can be exported to a single ODT document for editing.
- "Notizen" type tree elements are displayed in blue.

### Planung

You can mark parts, chapters, and scenes as "Planung" to exclude them from word count and regular export. 
Such elements may carry information about plot or story structure.

- The subelements of "Planung" parts and chapters are of the "Planung" Type as well.
- "Planung" type chapters and scenes can be subelements of the "Buch" or "Planung" branch.
- Alle "Planung" type parts are placed in the "Planung" branch.
- "Planung" type chapters and scenes are used for [arc](arcs) definition.
- Alle "Planung" type chapters can be exported to a single ODT document for editing.
- "Planung" type tree elements are displayed in red.

---

## Abschnitt completion status

You can assign a status to each "Normal" type scene via Kontextmenü or Abschnitt-Menü.

- Neuly created scenes are set to "Gliederung" by default.
- Word counts by status appear in the "Buch" properties.

---

## Modus of discourse

A scene's mode can be *szenisch*, *erklärend*, *beschreibend*, or *zusammenfassend*.

- **Staged** scenes are mainly made up of action and dialog.
- **Explaining** scenes mainly convey background information.
- **Descriptive** scenes describe characters, locations, etc in detail.
- **Summarizing** scenes summarize actions in brief, for example, to make time tighter.
- Neuly created scenes are set to "szenisch" by default.

---

## Formatting text

It is assumed that very few types of text markup are needed for a novel text:

- *Emphasized* (usually shown as italics).
- *Strongly emphasized* (usually shown as capitalized).
- *Citation* (paragraph visually distinguished from body text).

When exporting to ODT format, *novelyst* replaces these formattings as follows: 

- Text with `[i]Italic markup[/i]` is formatted as *Emphasized*.
- Text with `[b]Bold markup[/b]` is formatted as *Strongly emphasized*. 
- Paragraphs starting with `> ` are formatted as *Quote*.

---

## Comments, footnotes, endnotes

In general, the following applies when exporting to ODT format:

-   Comments in the text bracketed with slashes and asterisks (like
    `/* this is a comment */`) are converted to author's comments.
-   ODT author's comments are kept when re-converting to yw7 format. 

When exporting to the Manuskript without tags also applies:

-   yw7 comments with special marks (like `/*@en this is an endnote. */`) 
    are converted into footnotes or endnotes. Markup:
    - `@fn*` -- simple footnote, marked with an astersik
    - `@fn` -- numbered footnote
    - `@en` -- numbered endnote   

This is how a simple footnote substitute looks when inserted as a marked comment with LibreOffice in the working document:

![Screenshot](../Screenshots/footnote01.png)

This is how it looks in the *novelyst* contents viewer, or in the *novelyst_editor* scene editor:

![Screenshot](../Screenshots/footnote03.png)

This is the real footnote in the final Manuskript without tags:

![Screenshot](../Screenshots/footnote02.png)

---

## About document language handling

ODF documents are generally assigned a language that determines spell checking and country-specific character substitutions. In addition, Office Writer lets you assign text passages to languages other than the document language to mark foreign language usage or to suspend spell checking. 

*novelyst* supports this language handling for *OpenOffice/LibreOffice* interoperability.

### Document overall

The project language (Sprachencode acc. to ISO 639-1 and country code acc. to ISO 3166-2) can be set in the **Project** settings (right pane) under **Sprache des Dokuments**. The codes are stored as *yWriter* project variables. 

### Text passages in scenes

Text markup for other languages is imported from ODT documents. It is represented by *yWriter* project variables. Thus it's fully compatible with *yWriter*, which interprets them as HTML instructions during document export.

This then looks like this, for example:

`xxx xxxx [lang=en-AU]yyy yyyy yyyy[/lang=en-AU] xxx xxx` 

For the example shown above, the project variable definition for the opening tag looks like this: 

- *Variable Name:* `lang=en-AU` 
- *Value/Text:* `<HTM <SPAN LANG="en-AU"> /HTM>`

The point of this is that such language assignments are preserved even after multiple conversions in both directions, so they are always effective for spell checking in the ODT document.

It is recommended not to modify such markups with *novelyst* to avoid unwanted nesting and broken enclosing. 

