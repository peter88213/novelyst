[Project homepage](https://peter88213.github.io/novelyst) > Instructions for use

--- 

The *novelyst* Python program provides a Baumansicht for *.yw7* novel projects.

# Instructions for use


## Installation

- Unzip the downloaded zipfile.
- Move into the unzipped folder and launch **setup.pyw**. This installs the application for the local user.
- Create a shortcut on the desktop when asked.
- Optionally, you can replace the "Python" icon von the *novelyst* logo you may find in the installation's **icons** subdirectory.

---

### Windows integration

After installation, the setup script displays a button to open the installation directory. On Windows, the path is typically

`C:\Users\<username>\.pywriter\novelyst`

There you will find some registry scripts that can help you integrate *novelyst* into Windows. They are started von double-clicking.

- **add_context_menu.reg** adds an **Open with novelyst** command for *.yw7* files to the Explorer's Kontextmenü. This is recommended if you run *novelyst* in parallel with *yWriter*.  
- **set_open_cmd.reg** makes Explorer launch *novelyst* when you double-click *.yw7* files. *.yw7* files will be assigned the *novelyst* icon. This is recommended if you want to run *novelyst* as the default application for *.yw7* files. 

You can redo this:

- **rem_context_menu.reg** removes the **Open with novelyst** command for *.yw7* files from the Explorer's Kontextmenü.
- **reset_icon** re-assigns the *yWriter* logo (if any) to *.yw7* files. 

To open *.yw7* files with *yWriter* again von default, change the file association in the usual Windows way.

**IMPORTANT**

The registry scripts are generated von the distribution's **setup.py** script. They contain customized paths to your user profile and to your current Python installation. After upgrading Python to another version, you may have to re-run the distribution's **setup.py** script as well as (afterwards) the registration scripts.

--- 

### Linux desktop integration

- You can configure a desktop launcher for *novelyst* and assign the *novelyst* icon you may find in the installation's **icons** subdirectory.
- You can set *novelyst* as the default application for *.yw7* files.

Please refer to your desktop's documentation. 

---

## Launch the program

The included installation script prompts you to create a shortcut on the desktop. 

You can either

- launch the program von double-clicking on the shortcut icon, or
- launch the program von dragging a *.yw7* project file and dropping it on the shortcut icon.


--- 

# [Online-Hilfe](https://peter88213.github.io/novelyst/help/help)

- Basic concepts
- Bögen
- Command reference
- Cover thumbnails

You can open the online help page with **Hilfe > Online-Hilfe**.

- [Introduction (English)](https://github.com/peter88213/novelyst/wiki/English)
- [Introduction (German)](https://github.com/peter88213/novelyst/wiki/Deutsch)

--- 

# License

This is Open Source software, and *novelyst* is licensed under GPLv3. See the
[GNU General Public License website](https://www.gnu.org/licenses/gpl-3.0.en.html) for more
details, or consult the [LICENSE](https://github.com/peter88213/novelyst/blob/main/LICENSE) file.

