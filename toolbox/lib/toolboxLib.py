#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`toolboxLib`
===================================

.. module:: toolboxLib
   :platform: Windows
   :synopsis: Custom toolbox
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.08.23

'''

import os
import json


def pathToFileInfo(file_path, prefix='', suffix='', log=False):

    '''
    Require "os" package
    :param file_path: string
    :param prefix: string
    :param suffix: string
    :param log: Bool
    :return: array [folder, file_name, file_without_ext, extension, file_without_prefixAndSuffix]
    '''

    folder, file_name = file_path.rsplit(os.sep, 1)
    file_without_ext, extension = file_name.rsplit('.', 1)
    file_without_prefixAndSuffix = ''

    if prefix != '' and suffix != '':
        without_suffix = file_without_ext.rsplit(suffix, 1)[0]
        file_without_prefixAndSuffix = without_suffix.split(prefix, 1)[-1]
    else:
        if prefix != '':
            file_without_prefixAndSuffix = file_without_ext.split(prefix, 1)[-1]

        if suffix != '':
            file_without_prefixAndSuffix = file_without_ext.rsplit(suffix, 1)[0]

    if log:
        print '\n\n\n-----------------  Function pathTofileInfo  -----------------\n'
        print 'Folder :', folder
        print 'File :', file_name
        print 'Without Extension :', file_without_ext
        print 'Extension :', extension
        print 'Without prefix/suffix :', file_without_prefixAndSuffix
        print '\n-------------------------------------------------------------\n\n\n'

    return folder, file_name, file_without_ext, extension, file_without_prefixAndSuffix


class ToolBoxLayout():

    def __init__(self, toolbox_file_path):

        self.file_path = toolbox_file_path
        _, _, _, self.file_extension, self.name = pathToFileInfo(toolbox_file_path, prefix='toolbox_')

        self.toolbox_data = {}
        self.list_category = []

        self.loadFile()

    def fileIsValid(self):

        if not self.file_extension == 'json':
            return False

        if not os.path.exists(self.file_path):
            return False

        else:
            return True

    def loadFile(self):

        if self.fileIsValid():
            with open(self.file_path) as json_data:
                self.toolbox_data = json.load(json_data)

    def saveFile(self):

        if self.fileIsValid():

            json_datas = json.dumps(self.toolbox_data, indent=4)
            f = open(self.file_path, 'w')
            f.write(json_datas)
            f.close()

    def getCategories(self):

        self.list_category = []

        for category in self.toolbox_data:
            self.list_category.append(category)
            self.list_category.sort()

        return self.list_category

    def getScriptInCategory(self, category):

        if category not in self.list_category:
            return False

        list_script = []

        for script in self.toolbox_data[category]:
            list_script.append(script)

        list_script.sort()
        return list_script

    def getScriptInfo(self, category, script):

        version = self.toolbox_data[category][script]['version']
        description = self.toolbox_data[category][script]['description']
        icon = self.toolbox_data[category][script]['icon']
        helpMessage = self.toolbox_data[category][script]['helpMessage']
        helpPicture = self.toolbox_data[category][script]['helpPicture']
        left_click_command = self.toolbox_data[category][script]['left_click_command']
        middle_click_command = self.toolbox_data[category][script]['middle_click_command']
        right_click_command = self.toolbox_data[category][script]['right_click_command']
        double_clickCommand = self.toolbox_data[category][script]['double_clickCommand']

        return version, description, icon, helpMessage, helpPicture, left_click_command, middle_click_command, right_click_command, double_clickCommand
