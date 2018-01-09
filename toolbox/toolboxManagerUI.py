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
_author_ = 'Fabien Collet'

from ..lib.Qt import QtWidgets


toolboxManagerWin = None

class ToolboxManagerUI(QtWidgets.QWidget):

    def __init__(self):
        super(ToolboxManagerUI, self).__init__()

        self.title = ' - '.join(['Toolbox Manager', _version_, _author_])
        self.setWindowTitle(self.title)

        self.setMinimumSize(300, 400)
        self.resize(300, 400)

        self.createLayouts()
        self.createWidgets()
        self.createHierarchy()
        self.createConnections()

    def createLayouts(self):
        # Create Main Layout
        self.mainLayout = QtWidgets.QHBoxLayout()
        # Create Button Layout
        self.buttonLayout = QtWidgets.QGridLayout()

    def createWidgets(self):

        self.listScript = QtWidgets.QListWidget()
        self.textScript = QtWidgets.QTextEdit()

    def createHierarchy(self):

        self.mainLayout.addWidget(self.listScript)
        self.mainLayout.addWidget(self.textScript)

        self.setLayout(self.mainLayout)

    def createConnections(self):
        print 'testtest'


def launch():
    ''' Def to call to launch tool in maya '''

    global toolboxManagerWin

    if toolboxManagerWin:
        toolboxManagerWin.close()

    toolboxManagerWin = ToolboxManagerUI()
    toolboxManagerWin.show()