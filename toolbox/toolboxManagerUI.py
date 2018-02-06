#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`toolboxManagerUI`
===================================

.. module:: toolboxManagerUI
   :platform: Windows
   :synopsis: Toolbox manager
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.08.23

'''

_version_ = '1.0.0'

try:
    from PySide2 import QtWidgets
except:
    from ..lib.Qt import QtWidgets
import os

toolboxManagerWin = None

# Style
scriptDir = os.path.dirname(os.path.realpath(__file__))
stylePath = os.sep.join([scriptDir, 'css', 'dark.stylesheet'])

with open(stylePath, 'r') as f:
    styleSheet = f.read()
    f.close()


class ToolboxManagerUI(QtWidgets.QWidget):

    def __init__(self):
        super(ToolboxManagerUI, self).__init__()

        self.title = ' - '.join(['Toolbox Manager', _version_])
        self.setWindowTitle(self.title)

        self.setStyleSheet(styleSheet)

        self.setMinimumSize(750, 500)
        self.resize(750, 500)

        self.createLayouts()
        self.createWidgets()
        self.createHierarchy()
        self.createConnections()

    def createLayouts(self):
        # Create Main Layout
        self.mainLayout = QtWidgets.QHBoxLayout()

        self.categoryLayout = QtWidgets.QVBoxLayout()
        self.scriptLayout = QtWidgets.QVBoxLayout()
        self.contentLayout = QtWidgets.QVBoxLayout()

    def createWidgets(self):

        # Category part
        self.labelCategory = QtWidgets.QLabel()
        self.labelCategory.setText('Category')

        self.listCategory = QtWidgets.QListWidget()
        self.btnAddCategory = QtWidgets.QPushButton()
        self.btnAddCategory.setText('Add')
        self.btnRemoveCategory = QtWidgets.QPushButton()
        self.btnRemoveCategory.setText('Remove')

        # Script part
        self.labelScript = QtWidgets.QLabel()
        self.labelScript.setText('Scripts')
        self.listScript = QtWidgets.QListWidget()

        self.btnAddScript = QtWidgets.QPushButton()
        self.btnAddScript.setText('Add')
        self.btnRemoveScript = QtWidgets.QPushButton()
        self.btnRemoveScript.setText('Remove')

        # Content part
        self.labelLeftContent = QtWidgets.QLabel()
        self.labelLeftContent.setText('Left click :')
        self.leftScript = QtWidgets.QTextEdit()

        self.labelMiddleContent = QtWidgets.QLabel()
        self.labelMiddleContent.setText('Middle click :')
        self.middleScript = QtWidgets.QTextEdit()

        self.labelRightContent = QtWidgets.QLabel()
        self.labelRightContent.setText('Right click :')
        self.rightScript = QtWidgets.QTextEdit()

        self.btnSaveContent = QtWidgets.QPushButton()
        self.btnSaveContent.setText('Save')

    def createHierarchy(self):

        self.categoryLayout.addWidget(self.labelCategory)
        self.categoryLayout.addWidget(self.listCategory)
        self.categoryLayout.addWidget(self.btnAddCategory)
        self.categoryLayout.addWidget(self.btnRemoveCategory)

        self.scriptLayout.addWidget(self.labelScript)
        self.scriptLayout.addWidget(self.listScript)
        self.scriptLayout.addWidget(self.btnAddScript)
        self.scriptLayout.addWidget(self.btnRemoveScript)

        self.contentLayout.addWidget(self.labelLeftContent)
        self.contentLayout.addWidget(self.leftScript)
        self.contentLayout.addWidget(self.labelMiddleContent)
        self.contentLayout.addWidget(self.middleScript)
        self.contentLayout.addWidget(self.labelRightContent)
        self.contentLayout.addWidget(self.rightScript)
        self.contentLayout.addWidget(self.btnSaveContent)

        # Add to main layout
        self.mainLayout.addLayout(self.categoryLayout)
        self.mainLayout.addLayout(self.scriptLayout)
        self.mainLayout.addLayout(self.contentLayout)

        self.setLayout(self.mainLayout)

    def createConnections(self):
        print 'toolBox manager create connection'


def launch():
    ''' Def to call to launch tool in maya '''

    global toolboxManagerWin

    if toolboxManagerWin:
        toolboxManagerWin.close()

    toolboxManagerWin = ToolboxManagerUI()
    toolboxManagerWin.show()