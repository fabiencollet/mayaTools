#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`testWidget`
===================================

.. module:: testWidget
   :platform: Windows
   :synopsis: Custom toolbox
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.08.23

'''

try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from lib.Qt import QtWidgets, QtGui, QtCore

testWin = None


class TestUI(QtWidgets.QWidget):
    def __init__(self):
        super(TestUI, self).__init__()

        self.title = 'Test Widget'
        self.setWindowTitle(self.title)

        self.setMinimumSize(1, 1)
        self.resize(400, 400)

        self.createLayouts()
        self.createWidgets()
        self.createHierarchy()
        self.createConnections()

    def createLayouts(self):
        # Create Main Layout
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0,0,0,0)
        self.main_layout.setSpacing(0)


    def createWidgets(self):
        print 'Widget creation'

        # Add widget here
        self.myWidget = CollapseWidget()
        self.myWidget.setLabel('Modeling')

        self.myWidget2 = CollapseWidget()
        self.myWidget2.setLabel('Rigging')

        self.myWidget3 = CollapseWidget()
        self.myWidget3.setLabel('Lighting')

        for btn in ['testqsd1', 'test2', 'tesqdqdq dqt3', 'testqsd qdq4', 'test5']:

            button = QtWidgets.QPushButton()
            button.setText(btn)
            self.myWidget.addWidget(button)

            button = QtWidgets.QPushButton()
            button.setText(btn)
            self.myWidget2.addWidget(button)

            button = QtWidgets.QPushButton()
            button.setText(btn)
            self.myWidget3.addWidget(button)

            test = QtWidgets.QLineEdit()
            self.myWidget3.addWidget(test)


    def createHierarchy(self):

        self.main_layout.addWidget(self.myWidget)
        self.main_layout.addWidget(self.myWidget2)
        self.main_layout.addWidget(self.myWidget3)
        self.setLayout(self.main_layout)

    def createConnections(self):
        print 'Connections creation'
        # Add Connections here


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

        # Hierarchy
        self.main_layout.addWidget(self.button)
        self.main_layout.addLayout(self.content_layout)
        self.setLayout(self.main_layout)

        # Connections
        self.button.setCheckable(True)
        self.button.setChecked(False)
        self.button.toggled.connect(self.hideContent)

    def hideContent(self):
        child_item = self.content_layout.count()
        for i in range(child_item):
            if self.button.isChecked():
                self.content_layout.itemAt(i).widget().setVisible(True)
            else:
                self.content_layout.itemAt(i).widget().setVisible(False)

    def setLabel(self, label):
        self.label = label
        self.button.setText(self.label)

    def addWidget(self, widget):
        self.content_layout.addWidget(widget)
        widget.setVisible(False)


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
