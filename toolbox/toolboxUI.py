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
    from PySide2 import QtWidgets, QtCore, QtGui
except:
    from ..lib.Qt import QtWidgets, QtCore, QtGui

from lib import toolboxLib
from ..lib import customWidget
reload(customWidget)
reload(toolboxLib)
import os
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

scriptDir = os.path.dirname(os.path.realpath(__file__))
stylePath = os.sep.join([scriptDir, 'css', 'dark.stylesheet'])

with open(stylePath, 'r') as f:
    styleSheet = f.read()
    f.close()

toolBoxWin = None


class ToolBoxMain(QtWidgets.QMainWindow):

    def __init__(self):
        super(ToolBoxMain, self).__init__()

        self.toolBox = ToolboxUI()

        self.setCentralWidget(self.toolBox)


class DockWidget(QtWidgets.QDockWidget):

    def __init__(self):
        super(DockWidget, self).__init__()

        self.toolBox_main = ToolBoxMain()

        self.setParent(self.toolBox_main)

        self.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)


class ToolboxUI(MayaQWidgetDockableMixin, QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(ToolboxUI, self).__init__(parent=parent)

        self.title = ' - '.join(['Toolbox', _version_])
        self.setWindowTitle(self.title)

        self.setWindowIcon(QtGui.QIcon('/homes/fabco/maya/2016.5/scripts/myScript/mayaTools/toolbox/icons/svg/tools.svg'))

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

                version, description, icon, helpMessage, helpPicture, left_click_command, middle_click_command, right_click_command, double_clickCommand = self.tool.getScriptInfo(
                    category, script)

                button.setLeftClickCommand(left_click_command)
                button.setMiddleClickCommand(middle_click_command)
                button.setRightClickCommand(right_click_command)

                button.setDoubleClickCommand(double_clickCommand)

                # Set Icon
                if icon:
                    ico = QtGui.QIcon(os.sep.join([scriptDir, 'icons', icon]))
                    button.setIcon(ico)
                    button.setIconSize(QtCore.QSize(24, 24))
                    button.setLayoutDirection(QtCore.Qt.LeftToRight)

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

    global toolBoxWin

    if toolBoxWin:
        toolBoxWin.close()

    toolBoxWin = ToolboxUI()
    toolBoxWin.show(dockable=True)