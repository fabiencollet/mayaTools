from PySide import QtGui
from PySide import QtCore
import maya.cmds as mc


class ListWidget(QtGui.QWidget):

    def __init__(self, widgetName, buttonAlignement, multipleSelection):

        super(ListWidget, self).__init__()

        self.widgetName = widgetName
        self.buttonAlignement = buttonAlignement
        self.multipleSelection = multipleSelection

        self.centerAlignement = QtCore.Qt.AlignCenter

        self.createLayout()
        self.createWidget()
        self.addWidgetToLayout()
        self.layoutHierarchy()
        self.createConnection()

    def createLayout(self):

        self.mainLayout = QtGui.QVBoxLayout()

        self.labelLayout = QtGui.QVBoxLayout()
        self.topLabelLayout = QtGui.QHBoxLayout()
        self.bottomLabelLayout = QtGui.QHBoxLayout()

        self.listLayout = QtGui.QHBoxLayout()
        self.buttonLayout = QtGui.QHBoxLayout()

    def createWidget(self):

        self.titleFont = QtGui.QFont()
        self.titleFont.setBold(True)
        self.titleFont.setPixelSize(16)

        # Label
        self.nameLabel = QtGui.QLabel(self.widgetName)
        self.nameLabel.setAlignment(self.centerAlignement)
        self.nameLabel.setFont(self.titleFont)


        self.nodeLabel = QtGui.QLabel('Node')
        self.nodeLabel.setAlignment(self.centerAlignement)

        self.attributesLabel = QtGui.QLabel('Attributes')
        self.attributesLabel.setAlignment(self.centerAlignement)

        # List
        self.nodeList = QtGui.QListWidget()
        self.attributesList = QtGui.QListWidget()

        if self.multipleSelection:
            self.multipleSelectionMode()

        # Button
        self.importBtn = QtGui.QPushButton('Import')
        self.importBtn.setMinimumHeight(30)
        self.importBtn.setMaximumWidth(200)
        self.importBtn.setMaximumWidth(300)

        # Spacer
        self.spacer = QtGui.QSpacerItem(400,0)


    def singleSelectionMode(self):
        self.nodeList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.attributesList.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)

    def multipleSelectionMode(self):
        self.nodeList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.attributesList.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)


    def addWidgetToLayout(self):

        # Label
        self.topLabelLayout.addWidget(self.nameLabel)

        self.bottomLabelLayout.addWidget(self.nodeLabel)
        self.bottomLabelLayout.addWidget(self.attributesLabel)

        # List
        self.listLayout.addWidget(self.nodeList)
        self.listLayout.addWidget(self.attributesList)

        # Button

        if self.buttonAlignement == 'left':
            self.buttonLayout.addItem(self.spacer)

        self.buttonLayout.addWidget(self.importBtn)

        if self.buttonAlignement == 'right':
            self.buttonLayout.addItem(self.spacer)

    def layoutHierarchy(self):

        self.labelLayout.addLayout(self.topLabelLayout)
        self.labelLayout.addLayout(self.bottomLabelLayout)

        self.mainLayout.addLayout(self.labelLayout)
        self.mainLayout.addLayout(self.listLayout)
        self.mainLayout.addLayout(self.buttonLayout)

    def createConnection(self):
        self.importBtn.clicked.connect(self.importSelection)
        self.nodeList.doubleClicked.connect(self.listAttributes)


    def importSelection(self):

        listSelection = mc.ls(selection=True)

        self.nodeList.clear()
        self.nodeList.addItems(listSelection)

        node = listSelection[0]

        listAttr = mc.listAttr(node)

        self.attributesList.clear()
        self.attributesList.addItems(listAttr)


    def listAttributes(self):
        items = self.nodeList.selectedItems()
        node = str(items[0].text())

        listAttr = mc.listAttr(node)

        self.attributesList.clear()
        self.attributesList.addItems(listAttr)


class MultiConnectionUi(QtGui.QDialog):

    def __init__(self):

        super(MultiConnectionUi, self).__init__()

        self.setWindowTitle('Multi Connection')
        self.setMinimumSize(600, 300)
        self.resize(700, 400)


    def createLayout(self):

        self.mainLayout = QtGui.QHBoxLayout()
        self.connectionLayout = QtGui.QVBoxLayout()


    def createWidget(self):

        # List
        self.listOutWidget = ListWidget('OUTPUT', 'right', False)
        self.listInWidget = ListWidget('INPUT', 'left', True)

        # Button Connection
        self.invertBtn = QtGui.QPushButton('< >')
        self.invertBtn.setMinimumHeight(50)
        self.connectBtn = QtGui.QPushButton('Connect')
        self.connectBtn.setMinimumHeight(50)

        # CheckBox
        self.forceModeCheck = QtGui.QCheckBox('Force Mode')
        self.forceModeCheck.setChecked(True)


    def addWidgetToLayout(self):

        self.connectionLayout.addWidget(self.invertBtn)

        self.connectionLayout.addWidget(self.forceModeCheck)
        self.connectionLayout.addWidget(self.connectBtn)

    def layoutHierarchy(self):

        self.mainLayout.addLayout(self.listOutWidget.mainLayout)
        self.mainLayout.addLayout(self.connectionLayout)
        self.mainLayout.addLayout(self.listInWidget.mainLayout)

        self.setLayout(self.mainLayout)

    def createConnection(self):
        self.invertBtn.clicked.connect(self.invertList)
        self.connectBtn.clicked.connect(self.connectNode)

    def connectNode(self):

        outputNodeItems = self.listOutWidget.nodeList.selectedItems()
        outputNode = str(outputNodeItems[0].text())

        outputAttributesItems = self.listOutWidget.attributesList.selectedItems()
        outputAttribute = str(outputAttributesItems[0].text())

        inputNode = []
        inputNodeItems = self.listInWidget.nodeList.selectedItems()
        for i in inputNodeItems:
            inputNode.append(str(i.text()))

        inputAttributes = []
        inputAttributesItems = self.listInWidget.attributesList.selectedItems()
        for i in inputAttributesItems:
            inputAttributes.append(str(i.text()))

        # Force Mode
        forceMode = self.forceModeCheck.isChecked()

        if outputNode and outputAttribute:
            if inputNode and inputAttributes:
                outputConnection = '.'.join([outputNode,outputAttribute])
                if mc.objExists(outputConnection):
                    for node in inputNode:
                        for attribute in inputAttributes:
                            inputConnection = '.'.join([node, attribute])
                            if mc.objExists(inputConnection):
                                mc.connectAttr(outputConnection, inputConnection, force=forceMode)
                            else:
                                print '[ERROR][INPUT][NOT_EXIST]   =>', inputConnection
                else:
                    print '[ERROR][OUTPUT][NOT_EXIST]   =>',outputConnection
            else:
                print '[ERROR][INPUT][SELECTION]'
        else:
            print '[ERROR][OUTPUT][SELECTION]'


    def invertList(self):

        self.listOutWidget.multipleSelectionMode()

        self.listOutWidget.nodeList.selectAll()
        outputNode = []
        outputNodeItems = self.listOutWidget.nodeList.selectedItems()
        for i in outputNodeItems:
            outputNode.append(i.text())


        self.listOutWidget.attributesList.selectAll()
        outputAttributes = []
        outputAttributesItems = self.listOutWidget.attributesList.selectedItems()
        for i in outputAttributesItems:
            outputAttributes.append(i.text())


        self.listInWidget.nodeList.selectAll()
        inputNode = []
        inputNodeItems = self.listInWidget.nodeList.selectedItems()
        for i in inputNodeItems:
            inputNode.append(i.text())


        self.listInWidget.attributesList.selectAll()
        inputAttributes = []
        inputAttributesItems = self.listInWidget.attributesList.selectedItems()
        for i in inputAttributesItems:
            inputAttributes.append(i.text())


        self.listOutWidget.nodeList.clear()
        self.listOutWidget.attributesList.clear()
        self.listInWidget.nodeList.clear()
        self.listInWidget.attributesList.clear()

        self.listOutWidget.nodeList.addItems(inputNode)
        self.listOutWidget.attributesList.addItems(inputAttributes)
        self.listInWidget.nodeList.addItems(outputNode)
        self.listInWidget.attributesList.addItems(outputAttributes)

        self.listOutWidget.singleSelectionMode()

    def displayUi(self):

        self.createLayout()
        self.createWidget()
        self.addWidgetToLayout()
        self.layoutHierarchy()
        self.createConnection()

        self.show()


multi = MultiConnectionUi()
multi.displayUi()