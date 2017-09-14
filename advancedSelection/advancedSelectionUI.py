#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`advancedSelectionUI`
===================================

.. module:: advancedSelectionUI
   :platform: Windows
   :synopsis: advanced maya selection interface
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.08.23

'''

try:
    from PySide2 import QtWidgets, QtCore
except:
    from mayaTools.lib.Qt import QtWidgets, QtCore, QtGui
import maya.cmds as mc

advancedSelectionWin = None


class Selector(QtWidgets.QGroupBox):

    def __init__(self):
        super(Selector, self).__init__()

        self.mainLayout = QtWidgets.QVBoxLayout()

        self.operationLayout = QtWidgets.QHBoxLayout()
        self.operationLayout.setSpacing(0)
        self.headerLayout = QtWidgets.QHBoxLayout()

        self.contentLayout = QtWidgets.QVBoxLayout()

        self.bottomLayout = QtWidgets.QHBoxLayout()

        self.plusBtn = QtWidgets.QPushButton('+')
        self.minusBtn = QtWidgets.QPushButton('-')
        self.difBtn = QtWidgets.QPushButton('%')

        self.blueBtn = 'background-color:rgb(48, 127, 183);'
        self.greyBtn = 'background-color:rgb(100, 100, 100);'
        self.greenBtn = 'background-color:rgb(127, 183, 49);'
        self.redBtn = 'background-color:rgb(224, 78, 62);'

        self.closeBtn = QtWidgets.QPushButton('Delete')

        self.testBtn = QtWidgets.QPushButton('Test')

        self.operationLayout.addWidget(self.plusBtn)
        self.operationLayout.addWidget(self.minusBtn)
        self.operationLayout.addWidget(self.difBtn)

        self.headerLayout.addLayout(self.operationLayout)
        self.headerLayout.addWidget(self.closeBtn)

        self.bottomLayout.addWidget(self.testBtn)

        self.mainLayout.addLayout(self.headerLayout)
        self.mainLayout.addLayout(self.contentLayout)
        self.mainLayout.addLayout(self.bottomLayout)

        self.setLayout(self.mainLayout)

        self.closeBtn.clicked.connect(self.deleteGroupBox)

        self.mode = ''

        self.activatedBtn('plus')

        # --------------------------------------------------------------------------------
        # Connections
        # --------------------------------------------------------------------------------

        self.plusBtn.clicked.connect(lambda: self.activatedBtn('plus'))
        self.minusBtn.clicked.connect(lambda: self.activatedBtn('minus'))
        self.difBtn.clicked.connect(lambda: self.activatedBtn('dif'))
        self.testBtn.clicked.connect(self.printSelection)

        # --------------------------------------------------------------------------------
        # Tooltip
        # --------------------------------------------------------------------------------

        self.plusBtn.setToolTip('Plus')
        self.minusBtn.setToolTip('Minus')
        self.difBtn.setToolTip('Intersection')

    def deleteGroupBox(self):
        self.deleteLater()

    def activatedBtn(self, button):

        self.mode = button

        if self.mode == 'plus':
            self.plusBtn.setStyleSheet(self.greenBtn)
            self.minusBtn.setStyleSheet(self.greyBtn)
            self.difBtn.setStyleSheet(self.greyBtn)

        if self.mode == 'minus':
            self.plusBtn.setStyleSheet(self.greyBtn)
            self.minusBtn.setStyleSheet(self.redBtn)
            self.difBtn.setStyleSheet(self.greyBtn)

        if self.mode == 'dif':
            self.plusBtn.setStyleSheet(self.greyBtn)
            self.minusBtn.setStyleSheet(self.greyBtn)
            self.difBtn.setStyleSheet(self.blueBtn)

    def printSelection(self):
        listSelection = self.getSelection()
        print '\n\n\n'
        print '---------------------------------------------------------------------------'
        print '                             SELECTION                      number : '+str(len(listSelection))
        print '---------------------------------------------------------------------------'

        for i in listSelection:
            print i
        print '---------------------------------------------------------------------------'
        print '\n\n\n'


class SelectionSelector(Selector):

    def __init__(self):
        super(SelectionSelector, self).__init__()

        self.setTitle('By Selection')

        self.allCheck = QtWidgets.QCheckBox('All')
        self.dagObjectsCheck = QtWidgets.QCheckBox('Dag Objects')
        self.invertCheck = QtWidgets.QCheckBox('Invert selection')

        self.contentLayout.addWidget(self.allCheck)
        self.contentLayout.addWidget(self.dagObjectsCheck)
        # self.contentLayout.addWidget(self.invertCheck)

        self.dagObjectsCheck.clicked.connect(self.disableCheck)
        self.allCheck.clicked.connect(self.disableCheck)

    def disableCheck(self):
        if self.allCheck.isChecked():
            self.dagObjectsCheck.setDisabled(True)
            self.invertCheck.setDisabled(True)
        elif self.dagObjectsCheck.isChecked():
            self.allCheck.setDisabled(True)
            self.invertCheck.setDisabled(True)
        else:
            self.allCheck.setDisabled(False)
            self.dagObjectsCheck.setDisabled(False)
            self.invertCheck.setDisabled(False)

    def getSelection(self):
        if self.allCheck.isChecked():
            listSelection = mc.ls(allPaths=True)
        elif self.dagObjectsCheck.isChecked():
            listSelection = mc.ls(dagObjects=True)
        else:
            listSelection = mc.ls(selection=True)
        return set(listSelection)


class TypeSelector(Selector):

    def __init__(self):
        super(TypeSelector, self).__init__()

        self.setTitle('By Type')

        self.listAllTypes = mc.allNodeTypes(includeAbstract=False)
        self.typeCombo = QtWidgets.QComboBox()
        self.typeCombo.addItems(self.listAllTypes)
        self.parentTransformCheckbox = QtWidgets.QCheckBox()
        self.parentTransformCheckbox.setText('Parent Transform')

        self.contentLayout.addWidget(self.parentTransformCheckbox)
        self.contentLayout.addWidget(self.typeCombo)

    def getSelection(self):
        currentType = self.typeCombo.currentText()
        listSelection = mc.ls(type=currentType)
        parentSelection = set()

        if self.parentTransformCheckbox.isChecked():
            for i in listSelection:
                parent = mc.listRelatives(i, parent=True)
                if mc.objectType(parent) == 'transform':
                    parentSelection.update(parent)

        if parentSelection:
            listSelection = parentSelection

        return set(listSelection)


class NameSelector(Selector):

    def __init__(self):
        super(NameSelector, self).__init__()

        self.setTitle('By Name')

        self.nameLine = QtWidgets.QLineEdit()

        self.contentLayout.addWidget(self.nameLine)

    def getSelection(self):
        currentName = self.nameLine.text()
        listSelection = mc.ls(currentName)
        return set(listSelection)


class AdvancedSelectionUI(QtWidgets.QWidget):
    ''' Store Attribute UI '''

    def __init__(self):
        super(AdvancedSelectionUI, self).__init__()

        self.setWindowTitle('Advanced Selection')

        self.setMinimumSize(300, 500)
        self.resize(300, 500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)


        ########################################
        # Style

        # Color
        self.blueBtn = 'background-color:rgb(48, 127, 183);'
        self.greenBtn = 'background-color:rgb(127, 183, 49);'
        self.redBtn = 'background-color:rgb(224, 78, 62);'
        self.greyBtn = 'background-color:rgb(100, 100, 100);'

        # Font
        self.boldFont = QtGui.QFont()
        self.boldFont.setPixelSize(16)
        self.boldFont.setBold(True)

        ########################################

        self.createLayout()
        self.createWidget()
        self.createHierarchy()
        self.createConnections()

    def createLayout(self):
        ''' Create layout '''

        # Main Layout
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)

        self.newLayout = QtWidgets.QHBoxLayout()
        self.newLayout.setSpacing(5)

        self.selectorLayout = QtWidgets.QVBoxLayout()
        self.selectorLayout.setSpacing(5)

        self.resultLayout = QtWidgets.QHBoxLayout()
        self.resultLayout.setSpacing(5)

    def createWidget(self):
        ''' Create widget '''
        self.newCombo = QtWidgets.QComboBox()
        self.newCombo.addItems(['Selection', 'Type', 'Name', 'Child', 'Set', 'Attribute'])
        self.newBtn = QtWidgets.QPushButton('New')
        self.newBtn.setMaximumHeight(19)

        self.selector = SelectionSelector()

        self.selectResultBtn = QtWidgets.QPushButton('Select')


    def createHierarchy(self):
        ''' Create widget and layout hierarchy '''
        self.newLayout.addWidget(self.newCombo)
        self.newLayout.addWidget(self.newBtn)
        self.mainLayout.addLayout(self.newLayout)
        self.mainLayout.addLayout(self.selectorLayout)
        self.mainLayout.addLayout(self.resultLayout)

        self.selectorLayout.addWidget(self.selector)
        self.resultLayout.addWidget(self.selectResultBtn)

        # Add Main Layout to window
        self.setLayout(self.mainLayout)

    def createConnections(self):
        ''' Create UI connections '''
        self.newBtn.clicked.connect(self.newSelector)
        self.selectResultBtn.clicked.connect(self.selectResult)

    def newSelector(self):
        currentSelectorType = self.newCombo.currentText()

        if currentSelectorType == 'Selection':
            self.selectorLayout.addWidget(SelectionSelector())
        elif currentSelectorType == 'Type':
            self.selectorLayout.addWidget(TypeSelector())
        elif currentSelectorType == 'Name':
            self.selectorLayout.addWidget(NameSelector())

    def selectResult(self):
        nbItem = self.selectorLayout.count()

        setResult = set()

        for i in range(nbItem):
            widget = self.selectorLayout.itemAt(i).widget()
            selectorResult = widget.getSelection()
            selectorOperation = widget.mode

            if selectorOperation == 'plus':
                setResult.update(selectorResult)
            elif selectorOperation == 'minus':
                setResult.difference_update(selectorResult)
            elif selectorOperation == 'dif':
                setResult.intersection_update(selectorResult)

        mc.select(list(setResult))


def launch():
    ''' Def to call to launch tool in maya '''

    global advancedSelectionWin
    if advancedSelectionWin:
        advancedSelectionWin.close()

    advancedSelectionWin = AdvancedSelectionUI()
    advancedSelectionWin.show()
