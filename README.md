# novelyst

The *novelyst* Python program provides a tree view with parts, chapters and scenes for *.yw7* novel projects. The purpose of *novelyst* is to create a structuring framework for novel writing with *LibreOffice* or *OpenOffice Writer*. This means managing a variety of metadata along with the structure of the story, and ensuring a smooth workflow. For this purpose,  there are the appropriate export functions and a simple locking mechanism that gives enough freedom, so that the user remains responsible for making sure that nothing gets mixed up.

For more information, see the [project homepage](https://peter88213.github.io/novelyst) with description and download instructions.

## Development

*novelyst* depends on the [pywriter](https://github.com/peter88213/PyWriter) library which must be present in your file system. It is organized as an Eclipse PyDev project. The official release branch on GitHub is *main*.

### Mandatory directory structure for building the application script

```
.
├── PyWriter/
│   └── src/
│       └── pywriter/
└── novelyst/
    ├── src/
    ├── test/
    └── tools/ 
        └── build.xml
```

### Conventions

- Minimum Python version is 3.6. 
- The Python **source code formatting** follows widely the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide, except the maximum line length, which is 120 characters here.

### Development tools

- [Python](https://python.org) version 3.9
- [Eclipse IDE](https://eclipse.org) with [PyDev](https://pydev.org) and [EGit](https://www.eclipse.org/egit/)
- [Apache Ant](https://ant.apache.org/) for building the application script
- [Gaphor](https://gaphor.org/) for creating UML diagrams


## Credits

The icons are made using the free *Pusab* font by Ryoichi Tsunekawa, [Flat-it](http://flat-it.com/).

## License

This is Open Source software, and *novelyst* is licenced under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst/blob/main/LICENSE) file.

