"""Provide a tkinter based class for viewing and editing project notes.

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""
from novelystlib.view_controller.right_frame.basic_view import BasicView


class ProjectnoteView(BasicView):
    """Class for viewing and editing project notes.
       
    """

    def _create_frames(self):
        """Template method for creating the frames in the right pane."""
        self._create_index_card()
        self._create_button_bar()
