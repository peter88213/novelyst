[Project homepage](../index) > [Instructions for use](../usage) > [Online help](help) > Basic concepts

--- 

# Basic concepts

---

## Part/chapter/scene types

Each parts, chapter, and scene  is of a type that can be changed via context menu or Part/Chapter/Scene menu. 
The type can be *Normal*, *Notes*, *Todo*, or *Unused*.

### Normal

- "Normal" type parts, chapters, and scenes are counted. The totals are displayed in the status bar.
- "Normal" type scenes are exported to the manuscript and included in the word count. 
- "Normal" type parts and chapters can have subelements of each type. 
- "Normal" type tree elements are color coded according to the [coloring mode settings](tools_menu#coloring-mode).

### Unused

You can mark parts, chapters, and scenes as unused to exclude them from word count totals and export.

- The subelements of unused parts and chapters are unused as well.
- If you mark a scene "Unused", its properties are preserved. 
- Unused tree elements are displayed in gray.

### Notes

You can mark parts, chapters, and scenes as "Notes" to exclude them from word count and regular export. 
Such elements may contain background information or research data.

- "Notes" type chapters and scenes can be subelements of the "Book" or "Research" branch. 
- The subelements of "Notes" parts and chapters are of the "Notes" type as well.
- All "Notes" type parts are placed in the "Research" branch.
- All "Notes" type chapters can be exported to a single ODT document for editing.
- "Notes" type tree elements are displayed in blue.

### Todo

You can mark parts, chapters, and scenes as "Todo" to exclude them from word count and regular export. 
Such elements may carry information about plot or story structure.

- The subelements of "Todo" parts and chapters are of the "Todo" Type as well.
- "Todo" type chapters and scenes can be subelements of the "Book" or "Planning" branch.
- All "Todo" type parts are placed in the "Planning" branch.
- "Todo" type chapters and scenes are used for [arc](arcs) definition.
- All "Todo" type chapters can be exported to a single ODT document for editing.
- "Todo" type tree elements are displayed in red.

---

## Scene completion status

You can assign a status to each "Normal" type scene via context menu or Scene menu.

- Newly created scenes are set to "Outline" by default.
- Word counts by status appear in project properties.

---

## Mode of discourse

A scene's mode can be *staged*, *explaining*, *descriptive*, or *summarizing*.

- **Staged** scenes are mainly made up of action and dialog.
- **Explaining** scenes mainly convey background information.
- **Descriptive** scenes describe characters, locations, etc in detail.
- **Summarizing** scenes summarize actions in brief, for example, to make time tighter.
- Newly created scenes are set to "staged" by default.

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

## About document language handling

ODF documents are generally assigned a language that determines spell checking and country-specific character substitutions. In addition, Office Writer lets you assign text passages to languages other than the document language to mark foreign language usage or to suspend spell checking. 

*novelyst* supports this language handling for *OpenOffice/LibreOffice* interoperability.

### Document overall

The project language (Language code acc. to ISO 639-1 and country code acc. to ISO 3166-2) can be set in the **Project** settings (right pane) under **Document language**. The codes are stored as *yWriter* project variables. 

### Text passages in scenes

Text markup for other languages is imported from ODT documents. It is represented by *yWriter* project variables. Thus it's fully compatible with *yWriter*, which interprets them as HTML instructions during document export.

This then looks like this, for example:

`xxx xxxx [lang=en-AU]yyy yyyy yyyy[/lang=en-AU] xxx xxx` 

For the example shown above, the project variable definition for the opening tag looks like this: 

- *Variable Name:* `lang=en-AU` 
- *Value/Text:* `<HTM <SPAN LANG="en-AU"> /HTM>`

The point of this is that such language assignments are preserved even after multiple conversions in both directions, so they are always effective for spell checking in the ODT document.

It is recommended not to modify such markups with *novelyst* to avoid unwanted nesting and broken enclosing. 

