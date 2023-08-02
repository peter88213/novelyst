"""Provide a class for a history list for the novelyst tree. 

Copyright (c) 2023 Peter Triesberger
For further information see https://github.com/peter88213/novelyst
License: GNU GPLv3 (https://www.gnu.org/licenses/gpl-3.0.en.html)
"""


class HistoryList:

    def __init__(self):
        self.historyList = []
        self.pointer = None

    def append_node(self, element):
        try:
            del self.historyList[self.pointer:]
        finally:
            self.historyList.append(element)
            self.pointer = len(self.historyList) - 1

    def go_forward(self):
        if self.pointer + 1 < len(self.historyList):
            self.pointer += 1
        return self.historyList[self.pointer]

    def go_back(self):
        if self.pointer > 0:
            self.pointer -= 1
        return self.historyList[self.pointer]

    def get_node(self):
        return self.historyList[self.pointer]

    def remove_node(self, node):
        if node in self.historyList:
            self.historyList = [x for x in self.historyList if x != node]
            self.pointer = len(self.historyList) - 1
