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
from maya import OpenMayaUI as OpenMayaUI
from maya.OpenMayaUI import MQtUtil
from maya.app.general.mayaMixin import MayaQDockWidget
try:
    import pysideuic
    from shiboken import wrapInstance

except ImportError:
    import pyside2uic as pysideuic
    from shiboken2 import wrapInstance


# --------------------------------------------------------------------------------------------------
# GLOBALS VARIABLES
# --------------------------------------------------------------------------------------------------

__version__ = '0.1.0'
toolBoxWin = None

# --------------------------------------------------------------------------------------------------
def maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(long(main_window_ptr), QtWidgets.QWidget)

# Style
scriptDir = os.path.dirname(os.path.realpath(__file__))
stylePath = os.sep.join([scriptDir, 'css', 'dark.stylesheet'])

with open(stylePath, 'r') as f:
    styleSheet = f.read()
    f.close()



class ToolboxUI(MayaQWidgetDockableMixin, QtWidgets.QMainWindow):

    def __init__(self, parent):
        super(ToolboxUI, self).__init__(parent=parent)

        self.title = ' - '.join(['Toolbox', __version__])
        self.setObjectName('Toolbox')

        self.setWindowTitle(self.title)

        self.setWindowIcon(QtGui.QIcon(os.sep.join([scriptDir, 'icons', 'svg', 'tools.svg'])))

        self.setMinimumSize(150, 400)
        self.resize(150, 400)

        self.tool = {}

        self.createLayouts()
        self.createWidgets()
        self.createButtons()
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

        self.refreshBtn = QtWidgets.QPushButton()
        self.refreshBtn.setText('Refresh')

    def deleteCurrentButtons(self):
        for i in reversed(range(self.buttonLayout.count())):
            self.buttonLayout.itemAt(i).widget().deleteLater()

    def createButtons(self):

        self.deleteCurrentButtons()

        self.tool = toolboxLib.ToolBoxLayout(os.sep.join([scriptDir, 'data', 'toolbox_data.json']))

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
        self.mainLayout.addWidget(self.refreshBtn)
        self.mainLayout.addWidget(self.scrollArea)

        self.main_widget.setLayout(self.mainLayout)
        self.setCentralWidget(self.main_widget)

    def createConnections(self):
        self.settingsBtn.clicked.connect(self.showToolboxManager)
        self.refreshBtn.clicked.connect(self.createButtons)

    def showToolboxManager(self):

        self.toolboxManagerUI.show()

    def dockCloseEventTriggered(self):
        self.deleteInstances()

    # Delete any instances of this class
    def deleteInstances(self):
        mayaMainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
        mayaMainWindow = wrapInstance(long(mayaMainWindowPtr), QtWidgets.QMainWindow)
        # Important that it's QMainWindow, and not QWidget/QDialog

        # Go through main window's children to find any previous instances
        for obj in mayaMainWindow.children():
            if type(obj) == MayaQDockWidget:
                # if obj.widget().__class__ == self.__class__:
                # Alternatively we can check with this, but it will fail if we re-evaluate the class
                print obj.widget().objectName()
                if obj.widget().objectName() == self.objectName():  # Compare object names
                    # If they share the same name then remove it
                    print 'Deleting instance {0}'.format(obj)
                    mayaMainWindow.removeDockWidget(obj)
                    # This will remove from right-click menu,
                    # but won't actually delete it! ( still under mainWindow.children() )
                    # Delete it for good
                    obj.setParent(None)
                    obj.deleteLater()


def launch():
    ''' Def to call to launch tool in maya '''

    global toolBoxWin

    mayaWin = maya_main_window()
    toolBoxWin = ToolboxUI(mayaWin)
    toolBoxWin.deleteInstances()
    toolBoxWin.show(dockable=True, area='left')
