#!/usr/bin/env python
# -*- coding: utf-8 -*-

''':mod:`randomizerLib`
===================================

.. module:: randomizerLib
   :platform: Windows
   :synopsis: advanced maya selection interface
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.10.11

'''

import maya.cmds as mc
from random import randrange, random, choice

def randomizeInt(min, max):

    print randrange(min, max)

    mc.undoInfo(openChunk=True)
    mc.undoInfo(closeChunk=True)

def randomizeFloat(min, max):

    print random()

def randomizeList(list):

    print choice(list)