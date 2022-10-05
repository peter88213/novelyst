The *novelyst* Python program provides a tree view with parts, chapters and scenes for novel projects. I wrote it for my own use to work on my novels in combination with OpenOffice/LibreOffice. 

![Screenshot](Screenshots/compare.png)

With the [pywoo extension for OpenOffice](https://peter88213.github.io/pywoo) and the [yw-cnv extension for LibreOffice](https://peter88213.github.io/yw-cnv), you can write your edited Office documents back to the project.

![Screenshot](Screenshots/screen01.png)

## Features

- *novelyst* reads and writes [yWriter 7](http://spacejock.com/yWriter7.html) project files.
- The entire project is displayed in a tree, with branches for the narrative, characters, locations, and items.
- Chapters marked as "Start of a new section" in yWriter are treated as parts on a higher level. Normal chapters that follow such a chapter are shown as subtree of the part. In this way, parts can be moved or deleted along with their chapters.
- There is also a "Research" branch that contains all the "Notes type" parts. This can be exported to a separate ODT document. 
- The type of chapters and scenes, as well as the editing status of the scenes are color coded and can be changed via context menu.
- A text viewer window can be toggled on and off.
- The application is ready for internationalization with GNU gettext. A German localization is provided. 

## Plugins

*novelyst's* functionality can be extended by plugins. Here are some examples:

- [A simple "markup" scene editor](https://peter88213.github.io/novelyst_editor/)
- [A simple "rich text" scene editor](https://peter88213.github.io/novelyst_rich_editor/)
- [A Timeline plugin](https://peter88213.github.io/novelyst_timeline/)
- [An Aeon Timeline 2 plugin](https://peter88213.github.io/novelyst_aeon2/)
- [A theme changer](https://peter88213.github.io/novelyst_themes/)

There are some more examples in the release's *add-on* folder, such as a theme changer, or an experimental "dark theme" installer.

## Requirements

- [Python 3.9.10+](https://www.python.org). 
- Tk support for Python. This is usually part of the Windows Python installation, but may need to be installed additionally under Linux.

## Download and install

[Download the latest release (version 0.99.0)](https://raw.githubusercontent.com/peter88213/novelyst/main/dist/novelyst_v0.99.0.zip)

- Unzip the downloaded zipfile "novelyst_v0.99.0.zip" into a new folder.
- Move into this new folder and launch **setup.pyw**. This installs the application for the local user.
- Create a shortcut on the desktop when asked.
- Open "README.md" for usage instructions.

### Note for Linux users

Please make sure that your Python3 installation has the *tkinter* module. On Ubuntu, for example, it is not available out of the box and must be installed via a separate package. 

------------------------------------------------------------------

[Changelog](changelog)

## Usage

See the [instructions for use](usage)

## Credits

The icons are made using the free *Pusab* font by Ryoichi Tsunekawa, [Flat-it](http://flat-it.com/).

## License

This is Open Source software, and *novelyst* is licenced under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst/blob/main/LICENSE) file.
