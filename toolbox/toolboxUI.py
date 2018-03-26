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

import maya.cmds as mc
import toolboxManagerUI
reload(toolboxManagerUI)
import maya.OpenMayaUI as omui
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

try:
    import pysideuic
    from shiboken import wrapInstance

except ImportError:
    import pyside2uic as pysideuic
    from shiboken2 import wrapInstance


def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)


# Style
scriptDir = os.path.dirname(os.path.realpath(__file__))
stylePath = os.sep.join([scriptDir, 'css', 'dark.stylesheet'])

with open(stylePath, 'r') as f:
    styleSheet = f.read()
    f.close()

toolBoxWin = None


class ToolboxUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    def __init__(self, parent):
        super(ToolboxUI, self).__init__(parent=parent)

        self.title = ' - '.join(['Toolbox', _version_])
        self.setObjectName('Toolbox')

        self.setWindowTitle(self.title)

        self.setWindowIcon(QtGui.QIcon(os.sep.join([scriptDir, 'icons', 'svg', 'tools.svg'])))

        self.setMinimumSize(150, 400)
        self.resize(150, 400)

        self.tool = toolboxLib.ToolBoxLayout(os.sep.join([scriptDir, 'data', 'toolbox_data.json']))

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

        self.scrollArea = QtWidgets.QScrollArea()
        self.buttonGrpWidget = QtWidgets.QWidget()

        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(True)

        self.buttonGrpWidget.setLayout(self.buttonLayout)
        self.scrollArea.setWidget(self.buttonGrpWidget)

        self.main_widget = QtWidgets.QWidget()

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
        self.mainLayout.addWidget(self.scrollArea)

        self.main_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.main_widget)

    def createConnections(self):
        self.settingsBtn.clicked.connect(self.showToolboxManager)

    def showToolboxManager(self):

        self.toolboxManagerUI.show()


def launch():
    ''' Def to call to launch tool in maya '''

    global toolBoxWin

    if toolBoxWin:
        print toolBoxWin.objectName()

        mc.deleteUI(toolBoxWin.objectName())

    mayaWin = maya_main_window()
    toolBoxWin = ToolboxUI(mayaWin)
    toolBoxWin.show(dockable=True, area='left')