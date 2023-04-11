#!/usr/bin/python3
"""A novel organizer for writers. 

Version @release
Requires Python 3.6+
Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
"""
import os
import sys
from pathlib import Path
from pywriter.pywriter_globals import *
from pywriter.config.configuration import Configuration
from novelystlib.view_controller.novelyst_tk import NovelystTk

APPNAME = 'novelyst'
SETTINGS = dict(
    yw_last_open='',
    root_geometry='1200x800',
    gui_theme='',
    button_context_menu='<Button-3>',
    middle_frame_width=400,
    right_frame_width=350,
    prop_win_geometry='299x716+260+260',
    color_chapter='green',
    color_unused='gray',
    color_notes='blue',
    color_todo='red',
    color_major='navy',
    color_minor='cornflower blue',
    color_outline='dark orchid',
    color_draft='black',
    color_1st_edit='DarkGoldenrod4',
    color_2nd_edit='DarkGoldenrod3',
    color_done='DarkGoldenrod2',
    color_staged='black',
    color_descriptive='light sea green',
    color_explaining='brown',
    color_summarizing='magenta',
    color_behind_schedule='tomato',
    color_before_schedule='sea green',
    color_on_schedule='black',
    color_locked_bg='dim gray',
    color_locked_fg='light gray',
    color_modified_bg='goldenrod1',
    color_modified_fg='maroon',
    color_text_bg='white',
    color_text_fg='black',
    color_notes_bg='lemon chiffon',
    color_notes_fg='black',
    coloring_mode='',
    title_width=400,
    ps_width=50,
    wc_width=50,
    status_width=100,
    mode_width=100,
    nt_width=20,
    vp_width=100,
    tags_width=100,
    pacing_width=40,
    date_width=70,
    time_width=40,
    duration_width=55,
    arcs_width=55,
    plot_width=300,
    column_order='wc;vp;sy;st;nt;dt;tm;dr;tg;po;ac;pt;ar'
)
OPTIONS = dict(
    show_contents=True,
    show_properties=True,
    show_markup=False,
    show_language_settings=False,
    show_auto_numbering=False,
    show_renamings=False,
    show_writing_progress=False,
    show_arcs=False,
    show_date_time=False,
    show_action_reaction=False,
    show_relationships=False,
    show_cr_bio=True,
    show_cr_goals=True,
    detach_prop_win=False,
    clean_up_yw=False,
)


def main():
    #--- Set up the directories for configuration and temporary files.
    try:
        homeDir = str(Path.home()).replace('\\', '/')
        installDir = f'{homeDir}/.pywriter/{APPNAME}'
    except:
        installDir = '.'
    os.makedirs(installDir, exist_ok=True)
    configDir = f'{installDir}/config'
    os.makedirs(configDir, exist_ok=True)
    tempDir = f'{installDir}/temp'
    os.makedirs(tempDir, exist_ok=True)

    #--- Load configuration.
    iniFile = f'{configDir}/{APPNAME}.ini'
    configuration = Configuration(SETTINGS, OPTIONS)
    configuration.read(iniFile)
    kwargs = {}
    kwargs.update(configuration.settings)
    kwargs.update(configuration.options)

    #--- Get initial project path.
    try:
        sourcePath = sys.argv[1]
    except:
        sourcePath = ''
    if not sourcePath or not os.path.isfile(sourcePath):
        sourcePath = kwargs['yw_last_open']

    #--- Instantiate the app object.
    app = NovelystTk('novelyst @release', tempDir, **kwargs)
    app.open_project(sourcePath)
    app.start()

    #--- Save project specific configuration
    for keyword in app.kwargs:
        if keyword in configuration.options:
            configuration.options[keyword] = app.kwargs[keyword]
        elif keyword in configuration.settings:
            configuration.settings[keyword] = app.kwargs[keyword]
    configuration.write(iniFile)

    #--- Delete the temporary files.
    # Note: Do not remove the temp directory itself,
    # because other novelyst instances might be running and using it.
    # However, temporary files of other running instances are deleted
    # if not protected e.g. by a read-only flag.
    for file in os.scandir(tempDir):
        try:
            os.remove(file)
        except:
            pass


if __name__ == '__main__':
    main()
