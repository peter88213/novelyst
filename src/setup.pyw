#!/usr/bin/python3
"""Install the novelyst script. 

Version @release

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
import os
import sys
import stat
import glob
from shutil import copyfile
from shutil import copytree
from pathlib import Path
from string import Template
import gettext
import locale
import platform
try:
    import tkinter as tk
except ModuleNotFoundError:
    print('The tkinter module is missing. Please install the tk support package for your python3 version.')
    sys.exit(1)
from tkinter import messagebox

# Initialize localization.
LOCALE_PATH = f'{os.path.dirname(sys.argv[0])}/locale/'
try:
    CURRENT_LANGUAGE = locale.getlocale()[0][:2]
except:
    # Fallback for old Windows versions.
    CURRENT_LANGUAGE = locale.getdefaultlocale()[0][:2]
try:
    t = gettext.translation('reg', LOCALE_PATH, languages=[CURRENT_LANGUAGE])
    _ = t.gettext
except:

    def _(message):
        return message

APPNAME = 'novelyst'
VERSION = ' @release'
APP = f'{APPNAME}.py'
START_UP_SCRIPT = 'run.pyw'
INI_FILE = f'{APPNAME}.ini'
INI_PATH = '/config/'
SAMPLE_PATH = 'sample/'
SUCCESS_MESSAGE = '''

$Appname is installed here:

$Apppath'''

SHORTCUT_MESSAGE = '''
Now you might want to create a shortcut on your desktop.  

On Windows, open the installation folder, hold down the Alt key on your keyboard, 
and then drag and drop "run.pyw" to your desktop.

On Linux, create a launcher on your desktop. With xfce for instance, the launcher's command may look like this:
python3 '$Apppath' %f
'''

SET_OPEN_CMD = f'''Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Classes\\.yw7]
@="yWriter7"
[HKEY_CURRENT_USER\Software\Classes\\yWriter7]
@="yWriter7 Project"
[HKEY_CURRENT_USER\Software\Classes\yWriter7\DefaultIcon]
@="$INSTALL\\\\icons\\\\yLogo64.ico"
[HKEY_CURRENT_USER\Software\Classes\yWriter7\shell\open\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\""
[HKEY_CURRENT_USER\Software\Classes\\.pwc]
@="nv4Collection"
[HKEY_CURRENT_USER\Software\Classes\\nv4Collection]
@="novelyst Collection"
[HKEY_CURRENT_USER\Software\Classes\\nv4Collection\DefaultIcon]
@="$INSTALL\\\\icons\\\\cLogo64.ico"

'''

RESET_ICON = f'''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\yWriter7\DefaultIcon]

'''

PLUGIN_OUTDATED = '''There are outdated plugins installed, which will be ignored by novelyst from now on. 
Please update your plugins.
'''

PLUGIN_WARNING = '''
There are plugins installed. 
You may want to run the Plugin Manager for compatibility check.
'''

SET_CONTEXT_MENU = f'''Windows Registry Editor Version 5.00

[HKEY_CURRENT_USER\Software\Classes\\.yw7]
@="yWriter7"
[HKEY_CURRENT_USER\Software\Classes\\yWriter7]
@="yWriter7 Project"
[-HKEY_CURRENT_USER\Software\Classes\yWriter7\shell\Open with novelyst]
[HKEY_CURRENT_USER\Software\Classes\\yWriter7\\shell\\{_('Open with novelyst')}]
[HKEY_CURRENT_USER\SOFTWARE\Classes\\yWriter7\\shell\\{_('Open with novelyst')}\\command]
@="\\"$PYTHON\\" \\"$SCRIPT\\" \\"%1\\""

'''

RESET_CONTEXT_MENU = f'''Windows Registry Editor Version 5.00

[-HKEY_CURRENT_USER\Software\Classes\yWriter7\shell\Open with novelyst]
[-HKEY_CURRENT_USER\Software\Classes\yWriter7\shell\{_('Open with novelyst')}]

'''

START_UP_CODE = f'''import {APPNAME}
{APPNAME}.main()
'''

root = tk.Tk()
processInfo = tk.Label(root, text='')
message = []


def make_context_menu(installPath):
    """Generate ".reg" files to extend the yWriter context menu."""

    def save_reg_file(filePath, template, mapping):
        """Save a registry file."""
        with open(filePath, 'w') as f:
            f.write(template.safe_substitute(mapping))
        output(f'Creating "{os.path.normpath(filePath)}"')

    python = sys.executable.replace('\\', '\\\\')
    instPath = installPath.replace('/', '\\\\')
    script = f'{instPath}\\\\{START_UP_SCRIPT}'
    mapping = dict(PYTHON=python, SCRIPT=script, INSTALL=instPath)
    save_reg_file(f'{installPath}/set_open_cmd.reg', Template(SET_OPEN_CMD), mapping)
    save_reg_file(f'{installPath}/add_context_menu.reg', Template(SET_CONTEXT_MENU), mapping)
    save_reg_file(f'{installPath}/rem_context_menu.reg', Template(RESET_CONTEXT_MENU), {})
    save_reg_file(f'{installPath}/reset_icon.reg', Template(RESET_ICON), {})


def output(text):
    message.append(text)
    processInfo.config(text=('\n').join(message))


def open_folder(installDir):
    """Open an installation folder window in the file manager.
    """
    try:
        os.startfile(os.path.normpath(installDir))
        # Windows
    except:
        try:
            os.system('xdg-open "%s"' % os.path.normpath(installDir))
            # Linux
        except:
            try:
                os.system('open "%s"' % os.path.normpath(installDir))
                # Mac
            except:
                pass


def install(pywriterPath):
    """Install the script."""

    #--- Create a general PyWriter installation directory, if necessary.
    os.makedirs(pywriterPath, exist_ok=True)
    installDir = f'{pywriterPath}{APPNAME}'
    cnfDir = f'{installDir}{INI_PATH}'
    if os.path.isfile(f'{installDir}/{APP}'):
        simpleUpdate = True
    else:
        simpleUpdate = False

    #--- Move an existing installation to the new place, if necessary.
    try:
        oldInst = os.getenv('APPDATA').replace('\\', '/')
        oldInstDir = f'{oldInst}/pyWriter/{APPNAME}'
        output(f'Moving "{oldInstDir}" to "{installDir}" ...')
        os.replace(oldInstDir, installDir)
    except:
        pass
    os.makedirs(cnfDir, exist_ok=True)

    #--- Delete the old version, but retain configuration, if any.
    # Do not remove the locale folder, because it may contain plugin data.
    # Do not remove the icons folder, because it may contain plugin data.
    with os.scandir(installDir) as files:
        for file in files:
            if not 'config' in file.name:
                try:
                    output(f'Removing "{file.name}" ...')
                    os.remove(file)
                except:
                    pass

    #--- Install the new version.
    output(f'Copying "{APP}" ...')
    copyfile(APP, f'{installDir}/{APP}')

    # Create a starter script.
    output(f'Creating starter script ...')
    with open(f'{installDir}/{START_UP_SCRIPT}', 'w', encoding='utf-8') as f:
        f.write(f'import {APPNAME}\n{APPNAME}.main()')

    # Install the localization files.
    output(f'Copying locale ...')
    copytree('locale', f'{installDir}/locale', dirs_exist_ok=True)

    # Install the icon files.
    output(f'Copying icons ...')
    copytree('icons', f'{installDir}/icons', dirs_exist_ok=True)
    for f in os.listdir(f'{installDir}/icons'):
        if not f.endswith('.png') and not f.endswith('.ico'):
            output(f'Deleting {installDir}/icons/{f} ...')
            os.remove(f'{installDir}/icons/{f}')

    #--- Make the scripts executable under Linux.
    st = os.stat(f'{installDir}/{APP}')
    os.chmod(f'{installDir}/{APP}', st.st_mode | stat.S_IEXEC)
    st = os.stat(f'{installDir}/{START_UP_SCRIPT}')
    os.chmod(f'{installDir}/{START_UP_SCRIPT}', st.st_mode | stat.S_IEXEC)

    #--- Install configuration files, if needed.
    try:
        with os.scandir(SAMPLE_PATH) as files:
            for file in files:
                if not os.path.isfile(f'{cnfDir}{file.name}'):
                    output(f'Copying "{file.name}" ...')
                    copyfile(f'{SAMPLE_PATH}{file.name}', f'{cnfDir}{file.name}')
                else:
                    output(f'Keeping "{file.name}".')
    except:
        pass

    #--- Create a plugin directory.

    pluginDir = f'{installDir}/plugin'
    output(f'Creating "{os.path.normpath(pluginDir)}" ...')
    os.makedirs(pluginDir, exist_ok=True)

    #--- Check plugins.
    files = glob.glob(f'{pluginDir}/*.py')
    if files:
        output(PLUGIN_WARNING)
    for filePath in files:
        moduleName = os.path.split(filePath)[1][:-3]
        if not moduleName.startswith('novelyst_'):
            messagebox.showwarning('Plugin check', PLUGIN_OUTDATED)
            break

    #--- Generate registry entries for the context menu (Windows only).
    if os.name == 'nt':
        make_context_menu(installDir)

    #--- Display a success message.
    mapping = {'Appname': APPNAME, 'Apppath': f'{installDir}/{START_UP_SCRIPT}'}
    output(Template(SUCCESS_MESSAGE).safe_substitute(mapping))

    #--- Ask for shortcut creation.
    if not simpleUpdate:
        output(Template(SHORTCUT_MESSAGE).safe_substitute(mapping))

    #--- Create a start-up script.
    if platform.system() == 'Windows':
        shebang = ''
    else:
        shebang = '#!/usr/bin/env python3\n'
    with open(f'{installDir}/{START_UP_SCRIPT}', 'w', encoding='utf-8') as f:
        f.write(f'{shebang}{START_UP_CODE}')


if __name__ == '__main__':
    scriptPath = os.path.abspath(sys.argv[0])
    scriptDir = os.path.dirname(scriptPath)
    os.chdir(scriptDir)

    # Open a tk window.
    root.geometry("800x700")
    root.title(f'Install {APPNAME}{VERSION}')
    header = tk.Label(root, text='')
    header.pack(padx=5, pady=5)

    # Prepare the messaging area.
    processInfo.pack(padx=5, pady=5)

    # Run the installation.
    homePath = str(Path.home()).replace('\\', '/')
    pywriterPath = f'{homePath}/.pywriter/'
    try:
        install(pywriterPath)
    except Exception as ex:
        output(str(ex))

    # Show options: open installation folders or quit.
    root.openButton = tk.Button(text="Open installation folder", command=lambda: open_folder(f'{homePath}/.pywriter/{APPNAME}'))
    root.openButton.config(height=1, width=30)
    root.openButton.pack(padx=5, pady=5)
    root.quitButton = tk.Button(text="Quit", command=quit)
    root.quitButton.config(height=1, width=30)
    root.quitButton.pack(padx=5, pady=5)
    root.mainloop()
