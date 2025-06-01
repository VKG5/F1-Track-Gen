import bpy
import os
import random
import re

# Getting the directory name for importing the track files
dir = os.path.dirname(os.path.realpath(__file__))


'''Main Functions'''
# To import/append the data from another .blend file
def importCollection(name):
    filePath = dir+"\\Base.blend"
    fileType = "Collection"
    collectionName = name
    
    bpy.ops.wm.append(
        filepath = os.path.join(filePath, fileType, collectionName),
        directory = os.path.join(filePath, fileType),
        filename = collectionName
    )
    
    print("Successfully imported the collection %s!" % name)
    
# To generate fillers around the track
def placeFiller(name, flagOffset, displacement_factor):
    activeObj = bpy.data.scenes['Scene'].objects[name]
    
    activeObj.location[1] = flagOffset
    
    # Adding modifiers
    arrayModifierName = name+'Array'
    curveModifierName = name+'Curve'
    activeObj.modifiers.new(arrayModifierName, type = 'ARRAY')
    activeObj.modifiers.new(curveModifierName, type = 'CURVE')
    
    # Changing the fit type and offsets 
    activeObj.modifiers[arrayModifierName].fit_type = 'FIT_CURVE'
    activeObj.modifiers[arrayModifierName].curve = bpy.data.objects["trackCurve"]
    activeObj.modifiers[arrayModifierName].relative_offset_displace[0] = displacement_factor
    
    activeObj.modifiers[curveModifierName].object = bpy.data.objects["trackCurve"]
    
    # Applying the transforms (All three)
    bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    
def removePrevFillers():
    for coll in bpy.data.collections: 
        ## Debugging
        print(coll.name)
        
        # If it is a valid collection, then remove it
        if(coll):
            # Checking the name of the collection
            if( coll.name.find('Flag') != -1 or coll.name.find('Poles') != -1 ):
                print(coll.name)
                bpy.data.collections.remove(coll)
    
    # Clearing the project (Purging)
    bpy.ops.outliner.orphans_purge(do_local_ids=True, do_linked_ids=True, do_recursive=True)
    
# Main function to add the fillers!
def addFillers(flagOff, poleOff, deletePrev, flagDis, poleDis):
    ## Debugging
    #print(lengthOfTrack)
    
    ## If the delete Previous Fillers flag is true, we will delete those colelction
    if(deletePrev):
        removePrevFillers()
        
    # List of collections that need to be imported
    collNames = ['Flag', 'Poles']

    # Importing the collections
    for col in collNames:
        importCollection(col)
        
    # Placing the flags
    # Going through the collection and placing flags at random offsets
    flagOffset = flagOff
    poleOffset = poleOff
    for flag in bpy.data.collections[collNames[0]].objects:
        print(flag.name) 
        placeFiller(flag.name, flagDis, random.uniform(0.5, 2.5)*flagOffset)

    # Placing the poles
    placeFiller('Pole', poleDis, poleOffset)    
        
    print("Successfully added fillers!")
    