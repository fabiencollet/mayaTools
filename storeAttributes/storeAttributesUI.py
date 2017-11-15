''':mod:`storeAttributesUI`
===================================
.. module:: storeAttributesUI
   :platform: Windows
   :synopsis: UI part to store attribute in json file
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.08
   :version: 1.0.0
   :todo: Adding undo feature after apply values
'''

import lib.storeAttributesLib as storeAttr
from ..lib.Qt import QtWidgets, QtCore, QtGui
import maya.cmds as mc

reload(storeAttr)

storeAttributesUILog = storeAttr.Log('storeAttributesLog')

storeAttributesWin = None


class StoreAttributesUI(QtWidgets.QWidget):
    ''' Store Attribute UI '''

    def __init__(self):
        super(StoreAttributesUI, self).__init__()

        self.setWindowTitle('Store Attributes')

        self.setMinimumSize(400, 400)
        self.resize(650, 500)
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

        self.attributes = storeAttr.Attributes()

        # Second UI
        self.settingsDialog = SettingsDialog()
        self.searchAndReplaceDialog = SearchAndReplaceDialog()

        self.headerTreeName = 'node'
        self.headerTreeList = []

        self.createLayout()
        self.createWidget()
        self.createHierarchy()
        self.createConnections()
        self.updateHeaderTreeLabel()

    def createLayout(self):
        ''' Create layout '''

        # Main Layout
        self.mainLayout = QtWidgets.QVBoxLayout()
        self.mainLayout.setSpacing(0)

        # Options Layout
        self.optionsLayout = QtWidgets.QHBoxLayout()
        self.optionsLayout.setSpacing(0)

        # List Layout
        self.listLayout = QtWidgets.QHBoxLayout()
        self.listLayout.setSpacing(0)

        # Menu Layout
        self.menuLayout = QtWidgets.QVBoxLayout()
        self.menuLayout.setSpacing(5)

        # Import Layout
        self.importLayout = QtWidgets.QVBoxLayout()
        self.importLayout.setSpacing(2)

        # Append Subtract Layout
        self.appendSubtractLayout = QtWidgets.QHBoxLayout()
        self.appendSubtractLayout.setSpacing(2)

        # Tree Layout
        self.treeLayout = QtWidgets.QVBoxLayout()
        self.treeLayout.setSpacing(5)

        # Search Layout
        self.searchLayout = QtWidgets.QHBoxLayout()
        self.searchLayout.setSpacing(5)

        # Json Layout
        self.jsonGroupBoxLayout = QtWidgets.QVBoxLayout()
        self.jsonGroupBoxLayout.setSpacing(0)

        # Json Layout
        self.listGroupBoxLayout = QtWidgets.QVBoxLayout()
        self.listGroupBoxLayout.setSpacing(0)

    def createWidget(self):
        ''' Create widget '''

        # Group  Box
        self.jsonGroupBox = QtWidgets.QGroupBox('Json')
        self.jsonGroupBox.setMaximumHeight(150)

        self.listGroupBox = QtWidgets.QGroupBox('List')

        ########################################

        # Buttons

        # Settings
        self.settingsBtn = QtWidgets.QPushButton('Settings')
        self.settingsBtn.setMinimumHeight(30)
        self.settingsBtn.setStyleSheet(self.greyBtn)

        # Import
        self.importJsonBtn = QtWidgets.QPushButton('Import')
        self.importJsonBtn.setMinimumHeight(30)
        self.importJsonBtn.setMinimumWidth(120)
        self.importJsonBtn.setStyleSheet(self.blueBtn)

        # Append
        self.appendJsonBtn = QtWidgets.QPushButton('+')
        self.appendJsonBtn.setMinimumHeight(30)
        self.appendJsonBtn.setStyleSheet(self.blueBtn)
        self.appendJsonBtn.setFont(self.boldFont)

        # Subtract
        self.subtractJsonBtn = QtWidgets.QPushButton('-')
        self.subtractJsonBtn.setMinimumHeight(30)
        self.subtractJsonBtn.setStyleSheet(self.blueBtn)
        self.subtractJsonBtn.setFont(self.boldFont)

        # Save
        self.saveJsonBtn = QtWidgets.QPushButton('Save')
        self.saveJsonBtn.setMinimumHeight(30)
        self.saveJsonBtn.setStyleSheet(self.greenBtn)

        ########################################

        # Find and replace
        self.replaceBtn = QtWidgets.QPushButton('Search and replace')
        self.replaceBtn.setMinimumHeight(30)
        self.replaceBtn.setStyleSheet(self.blueBtn)

        # Append
        self.appendBtn = QtWidgets.QPushButton('Append')
        self.appendBtn.setMinimumHeight(30)
        self.appendBtn.setStyleSheet(self.greenBtn)

        # Remove
        self.removeBtn = QtWidgets.QPushButton('Remove')
        self.removeBtn.setMinimumHeight(30)
        self.removeBtn.setStyleSheet(self.redBtn)

        # Select
        self.selectBtn = QtWidgets.QPushButton('Select')
        self.selectBtn.setMinimumHeight(30)
        self.selectBtn.setStyleSheet(self.blueBtn)

        # Apply
        self.applyBtn = QtWidgets.QPushButton('Apply')
        self.applyBtn.setMinimumHeight(30)
        self.applyBtn.setStyleSheet(self.blueBtn)

        ########################################

        # Text Search Widget
        self.searchTxt = QtWidgets.QLineEdit()

        self.searchBtn = QtWidgets.QPushButton('Search')
        self.searchBtn.setFixedWidth(65)

        ########################################

        # Tree Widget
        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setColumnWidth(0, 20)
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)


    def createHierarchy(self):
        ''' Create widget and layout hierarchy '''

        self.menuLayout.addWidget(self.settingsBtn)

        # Button > Group Box
        # Json
        self.importLayout.addWidget(self.importJsonBtn)

        self.appendSubtractLayout.addWidget(self.appendJsonBtn)
        self.appendSubtractLayout.addWidget(self.subtractJsonBtn)
        self.importLayout.addLayout(self.appendSubtractLayout)

        self.jsonGroupBoxLayout.addLayout(self.importLayout)

        self.jsonGroupBoxLayout.addWidget(self.saveJsonBtn)

        self.jsonGroupBox.setLayout(self.jsonGroupBoxLayout)

        # List
        self.listGroupBoxLayout.addWidget(self.appendBtn)
        self.listGroupBoxLayout.addWidget(self.removeBtn)
        self.listGroupBoxLayout.addWidget(self.replaceBtn)
        self.listGroupBoxLayout.addWidget(self.selectBtn)
        self.listGroupBoxLayout.addWidget(self.applyBtn)

        self.listGroupBox.setLayout(self.listGroupBoxLayout)

        # Group Box
        self.menuLayout.addWidget(self.jsonGroupBox)
        self.menuLayout.addWidget(self.listGroupBox)

        # Tree Layout
        self.searchLayout.addWidget(self.searchTxt)
        self.searchLayout.addWidget(self.searchBtn)

        self.treeLayout.addLayout(self.searchLayout)
        self.treeLayout.addWidget(self.treeWidget)

        # Layout Hierarchy #

        # Main --
        #        |-- Options
        #        |-- List --
        #                   |-- Menu --
        #                              |-- Import
        #                   |-- Tree --
        #                              |-- Search

        self.listLayout.addLayout(self.menuLayout)
        self.listLayout.addLayout(self.treeLayout)

        self.mainLayout.addLayout(self.optionsLayout)
        self.mainLayout.addLayout(self.listLayout)

        # Add Main Layout to window
        self.setLayout(self.mainLayout)

    def createConnections(self):
        ''' Create UI connections '''

        self.importJsonBtn.clicked.connect(self.importJson)
        self.appendJsonBtn.clicked.connect(self.appendJson)
        self.subtractJsonBtn.clicked.connect(self.subtractJson)

        self.saveJsonBtn.clicked.connect(self.saveJson)

        self.appendBtn.clicked.connect(self.appendItems)
        self.removeBtn.clicked.connect(self.removeItems)
        self.applyBtn.clicked.connect(self.applyValues)

        self.replaceBtn.clicked.connect(self.searchAndReplaceDisplay)

        self.searchAndReplaceDialog.processBtn.clicked.connect(self.searchAndReplace)

        # Settings
        self.settingsBtn.clicked.connect(self.displaySettings)
        self.settingsDialog.applyBtn.clicked.connect(self.applySettings)

        # Select
        self.treeWidget.doubleClicked.connect(self.selectItemInMaya)
        self.selectBtn.clicked.connect(self.selectItemInMaya)

        # Search
        self.searchBtn.clicked.connect(self.searchInTreeWidget)
        self.searchTxt.returnPressed.connect(self.searchInTreeWidget)

    def searchAndReplaceDisplay(self):
        ''' Display search and replace UI '''

        items = self.treeWidget.selectedItems()

        if not items:
            self.treeWidget.selectAll()

        self.searchAndReplaceDialog.displayUi()

    def searchAndReplace(self):
        ''' Search and replace node name '''

        items = self.treeWidget.selectedItems()

        findTxt = str(self.searchAndReplaceDialog.findTxt.text())
        replaceTxt = str(self.searchAndReplaceDialog.replaceTxt.text())

        for item in items:
            obj_name = str(item.text(0))
            self.attributes.searchAndReplaceNodes(obj_name, findTxt, replaceTxt)

        self.searchAndReplaceDialog.close()
        self.updateTreeWidget()

    def displaySettings(self):
        ''' Display Settings UI '''

        self.settingsDialog.displayUi(self.attributes.listAttributes)

    def applySettings(self):
        ''' Change tree widget header label'''

        # Get new Attributes
        self.settingsDialog.activeList.selectAll()
        items = self.settingsDialog.activeList.selectedItems()
        listAttributes = []

        for item in items:
            listAttributes.append(str(item.text()))

        self.attributes.changeAttributes(listAttributes)

        self.attributes.appendAttributesValue(self.attributes.listNodes())

        self.clearTreeWidget()
        self.updateTreeWidget()
        self.updateHeaderTreeLabel()

        self.settingsDialog.close()

    def searchInTreeWidget(self):
        ''' Search and select item in tree widget'''

        self.treeWidget.selectAll()
        items = self.treeWidget.selectedItems()
        self.treeWidget.clearSelection()

        textSearch = str(self.searchTxt.text())

        storeAttributesUILog.info('[SEARCH]  {}'.format(textSearch))

        for item in items:
            obj_name = str(item.text(0))
            if textSearch.lower() in obj_name.lower():
                self.treeWidget.setItemSelected(item, True)
                self.treeWidget.scrollToItem(item)
                storeAttributesUILog.info('[SEARCH] [MATCH]  {}'.format(obj_name))

    def importJson(self):
        ''' import data to treeWidget '''

        self.attributes.importDict()
        self.clearTreeWidget()
        self.updateTreeWidget()
        self.updateHeaderTreeLabel()

    def appendJson(self):
        ''' Append current treeWidget with another data '''

        self.attributes.appendDict()
        self.clearTreeWidget()
        self.updateTreeWidget()
        self.updateHeaderTreeLabel()

    def subtractJson(self):
        ''' Subtract current treeWidget with another data '''

        self.attributes.subtractDict()
        self.clearTreeWidget()
        self.updateTreeWidget()
        self.updateHeaderTreeLabel()

    def saveJson(self):
        ''' Save data to json file'''

        self.attributes.saveDict()

    def applyValues(self):
        ''' Apply values in maya scene'''

        self.treeWidget.selectAll()
        items = self.treeWidget.selectedItems()
        self.treeWidget.clearSelection()

        for item in items:
            obj_name = str(item.text(0))
            if not mc.objExists(obj_name):
                self.treeWidget.setItemSelected(item, True)

        self.attributes.applyAttributesValue()

    def clearTreeWidget(self):
        ''' Clear all item and header label in tree widget'''

        self.treeWidget.deleteLater()
        self.treeWidget = QtWidgets.QTreeWidget()
        self.treeWidget.setSelectionMode(QtWidgets.QAbstractItemView.ContiguousSelection)
        self.treeWidget.doubleClicked.connect(self.selectItemInMaya)
        self.treeLayout.addWidget(self.treeWidget)

    def updateTreeWidget(self):
        ''' Convert data to item and display item in tree widget'''

        self.treeWidget.clear()

        if self.attributes.dictAttributesValues:
            for node in sorted(self.attributes.dictAttributesValues):
                listItem = []
                listItem.append(node)
                for attribute in self.attributes.listAttributes:
                    if attribute not in self.attributes.dictAttributesValues[node]:
                        listItem.append('')
                    else:
                        listItem.append(str(self.attributes.dictAttributesValues[node][attribute]))
                newItem = QtWidgets.QTreeWidgetItem(listItem)
                self.treeWidget.addTopLevelItem(newItem)

    def appendItems(self):
        ''' Append new item in tree widget'''

        listNode = mc.ls(selection=True)
        self.attributes.appendAttributesValue(listNode)
        self.updateTreeWidget()

    def removeItems(self):
        ''' Remove item in tree widget'''

        listItemToRemove = []

        items = self.treeWidget.selectedItems()
        for item in items:
            listItemToRemove.append(str(item.text(0)))
            indexTopItem = self.treeWidget.indexOfTopLevelItem(item)
            self.treeWidget.takeTopLevelItem(indexTopItem)

        if listItemToRemove:
            self.attributes.removeAttributesValue(listItemToRemove)

    def selectItemInMaya(self):
        ''' Select node in maya scene'''

        items = self.treeWidget.selectedItems()
        if not items:
            self.treeWidget.selectAll()
            items = self.treeWidget.selectedItems()
        listSelection = []
        if items:
            for item in items:
                if mc.objExists(str(item.text(0))):
                    listSelection.append(item.text(0))
                else:
                    print '[ERROR][NOT_EXIST]   ', item.text(0)
            mc.select(listSelection)

    def updateHeaderTreeLabel(self):
        ''' Update tree widget label'''

        self.headerTreeList = []
        self.headerTreeList.append(self.headerTreeName)
        for attribute in self.attributes.listAttributes:
            self.headerTreeList.append(attribute)

        self.treeWidget.setHeaderLabels(self.headerTreeList)


class SearchAndReplaceDialog(QtWidgets.QDialog):
    ''' Search and replace UI '''
    def __init__(self):

        super(SearchAndReplaceDialog, self).__init__()

        self.setWindowTitle('Search and Replace')
        self.setMinimumSize(250, 125)

        # Layout
        self.mainLayout = QtWidgets.QVBoxLayout()

        self.findLayout = QtWidgets.QHBoxLayout()
        self.replaceLayout = QtWidgets.QHBoxLayout()

        self.findLabel = QtWidgets.QLabel('Search :')
        self.findTxt = QtWidgets.QLineEdit()

        self.replaceLabel = QtWidgets.QLabel('Replace :')
        self.replaceTxt = QtWidgets.QLineEdit()

        self.processBtn = QtWidgets.QPushButton('Process')

    def createLayoutHierarchy(self):
        ''' Create widget and layout hierarchy '''

        # Main Layout
        self.findLayout.addWidget(self.findLabel)
        self.findLayout.addWidget(self.findTxt)

        self.replaceLayout.addWidget(self.replaceLabel)
        self.replaceLayout.addWidget(self.replaceTxt)

        self.mainLayout.addLayout(self.findLayout)
        self.mainLayout.addLayout(self.replaceLayout)
        self.mainLayout.addWidget(self.processBtn)

        # Dialog Layout
        self.setLayout(self.mainLayout)

    def displayUi(self):
        ''' Display searchAndReplaceUI'''

        self.createLayoutHierarchy()
        self.show()


class SettingsDialog(QtWidgets.QDialog):
    ''' Settings UI '''

    def __init__(self):

        super(SettingsDialog, self).__init__()

        self.setWindowTitle('Settings')
        self.setMinimumSize(600, 500)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

        # CSS
        self.greenLabel = 'color:rgb(127, 183, 49);'
        self.redLabel = 'color:rgb(224, 78, 62);'

        # Layout
        self.mainLayout = QtWidgets.QVBoxLayout()

        self.transferButtonLayout = QtWidgets.QVBoxLayout()

        self.labelLayout = QtWidgets.QHBoxLayout()
        self.listLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout = QtWidgets.QHBoxLayout()

        # Widget

        # Label
        self.activeLabel = QtWidgets.QLabel('Active')
        self.activeLabel.setStyleSheet(self.greenLabel)
        self.activeLabel.setAlignment(QtCore.Qt.AlignCenter)

        self.inactiveLabel = QtWidgets.QLabel('Inactive')
        self.inactiveLabel.setStyleSheet(self.redLabel)
        self.inactiveLabel.setAlignment(QtCore.Qt.AlignCenter)

        # List
        self.activeList = QtWidgets.QListWidget()
        self.activeList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        self.inactiveList = QtWidgets.QListWidget()
        self.inactiveList.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # Transfer Button
        self.inactiveBtn = QtWidgets.QPushButton('>')
        self.inactiveBtn.setMinimumHeight(40)

        self.activeBtn = QtWidgets.QPushButton('<')
        self.activeBtn.setMinimumHeight(40)

        # Button
        self.applyBtn = QtWidgets.QPushButton('Apply')
        self.listBtn = QtWidgets.QPushButton('List attributes from Selection')

        self.labelLayout.addWidget(self.activeLabel)
        self.labelLayout.addWidget(self.inactiveLabel)

        self.transferButtonLayout.addWidget(self.inactiveBtn)
        self.transferButtonLayout.addWidget(self.activeBtn)

        self.listLayout.addWidget(self.activeList)
        self.listLayout.addLayout(self.transferButtonLayout)
        self.listLayout.addWidget(self.inactiveList)

        self.buttonLayout.addWidget(self.applyBtn)
        self.buttonLayout.addWidget(self.listBtn)

        # Connections
        self.listBtn.clicked.connect(self.listFromSelection)

        self.inactiveBtn.clicked.connect(self.activeToInactive)
        self.activeBtn.clicked.connect(self.inactiveToActive)

    def activeToInactive(self):
        ''' Take selected item from active list to inactive list '''

        selectedItem = self.activeList.selectedItems()
        self.activeList.clearSelection()

        for item in selectedItem:
            itemText = item.text()
            self.inactiveList.addItem(itemText)

            self.activeList.takeItem(self.activeList.row(item))

    def inactiveToActive(self):
        ''' Take selected item from inactive list to active list '''

        selectedItem = self.inactiveList.selectedItems()
        self.inactiveList.clearSelection()

        for item in selectedItem:
            itemText = item.text()
            self.activeList.addItem(itemText)

            self.inactiveList.takeItem(self.inactiveList.row(item))

    def listFromSelection(self):
        ''' Set inactive list with with listAttr from first selected node in maya '''

        self.inactiveList.clear()
        sel = mc.ls(selection=True)

        if sel:
            obj = sel[0]
            attributes = mc.listAttr(obj, write=True, read=True, unlocked=True, ramp=False,
                                     array=False, hasData=True, visible=True)

            self.inactiveList.addItems(attributes)

    def createLayoutHierarchy(self):
        ''' Create layout hierarchy '''

        # Main Layout
        self.mainLayout.addLayout(self.labelLayout)
        self.mainLayout.addLayout(self.listLayout)
        self.mainLayout.addLayout(self.buttonLayout)

        # Dialog Layout
        self.setLayout(self.mainLayout)

    def displayUi(self, attributes):
        ''' Display Settings UI '''

        self.activeList.clear()
        self.inactiveList.clear()

        self.activeAttributes = attributes
        self.activeList.addItems(attributes)

        self.createLayoutHierarchy()

        self.show()


def launch():
    ''' Def to call to launch tool in maya '''

    global storeAttributesWin
    if storeAttributesWin:
        storeAttributesWin.close()

    storeAttributesWin = StoreAttributesUI()
    storeAttributesWin.show()