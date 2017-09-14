''':mod:`storeAttributesLib`
===================================
.. module:: storeAttributesLib
   :platform: Windows
   :synopsis: Library part to store attribute in dict and load/save into json file
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.08
   :version: 1.0.0
   :todo: Adding undo feature after apply values
'''

import json
import os
import pprint

import maya.cmds as mc
from mayaTools.lib.Qt import QtWidgets

##########################
#        SETTINGS
##########################
pref_dir = mc.internalVar(userPresetsDir=True)
STORE_DIR = os.sep.join([pref_dir, 'storeAttributes'])
##########################

class Log(object):

    def __init__(self, scriptName):
        self.scripName = scriptName

    def error(self, text):
        print '[{0}] [ERROR]    | {1}'.format(self.scripName, text)

    def warning(self, text):
        print '[{0}] [WARNING]  | {1}'.format(self.scripName, text)

    def info(self, text):
        print '[{0}] [INFO]     | {1}'.format(self.scripName, text)


storeAttributesLibLog = Log('storeAttributesLog')

class Attributes(object):
    ''' Class to store nodes and her attributes in dict '''

    def __init__(self):
        self.listAttributes = ['rotateX', 'rotateY', 'rotateZ',
                               'scaleX', 'scaleY', 'scaleZ',
                               'translateX', 'translateY', 'translateZ']

        self.dictAttributesValues = {}



    # Attribute's methods

    def sortedAttributes(self):
        ''' Sorted listAttributes '''

        self.listAttributes = sorted(self.listAttributes)

    def appendAttributes(self, listAttributes):
        ''' Append attribute(s) in listAttributes '''

        for attribute in listAttributes:
            self.listAttributes.append(attribute)
        self.sortedAttributes()

    def removeAttributes(self, listAttributes):
        ''' Remove attribute(s) in listAttributes '''

        for attribute in listAttributes:
            if attribute in self.listAttributes:
                self.listAttributes.remove(attribute)
        self.sortedAttributes()

    def changeAttributes(self, listAttributes):
        ''' Change all attributes in listAttributes '''

        self.listAttributes = listAttributes
        self.sortedAttributes()

    def getAttributesFromDict(self):
        ''' get all attributes from dictAttributeValues and fill there in listAttributes '''

        self.listAttributes = []

        for node in self.dictAttributesValues:
            nodeAttributes = sorted(self.dictAttributesValues[node].keys())
            for attribute in nodeAttributes:
                if not attribute in self.listAttributes:
                    self.listAttributes.append(attribute)

        self.sortedAttributes()

    def printAttributes(self):
        ''' print listAttributes '''

        print self.listAttributes

    # Attribute's value methods

    def appendAttributesValue(self, listNodes):
        ''' Append node name and attribute(s) value in dictAttributeValue '''

        if listNodes:
            for node in listNodes:

                dictAttributeValue = {}

                if mc.objExists(node):
                    for attribute in self.listAttributes:
                        if mc.objExists(node+'.'+attribute):
                            attributeValue = mc.getAttr(node+'.'+attribute)
                            dictAttributeValue[attribute] = attributeValue
                        else:
                            storeAttributesLibLog.error('[ERROR] [ATTRIBUTE] [DOES NOT EXIST]  {}.{}'.format(node, attribute))

                    self.dictAttributesValues[node] = dictAttributeValue

                else:
                    storeAttributesLibLog.error('[ERROR] [NODE] [DOES NOT EXIST]  {}'.format(node))

    def removeAttributesValue(self, listNodes):
        ''' Remove node name and attribute(s) value in dictAttributeValue '''

        for node in listNodes:
            if node in self.dictAttributesValues:
                self.dictAttributesValues.pop(node, None)

    def applyAttributesValue(self):
        ''' Append attribute(s) value store in dictAttributeValue '''

        if self.dictAttributesValues:
            for node in self.dictAttributesValues:
                if mc.objExists(node):
                    for attribute in self.dictAttributesValues[node]:
                        if mc.objExists(node + '.' + attribute):
                            attributeValue = self.dictAttributesValues[node][attribute]
                            if attributeValue is not None:
                                mc.setAttr(node + '.' + attribute, attributeValue)
                            else:
                                storeAttributesLibLog.error('[ATTRIBUTE VALUE] '
                                                          '[IS EMPTY] {}.{}'.format(node,
                                                                                    attribute))
                        else:
                            storeAttributesLibLog.error('[ATTRIBUTE] '
                                                      '[DOES NOT EXIST] {}.{}'.format(node,
                                                                                      attribute))
                else:
                            storeAttributesLibLog.error('[NODE] [DOES NOT EXIST] {}'.format(node))

    def listNodes(self):
        ''' List all nodes name
        :return list nodes name from dictAttributeValue
        '''

        listNodes = []

        if self.dictAttributesValues:
            for node in self.dictAttributesValues:
                listNodes.append(node)

            if listNodes:
                return listNodes

    def renameNode(self, oldName, newName):
        ''' Rename node in dictAttributesValues
        :param oldName: current node name
        :type string
        :param newName: new node name
        :type string
        '''

        attributes = self.dictAttributesValues[oldName]
        self.dictAttributesValues[newName] = attributes
        self.dictAttributesValues.pop(oldName, None)

    def searchAndReplaceNodes(self, node, searchTxt, replaceTxt):
        ''' Search string in node name and replace with new string
        :param node: node name
        :type string
        :param searchTxt: search string
        :type string
        :param replaceTxt: replace string
        :type string
        '''

        if node in self.dictAttributesValues:
                if searchTxt in node:
                    splitNode = node.split(searchTxt)
                    newNode = replaceTxt.join(splitNode)

                    self.renameNode(node, newNode)

    def saveDict(self):
        ''' Save dictAttributesValues to json file'''

        if self.dictAttributesValues:

            json_datas = json.dumps(self.dictAttributesValues, indent=4)

            if not os.path.exists(STORE_DIR):
                os.makedirs(STORE_DIR)

            filePath = QtWidgets.QFileDialog.getSaveFileName(caption='Save As',
                                                             directory=STORE_DIR,
                                                             filter='json (*.json)')[0]

            if filePath:
                splitPath = filePath[0].rsplit(os.sep, 1)
                fileName = splitPath[-1]

                f = open(filePath, 'w')

                f.write(json_datas)
                f.close()

                storeAttributesLibLog.info('[SAVE]  {}'.format(f))

        else :
            storeAttributesLibLog.error('[DATA] Data are Empty')

    def loadDict(self):
        ''' Load json file
        :return dict{node {attribute: value}}
        '''

        if not os.path.exists(STORE_DIR):
            os.makedirs(STORE_DIR)

        filePath = QtWidgets.QFileDialog.getOpenFileName(caption='Import',
                                                         directory=STORE_DIR)[0]

        print '\n\n\n\n\n' + str(filePath) + '\n\n\n\n\n'

        if filePath:
            storeAttributesLibLog.info('[LOAD]  {}'.format(filePath))
            with open(filePath) as json_data:
                data = json.load(json_data)
            return data

    def importDict(self):
        ''' Import json data to dictAttributesValues '''

        data = self.loadDict()

        if data:
            self.dictAttributesValues = data
            self.getAttributesFromDict()

    def appendDict(self):
        ''' Append json data with dictAttributesValues '''

        data = self.loadDict()

        if data:
            for node in data:
                self.dictAttributesValues[node] = data[node]

            self.getAttributesFromDict()

    def subtractDict(self):
        ''' Subtract json data{node} with dictAttributesValues{node} '''

        data = self.loadDict()

        if data:
            for node in data:
                self.dictAttributesValues.pop(node, None)

            self.getAttributesFromDict()

    def printAttributesValue(self):
        ''' Custom dictAttributesValues print '''

        pprint.pprint(self.dictAttributesValues)
