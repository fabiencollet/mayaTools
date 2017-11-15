''':mod:`lookDevLib`
===================================

.. module:: lookDevLib
   :platform: Linux
   :synopsis: Arnold Look Development Library
   :author: Fabien Collet <fbncollet@gmail.com>
   :date: 2017.11.15

'''

import maya.cmds as mc
from math import tan, radians

LD_CAMERA_FOCAL = 38.56

def createTurnTable(asset):

    # Get Asset Bounding Box
    bbMinX, bbMinY, bbMinZ, bbMaxX, bbMaxY, bbMaxZ = mc.exactWorldBoundingBox()
    bbSizeX = bbMaxX - bbMinX
    bbSizeY = bbMaxY - bbMinY
    bbSizeZ = bbMaxZ - bbMinZ

    bbCenterX = (bbSizeX / 2) + bbMinX
    bbCenterY = (bbSizeY / 2) + bbMinY
    bbCenterZ = (bbSizeZ / 2) + bbMinZ

    if bbSizeX > bbSizeY:
        halfBBSize = bbSizeX / 2

    else:
        halfBBSize = bbSizeY / 2

    print 'size X : {}'.format(bbSizeX)
    print 'size Y : {}'.format(bbSizeY)
    print 'size Z : {}'.format(bbSizeZ)


    print halfBBSize
    camPosZ = ((halfBBSize)/tan(radians(LD_CAMERA_FOCAL/2))) + (bbSizeZ/2)
    print camPosZ