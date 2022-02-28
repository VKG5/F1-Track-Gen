import bpy
import os
from mathutils import Vector

from . import importData as getData

# Getting the directory name for importing the track files
dir = os.path.dirname(os.path.realpath(__file__))

# assign the point coordinates to the spline points
def generatePoints(sector, cData, crv, spline):
    
    for p, new_co in zip(spline.points, cData):
        if(new_co[3] == sector):              
            posX = new_co[0]
            posY = new_co[1]
            posZ = new_co[2]    
            p.co = ([posX, posY, posZ] + [1.0]) # (add nurbs weight)

def generateCurve(val, apiName):
    lData, rData, cData = getData.processData(apiName)

    print("\nDirectory: %s\n" % dir)
    
    # make a new curve
    crv = bpy.data.curves.new('crv', 'CURVE')
    crv.dimensions = '3D'

    # make a new spline in that curve
    spline = crv.splines.new(type='NURBS')

    # a spline point for each point
    spline.points.add(len(cData)-1) # theres already one point by default
    
    startSect = 1
    stopSect = val
    
    # Generating the points on the curve
    for sector in range(startSect - 1, stopSect):
        generatePoints(sector, cData, crv, spline)
        
    # make a new object with the curve
    obj = bpy.data.objects.new('trackCurve', crv)
    bpy.context.collection.objects.link(obj)
    
    ## Debugging
    print("Curve successfully generated!")
    
# To import the track data from another .blend file
def importTrack():
    filePath = dir+"\\Base.blend"
    fileType = "Collection"
    collectionName = "TrackCollection"
    
    bpy.ops.wm.append(
        filepath = os.path.join(filePath, fileType, collectionName),
        directory = os.path.join(filePath, fileType),
        filename = collectionName
    )
    
    print("Successfully imported the track presets!")
    
def addFitTrack(trackName):
    # Selecting the already added Track(s)
    bpy.context.scene.view_layers['View Layer'].objects.active = bpy.data.objects[trackName]
    
    # Getting reference to the active object
    activeObj = bpy.context.active_object
    
    # Initializing the names of the modifiers
    # 2 main modifiers will be used : Array and Curve
    arrayModifierName = 'trackArray'
    curveModifierName = 'trackCurve'
    activeObj.modifiers.new(arrayModifierName, type = 'ARRAY')
    activeObj.modifiers.new(curveModifierName, type = 'CURVE')
    
    activeObj.modifiers[arrayModifierName].fit_type = 'FIT_CURVE'
    activeObj.modifiers[arrayModifierName].curve = bpy.data.objects["trackCurve"]
    
    activeObj.modifiers[curveModifierName].object = bpy.data.objects["trackCurve"]
    
    # Applying the transforms (All three)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
    ## Debugging
    print("Successfully generated the Track!!")
    
# Function for placing mesh along the curve generated above
def generateTrack(val, trackName, apiName):
    # Will generate the curve with the name of "trackCurve"
    generateCurve(val, apiName)
    
    # Importing the track(s)
    importTrack()
    
    activeTrack = trackName
    # Adding the track/object and fitting it onto the curve
    addFitTrack(activeTrack)
    