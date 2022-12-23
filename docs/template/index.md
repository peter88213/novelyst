The *novelyst* Python program provides a tree view with parts, chapters and scenes for *.yw7* novel projects. I wrote it for my own use to work on my novels in combination with *OpenOffice* or *LibreOffice*. 

![Screenshot](Screenshots/screen01.png)

With the [oo2yw7 extension for OpenOffice](https://peter88213.github.io/oo2yw7) and the [lo2yw7 extension for LibreOffice](https://peter88213.github.io/lo2yw7), you can write your edited Office documents back to the project.


## Features

- *novelyst* reads and writes [yWriter 7](http://spacejock.com/yWriter7.html) project files.
- The entire project is displayed in a tree, with branches for the narrative, characters, locations, and items.
- Chapters marked as "Start of a new section" in yWriter are treated as parts on a higher level. Normal chapters that follow such a chapter are shown as subtree of the part. In this way, parts can be moved or deleted along with their chapters.
- There is also a "Research" branch that contains all the "Notes type" parts. This can be exported to a separate ODT document. 
- The type of chapters and scenes, as well as the editing status of the scenes are color coded and can be changed via context menu.
- A text viewer window can be toggled on and off.
- There is a wide range of ODF-type file export for *OpenOffice* and *LibreOffice*.
- Several reports can be presented in list form. 
- The application is ready for internationalization with GNU gettext. A German localization is provided. 

## What's the difference to yWriter?

When structuring a novel, *novelyst* builds on the concept of *yWriter*, and extends it in a compatible way. If the appropriate plugin is installed, *yWriter* can even be started with the current project from within the program. Here is a comparison with *yWriter* that illustrates the differences in presentation:

![Screenshot](Screenshots/compare.png)

Please note that *novelyst* is not intended to compete with or replace *yWriter*. Quite deliberately, *novelyst* does not support many of *yWriter's* unique features. It has no scene editor included, no progress control, neither LaTeX nor ebook export. Definition and replacement of global variables and project variables is not supported, neither is inline code. Not to mention yWriter's sophisticated backup features.

The purpose of *novelyst* is to create a structuring framework for novel writing with *LibreOffice* or *OpenOffice Writer*. This means managing a variety of metadata along with the structure of the story, and ensuring a smooth workflow. For this purpose,  there are the appropriate export functions and a simple locking mechanism that gives enough freedom, so that the user remains responsible for making sure that nothing gets mixed up.

- Besides, in *novelyst* you can assign additional properties to the scenes, for example, the style (*staged*, *explaining*, *descriptive*, or *summarizing*), or any number of story arcs. Especially when revising a large novel, this can be quite useful. 
- In addition to the *Action/Reaction* scheme, another custom scene category can be defined by the user. 
- The character data categories "Bio" and "Goals" can be renamed.
- The necessary data is stored along in the *.yw7* file, without breaking the compatibility to *yWriter*.

## Plugins

*novelyst's* functionality can be extended by plugins. Here are some examples:

- [A simple "markup" scene editor](https://peter88213.github.io/novelyst_editor/)
- [A book/series collection manager](https://peter88213.github.io/novelyst_collection/)
- [A relationship matrix](https://peter88213.github.io/novelyst_matrix/)
- [A Timeline plugin](https://peter88213.github.io/novelyst_timeline/)
- [An Aeon Timeline 2 plugin](https://peter88213.github.io/novelyst_aeon2/)
- [A theme changer](https://peter88213.github.io/novelyst_themes/)

There are some more examples in the release's *add-on* folder, such as a yWriter launcher, a theme changer, or an experimental "dark theme" installer.

## Requirements

- [Python](https://www.python.org/) version 3.6+. Under Windows, please use version 3.9.10 or above.
- Tk support for Python. This is usually part of the Windows Python installation, but may need to be installed additionally under Linux.
- Either [LibreOffice](https://www.libreoffice.org/) with the [lo2yw7](https://peter88213.github.io/lo2yw7) or [yw-cnv](https://peter88213.github.io/yw-cnv) extension, 
- or [OpenOffice](https://www.openoffice.org) with the [oo2yw7](https://peter88213.github.io/oo2yw7) or [pywoo](https://peter88213.github.io/pywoo) extension.

### Note for Windows users

The easiest way to install Python on your PC may be via the Microsoft store. 

### Note for Linux users

Please make sure that your Python3 installation has the *tkinter* module. On Ubuntu, for example, it is not available out of the box and must be installed via a separate package named *python3-tk*. 

## General note about the fitness for use

At present, this program is still under active development. Therefore it is recommended to check for updates from time to time, as well as for the plugins. 

I use the program myself and fix errors immediately if I notice any. As far as I can tell, *novelyst* runs fast and reliably under Windows and Linux. It should also under other operating systems for which there is a reasonably up-to-date *Python 3* installation. However, there is a lack of a broad user base, which is why one cannot speak of real proven operation. 

The user documentation is a bit sketchy, and I can't promise support either. So if you're curious, the best way is to explore the feature set yourself with a test project.

As it is the case for *yWriter*, *novelyst* applies to an even greater extent that it organizes the text without worrying about formatting and layout issues. For this, users are assumed to have the necessary knowledge of *OpenOffice* or *LibreOffice*.

## Download and install

[Download the latest release (version 0.99.0)](https://raw.githubusercontent.com/peter88213/novelyst/main/dist/novelyst_v0.99.0.zip)

- Unzip the downloaded zipfile "novelyst_v0.99.0.zip" into a new folder.
- Move into this new folder and launch **setup.pyw**. This installs the application for the local user.
- Create a shortcut on the desktop when asked.
- Optionally, you can replace the "Python" icon by the *novelyst* logo you may find in the installation's **icons** subdirectory.
- Open "README.md" for usage instructions.

------------------------------------------------------------------

[Changelog](changelog)

## Usage

See the [instructions for use](usage)

## Credits

The icons are made using the free *Pusab* font by Ryoichi Tsunekawa, [Flat-it](http://flat-it.com/).

## License

This is Open Source software, and *novelyst* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst/blob/main/LICENSE) file.
