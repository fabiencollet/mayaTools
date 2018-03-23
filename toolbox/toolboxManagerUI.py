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
import pprint

from lib import toolboxLib
reload(toolboxLib)

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

        self.tool = toolboxLib.ToolBoxLayout(os.sep.join([scriptDir, 'data', 'toolbox_data.json']))


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

        self.btnRefreshContent = QtWidgets.QPushButton()
        self.btnRefreshContent.setText('Refresh')

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
        self.contentLayout.addWidget(self.btnRefreshContent)

        # Add to main layout
        self.mainLayout.addLayout(self.categoryLayout)
        self.mainLayout.addLayout(self.scriptLayout)
        self.mainLayout.addLayout(self.contentLayout)

        self.setLayout(self.mainLayout)

    def createConnections(self):
        self.btnRefreshContent.clicked.connect(self.refreshContent)
        self.btnSaveContent.clicked.connect(self.printData)

        self.btnAddCategory.clicked.connect(self.addCategory)
        self.btnAddScript.clicked.connect(self.addScript)

        self.listCategory.itemActivated.connect(self.getScripts)
        self.listScript.itemActivated.connect(self.getScriptInfo)

    def refreshContent(self):

        self.listCategory.clear()
        self.listScript.clear()
        self.leftScript.clear()
        self.middleScript.clear()
        self.rightScript.clear()

        for category in self.tool.toolbox_data:
            self.listCategory.addItem(category)


    def getScripts(self):
        category = self.listCategory.currentItem().text()
        self.listScript.clear()
        self.leftScript.clear()
        self.middleScript.clear()
        self.rightScript.clear()

        for script in self.tool.toolbox_data[category]:
            self.listScript.addItem(script)


    def getScriptInfo(self):
        category = self.listCategory.currentItem().text()
        script = self.listScript.currentItem().text()
        self.leftScript.clear()
        self.middleScript.clear()
        self.rightScript.clear()


        left_click_command = self.tool.toolbox_data[category][script]['left_click_command']
        middle_click_command = self.tool.toolbox_data[category][script]['middle_click_command']
        right_click_command = self.tool.toolbox_data[category][script]['right_click_command']

        self.leftScript.setText(left_click_command)
        self.middleScript.setText(middle_click_command)
        self.rightScript.setText(right_click_command)

    def addCategory(self):

        category, ok = QtWidgets.QInputDialog.getText(self, 'Text Input Dialog', 'New category:')
        if ok:
            self.listCategory.addItem(category)
            self.tool.toolbox_data[category]= {}

    def addScript(self):

        category = self.listCategory.currentItem().text()

        script, ok = QtWidgets.QInputDialog.getText(self, 'Text Input Dialog', 'New script:')
        if ok:
            self.listScript.addItem(script)
            self.tool.toolbox_data[category][script] = {"description": "",
                                                        "version": "",
                                                        "icon": "",
                                                        "helpMessage": "",
                                                        "helpPicture": "",
                                                        "left_click_command": "",
                                                        "middle_click_command": "",
                                                        "right_click_command": "",
                                                        "double_clickCommand": ""}

    def printData(self):
        left_script = self.leftScript.toPlainText()
        middle_script = self.middleScript.toPlainText()
        right_script = self.rightScript.toPlainText()

        category = self.listCategory.currentItem().text()
        script = self.listScript.currentItem().text()

        self.tool.toolbox_data[category][script]['left_click_command'] = left_script
        self.tool.toolbox_data[category][script]['middle_click_command'] = middle_script
        self.tool.toolbox_data[category][script]['right_click_command'] = right_script

        # pprint.pprint(self.tool.toolbox_data)

        self.tool.saveFile()

def launch():
    ''' Def to call to launch tool in maya '''

    global toolboxManagerWin

    if toolboxManagerWin:
        toolboxManagerWin.close()

    toolboxManagerWin = ToolboxManagerUI()
    toolboxManagerWin.show()
