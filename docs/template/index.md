The *novelyst* Python program provides a tree view with parts, chapters and scenes for [yWriter](http://spacejock.com/yWriter7.html) projects. I wrote it for my own use to work on my novels in combination with OpenOffice/LibreOffice. 

With the [pywoo extension for OpenOffice](https://peter88213.github.io/pywoo) and the [yw-cnv extension for LibreOffice](https://peter88213.github.io/yw-cnv), you can write your edited Office documents back to the yWriter project.

## Requirements

- [Python 3.6+](https://www.python.org). 
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

Bryan Oakley presented a Rich Text example on [stack overflow](https://stackoverflow.com/questions/63099026/fomatted-text-in-tkinter).


## License

novelyst is distributed under the [MIT License](http://www.opensource.org/licenses/mit-license.php).
