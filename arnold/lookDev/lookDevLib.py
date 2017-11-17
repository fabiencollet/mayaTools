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


LD_CAMERA_FOCAL = 75
CAMERA_NAME = 'camera_lookDev'
OVERSCAN = 1


def createTurnTable(asset, debug=False):

    # Get Bounding Box Asset
    bbMinX, bbMinY, bbMinZ, bbMaxX, bbMaxY, bbMaxZ = mc.exactWorldBoundingBox()

    bbSizeX = bbMaxX - bbMinX
    bbSizeY = bbMaxY - bbMinY
    bbSizeZ = bbMaxZ - bbMinZ

    bbCenterX = (bbSizeX / 2) + bbMinX
    bbCenterY = (bbSizeY / 2) + bbMinY
    bbCenterZ = (bbSizeZ / 2) + bbMinZ

    if debug:
        print 'Size X : ' + str(bbSizeX)
        print 'Size Y : ' + str(bbSizeY)
        print 'Size Z : ' + str(bbSizeZ)

    # Create Look Development Camera
    mc.camera(focalLength=LD_CAMERA_FOCAL)
    if mc.objExists(CAMERA_NAME):
        mc.delete(CAMERA_NAME)
    mc.rename(CAMERA_NAME)

    # Get Camera Shape
    cameraShape = mc.listRelatives(CAMERA_NAME, children=True, type='shape')[0]
    # Get Field of View
    fov = mc.camera(cameraShape, query=True, horizontalFieldOfView=True)
    # Get Rendering Aspect Ratio
    aspectRatio = mc.getAttr('defaultResolution.deviceAspectRatio')

    # Get Camera Position
    camPosX = bbMinX + (bbSizeX / 2)
    camPosY = bbMinY + (bbSizeY / 2)

    if bbSizeZ >= bbSizeY and bbSizeZ >= bbSizeX:
        camPosZ = (((bbSizeZ / 2) / tan(radians(fov / 2))) + (bbSizeX / 2)) * OVERSCAN
    elif bbSizeX >= bbSizeY and bbSizeX >= bbSizeZ:
        camPosZ = (((bbSizeX / 2) / tan(radians(fov / 2))) + (bbSizeZ / 2)) * OVERSCAN
    else:
        camPosZ = ((((bbSizeY / 2) / tan(radians(fov / 2))) + (bbSizeZ / 2)) * aspectRatio) * OVERSCAN

    # Set Camera position
    mc.setAttr('{}.translateX'.format(CAMERA_NAME), camPosX)
    mc.setAttr('{}.translateY'.format(CAMERA_NAME), camPosY)
    mc.setAttr('{}.translateZ'.format(CAMERA_NAME), camPosZ)

    # Create Locator
    assetLocator = mc.spaceLocator(name='{}_turn_loc'.format(asset))[0]

    # Set Locator position
    mc.setAttr('{}.translateX'.format(assetLocator), bbCenterX)
    mc.setAttr('{}.translateY'.format(assetLocator), bbCenterY)
    mc.setAttr('{}.translateZ'.format(assetLocator), bbCenterZ)

    # Parent asset to locator
    mc.parent(asset, assetLocator)

    # Animate the locator
    mc.setKeyframe(assetLocator,
                   time=[0],
                   attribute='rotateY',
                   value=0,
                   outTangentType='linear',
                   inTangentType='linear')
    mc.setKeyframe(assetLocator,
                   time=[120],
                   attribute='rotateY',
                   value=360,
                   outTangentType='linear',
                   inTangentType='linear')