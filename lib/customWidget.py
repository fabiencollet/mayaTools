#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`customWidget`
===================================

.. module:: customWidget
   :platform: Windows
   :synopsis: Custom Widget
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.08.23

'''

try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from Qt import QtWidgets, QtGui, QtCore

from random import randint
import os

SCRIPT_PATH = os.path.dirname(os.path.realpath(__file__))


class Button(QtWidgets.QWidget):
    def __init__(self):
        super(Button, self).__init__()

        self.initUI()

        self.x = 0
        self.y = 0
        self.w = 10
        self.h = 10
        self.collapse = True
        self.hover = False

    def initUI(self):

        self.setMinimumSize(1, 30)
        self.label = ''

    def setLabel(self, label):

        self.label = label

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(event, qp)
        qp.end()

    def drawWidget(self, event, qp):

        size = self.size()
        w = size.width()
        h = size.height()

        if self.hover:
            qp.setPen(QtGui.QColor(0, 255, 255))
            qp.setBrush(QtGui.QColor(0, 255, 255))
        else:
            qp.setPen(QtGui.QColor(0, 255, 255))
            qp.setBrush(QtGui.QColor(0, 255, 255))


        self.btn_rect = qp.drawRect(self.x, self.y, self.w, self.h)

    def mousePressEvent(self, event):

        size = self.size()
        w = size.width()
        h = size.height()

        x = event.x()
        y = event.y()

        if x > 0 and x < self.w and y > 0 and y < self.h:
            if self.collapse:
                self.w = w
                self.h = h
                self.collapse = False
            else:
                self.w = 10
                self.h = 10
                self.collapse = True

        self.update()

    def changeEvent(self, event):
        if self.underMouse():
            print 'Under Mouse'


class CollapseWidget(QtWidgets.QWidget):
    def __init__(self):
        super(CollapseWidget, self).__init__()

        # init
        self.main_layout = QtWidgets.QVBoxLayout()
        self.content_layout = QtWidgets.QVBoxLayout()
        self.label = ''
        self.button = QtWidgets.QPushButton()
        rgb = (randint(0,255), randint(0,255), randint(0,255))
        rgbHover = (rgb[0]+20, rgb[1]+20, rgb[2]+20)

        # Hierarchy
        self.main_layout.addWidget(self.button)
        self.main_layout.addLayout(self.content_layout)
        self.setLayout(self.main_layout)

        # Connections
        self.button.setCheckable(True)
        self.button.setChecked(False)
        self.button.toggled.connect(self.hideContent)

        self.icon_path_open = os.sep.join([SCRIPT_PATH, 'icons', 'svg', 'chevron-down.svg'])
        self.icon_path_closed = os.sep.join([SCRIPT_PATH, 'icons', 'svg', 'chevron-right.svg'])

        self.button.setStyleSheet("background-color:grey;")

        self.setIcon(self.icon_path_closed)

        self.button.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.button.setIconSize(QtCore.QSize(16, 16))

    def setIcon(self, path):

        ico = QtGui.QIcon(path)
        self.button.setIcon(ico)

    def hideContent(self):
        child_item = self.content_layout.count()
        for i in range(child_item):
            if self.button.isChecked():
                self.setIcon(self.icon_path_open)
                self.content_layout.itemAt(i).widget().setVisible(True)
            else:
                self.setIcon(self.icon_path_closed)
                self.content_layout.itemAt(i).widget().setVisible(False)

    def setLabel(self, label):
        self.label = label
        self.button.setText(self.label)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)
        widget.setVisible(False)


class CustomButton(QtWidgets.QPushButton):

    def __init__(self):
        super(CustomButton, self).__init__()
        self.doubleClickTriggered = False
        self.left_click_command = ''
        self.middle_click_command = ''
        self.right_click_command = ''
        self.doubleClickCommand = ''

    def setLeftClickCommand(self, script):
        self.left_click_command = compile(script, '<string>', 'exec')

    def setMiddleClickCommand(self, script):
        self.middle_click_command= compile(script, '<string>', 'exec')

    def setRightClickCommand(self, script):
        self.right_click_command = compile(script, '<string>', 'exec')

    def setDoubleClickCommand(self, script):
        self.doubleClickCommand = compile(script, '<string>', 'exec')

    def mouseDoubleClickEvent(self, event):
        if event.button() != QtCore.Qt.MouseButton.LeftButton:
            return False

        self.doubleClickTriggered = True

        if self.doubleClickCommand:
            exec self.doubleClickCommand

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            if self.left_click_command:
                exec self.left_click_command

        if event.button() == QtCore.Qt.MouseButton.MiddleButton:
            if self.middle_click_command:
                exec self.middle_click_command

        if event.button() == QtCore.Qt.MouseButton.RightButton:
            if self.right_click_command:
                exec self.right_click_command


class RoundButton(QtWidgets.QToolButton):
    def __init__(self):
        super(RoundButton, self).__init__()

        self.x = 0
        self.y = 0
        self.radius = 10

        # self.setMinimumSize(1, 30)
        self.label = ''

        self.setMouseTracking(True)

    def setLabel(self, label):

        self.label = label

    def paintEvent(self, event):

        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(event, qp)
        qp.end()

    def drawWidget(self, event, qp):

        size = self.size()
        w = size.width()
        h = size.height()

        qp.setPen(QtGui.QColor(0, 255, 255))
        qp.setBrush(QtGui.QColor(0, 255, 255))


        self.btn_rect = qp.drawEllipse(self.x, self.y, self.radius, self.radius)

    def mouseMoveEvent(self, event):
        print event.type()

def launch():
    ''' Def to call to launch tool in maya '''

    global testWin

    if testWin:
        testWin.close()

    testWin = TestUI()
    testWin.show()
