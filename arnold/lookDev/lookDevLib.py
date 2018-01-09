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

LD_PREFIX = 'lookDev'
LD_SPHERE = ['black', 'grey', 'white', 'chrome']
LD_SPHERE_COLUMN = 2

LD_TOP_GROUP = '_'.join([LD_PREFIX, 'grp'])
LD_OFFSET_GROUP = '_'.join([LD_PREFIX, 'offset_grp'])
LD_CAM_OFFSET_GROUP = '_'.join([LD_PREFIX, 'cam_offset_grp'])
LD_LIGHT_GROUP = '_'.join([LD_PREFIX, 'light_grp'])
LD_ASSET_LOCATOR = '{}_turn_loc'.format(LD_PREFIX)

LD_HIERARCHY = {LD_TOP_GROUP: {
                    LD_OFFSET_GROUP: {
                        LD_LIGHT_GROUP,
                        LD_ASSET_LOCATOR,
                        LD_CAM_OFFSET_GROUP
                        }
                    }
                }

CAMERA_NAME = '{}_camera'.format(LD_PREFIX)


def createTurnTable(asset,
                    cameraFocal=75,
                    overscan=1,
                    animEnd=120):

    # Set Current time to frame 1
    mc.currentTime(1)

    # Create turn table hierarchy
    # Create Locator
    assetLocator = mc.spaceLocator(name=LD_ASSET_LOCATOR)[0]

    # Create Camera
    if mc.objExists(CAMERA_NAME):
        mc.delete(CAMERA_NAME)
    mc.camera(focalLength=cameraFocal)
    mc.rename(CAMERA_NAME)

    mc.group()
    mc.rename(LD_CAM_OFFSET_GROUP)
    mc.select(deselect=True)
    mc.group(empty=True)
    mc.rename(LD_LIGHT_GROUP)
    mc.select([LD_CAM_OFFSET_GROUP, assetLocator], add=True)
    mc.group()
    mc.rename(LD_OFFSET_GROUP)
    mc.group()
    mc.rename(LD_TOP_GROUP)

    # Get Bounding Box Asset
    mc.select(asset)
    bbMinX, bbMinY, bbMinZ, bbMaxX, bbMaxY, bbMaxZ = mc.exactWorldBoundingBox()

    bbSizeX = bbMaxX - bbMinX
    bbSizeY = bbMaxY - bbMinY
    bbSizeZ = bbMaxZ - bbMinZ

    bbCenterX = (bbSizeX / 2) + bbMinX
    bbCenterY = (bbSizeY / 2) + bbMinY
    bbCenterZ = (bbSizeZ / 2) + bbMinZ

    # Get Camera Shape
    cameraShape = mc.listRelatives(CAMERA_NAME, children=True, type='shape')[0]
    # Get Field of View
    fov = mc.camera(cameraShape, query=True, horizontalFieldOfView=True)
    # Get Rendering Aspect Ratio
    aspectRatio = mc.getAttr('defaultResolution.deviceAspectRatio')

    # Get Camera Position

    print '\nAspect Ratio : ', aspectRatio, '\n'
    print '\nSize X : ', bbSizeX
    print 'Size Y : ', bbSizeY
    print 'Size Z : ', bbSizeZ

    print '\nSize X : ', bbSizeX/bbSizeY

    if bbSizeZ >= bbSizeY and bbSizeZ >= bbSizeX:
        camPosZ = (((bbSizeZ / 2) / tan(radians(fov / 2))) + (bbSizeX / 2)) * overscan

    elif bbSizeX >= bbSizeY and bbSizeX >= bbSizeZ:
        '''
        if bbSizeX/bbSizeY <= aspectRatio:
            camPosZ = (((bbSizeX / 2) / tan(radians(fov / 2))) + (bbSizeZ / 2)) * overscan
        else:'''
        print 'blabla'
        camPosZ = ((((bbSizeY / 2) / tan(radians(fov / 2))) + (bbSizeZ / 2)) * aspectRatio) * overscan

    else:
        print 'bloblo'
        camPosZ = ((((bbSizeY / 2) / tan(radians(fov / 2))) + (bbSizeZ / 2)) * aspectRatio) * overscan

    # Set Camera Z position
    mc.xform(LD_CAM_OFFSET_GROUP, translation=(0, 0, camPosZ))

    # Set Locator position
    mc.xform(LD_OFFSET_GROUP, translation=(bbCenterX, bbCenterY, bbCenterZ))

    # Animate the locator
    mc.playbackOptions(minTime=1)
    mc.playbackOptions(maxTime=animEnd)
    mc.playbackOptions(animationStartTime=1)
    mc.playbackOptions(animationEndTime=animEnd)

    mc.setKeyframe(assetLocator,
                   time=[1],
                   attribute='rotateY',
                   value=0,
                   outTangentType='linear',
                   inTangentType='linear')
    mc.setKeyframe(assetLocator,
                   time=[animEnd],
                   attribute='rotateY',
                   value=360,
                   outTangentType='linear',
                   inTangentType='linear')

    mc.parent(asset, LD_ASSET_LOCATOR)

    # Create polySphere
    mc.select(deselect=True)
    sphereGroupName = '_'.join([LD_PREFIX, 'sphere', 'grp'])
    mc.group(empty=True)
    mc.rename(sphereGroupName)

    column = 1
    line = 0

    for i in range(len(LD_SPHERE)):
        sphereName = '{}_{}Sphere_geo'.format(LD_PREFIX, LD_SPHERE[i])
        sphereRadius = camPosZ/100
        mc.polySphere(name=sphereName, radius=sphereRadius)
        if i % 2 == 0:
            line += 1
        if column % LD_SPHERE_COLUMN == 0:
            column = 1
        else:
            column += 1

        mc.setAttr('{}.translateY'.format(sphereName), ((sphereRadius*2) * line) + sphereRadius / 2)
        mc.setAttr('{}.translateX'.format(sphereName), ((sphereRadius*2) * column) + sphereRadius / 2)

        mc.parent(sphereName, sphereGroupName)

    # Get Bounding Box Asset
    sphereBBMinX, sphereBBMinY, sphereBBMinZ, sphereBBMaxX, sphereBBMaxY, sphereBBMaxZ = mc.exactWorldBoundingBox()

    sphereBBSizeX = sphereBBMaxX - sphereBBMinX
    sphereBBSizeY = sphereBBMaxY - sphereBBMinY
    sphereBBSizeZ = sphereBBMaxZ - sphereBBMinZ

    sphereBBCenterX = (sphereBBSizeX / 2) + sphereBBMinX
    sphereBBCenterY = (sphereBBSizeY / 2) + sphereBBMinY
    sphereBBCenterZ = (sphereBBSizeZ / 2) + sphereBBMinZ

    mc.setAttr('{}.translateX'.format(sphereGroupName), bbCenterX-(sphereBBSizeX/2))
    mc.setAttr('{}.translateY'.format(sphereGroupName), bbCenterY-(sphereBBSizeY/2))


def turnTableExist():
    lookdevNodes = mc.ls('lookDev_*')
    if lookdevNodes:
        return True
    else:
        return False


def turnTableGoodHierarchy():
    assets = mc.listRelatives(LD_ASSET_LOCATOR, children=True, type='transform')


def deleteTurnTable():

    mc.currentTime(1)
    assets = mc.listRelatives(LD_ASSET_LOCATOR, children=True, type='transform')
    mc.select(deselect=True)
    for asset in assets:
        mc.parent(asset, world=True)

    lookdevNodes = mc.ls('lookDev_*')
    mc.delete(lookdevNodes)
