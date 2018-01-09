#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`toolboxUI`
===================================

.. module:: toolboxUI
   :platform: Windows
   :synopsis: Custom toolbox
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.08.23

'''

_version_ = '1.0.0'
_author_ = 'Fabien Collet'

import toolboxManagerUI
try:
    from PySide2 import QtWidgets, QtCore
except:
    from ..lib.Qt import QtWidgets, QtCore

from lib import toolboxLib
from ..lib import customWidget
reload(customWidget)
reload(toolboxLib)
import os

scriptDir = os.path.dirname(__file__)
stylePath = os.sep.join([scriptDir, 'css', 'dark.stylesheet'])

with open(stylePath, 'r') as f:
    styleSheet = f.read()
    f.close()

toolboxWin = None


class ToolboxUI(QtWidgets.QWidget):

    def __init__(self):
        super(ToolboxUI, self).__init__()

        self.title = ' - '.join(['Toolbox', _version_])
        self.setWindowTitle(self.title)

        self.setMinimumSize(150, 400)
        self.resize(150, 400)

        self.tool = toolboxLib.ToolBoxLayout(
            '/homes/fabco/maya/2016.5/scripts/myScript/mayaTools/toolbox/data/toolbox_fab.json')

        self.createLayouts()
        self.createWidgets()
        self.createHierarchy()
        self.createConnections()

        self.toolboxManagerUI = toolboxManagerUI.ToolboxManagerUI()

        self.setStyleSheet(styleSheet)

    def createLayouts(self):
        # Create Main Layout
        self.mainLayout = QtWidgets.QVBoxLayout()
        # Create Button Layout
        self.buttonLayout = QtWidgets.QGridLayout()

    def createWidgets(self):

        self.settingsBtn = QtWidgets.QPushButton()
        self.settingsBtn.setText('Settings')

        for category in self.tool.getCategories():

            collapse_widget = customWidget.CollapseWidget()
            collapse_widget.setLabel(category)

            for script in self.tool.getScriptInCategory(category):
                button = customWidget.CustomButton()
                button.setText(script)
                collapse_widget.addWidget(button)

                version, description, icon, helpMessage, helpPicture, clickCommand, double_clickCommand = self.tool.getScriptInfo(
                    category, script)

                button.setClickCommand(clickCommand)
                button.setDoubleClickCommand(double_clickCommand)

            self.buttonLayout.addWidget(collapse_widget)

    def createHierarchy(self):

        self.mainLayout.addWidget(self.settingsBtn)
        self.mainLayout.addLayout(self.buttonLayout)

        self.setLayout(self.mainLayout)

    def createConnections(self):
        self.settingsBtn.clicked.connect(self.showToolboxManager)

    def showToolboxManager(self):

        self.toolboxManagerUI.show()
        print self.toolboxManagerUI.textScript.toPlainText()


def launch():
    ''' Def to call to launch tool in maya '''

    global toolboxWin

    if toolboxWin:
        toolboxWin.close()

    toolboxWin = ToolboxUI()
    toolboxWin.show()