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
from PySide2 import QtWidgets
import os


toolboxWin = None

class ToolboxUI(QtWidgets.QWidget):

    def __init__(self):
        super(ToolboxUI, self).__init__()

        self.title = ' - '.join(['Toolbox', _version_])
        self.setWindowTitle(self.title)

        self.setMinimumSize(150, 400)
        self.resize(150, 400)

        self.createLayouts()
        self.createWidgets()
        self.createHierarchy()
        self.createConnections()

        self.toolboxManagerUI = toolboxManagerUI.ToolboxManagerUI()

    def createLayouts(self):
        # Create Main Layout
        self.mainLayout = QtWidgets.QVBoxLayout()
        # Create Button Layout
        self.buttonLayout = QtWidgets.QGridLayout()

    def createWidgets(self):

        self.settingsBtn = QtWidgets.QPushButton()
        self.settingsBtn.setText('Settings')

        listScripts = ['fre', 'goij', 'ert',
                       'olpm', 'orie', 'ploi',
                       'msoe', 'ilpo', 'edf']

        for script in listScripts:
            btnWidget = QtWidgets.QPushButton()
            btnWidget.setText(script)

            self.buttonLayout.addWidget(btnWidget)

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