import bpy
from math import radians
import os
import pandas as pd
import numpy as np
import json

# A reference to the basic functions that are present in the other script

from . import basicFunctions as basicFuncs
# basicFuncs = bpy.data.texts["basicFunctions.py"].as_module()

from . import f1Info as f1Info
# f1Info = bpy.data.texts["f1Info.py"].as_module()
             
''' 
Importing and Core Data Functions
'''
# Just to avoid redundant for loops in the subsequent function
def insertDataIntoList(ls, file_path):
    # Load the JSON data from the file path
    with open(file_path, 'r') as file:
        js = json.load(file)

    # Generating the dataframe for Left Side
    for i in js:
        posX = i['WORLDPOSX']
        posY = i['WORLDPOSY']
        posZ = i['WORLDPOSZ']
        sector = i['SECTOR']
        frame = i['FRAME']
        
        ls.append((posX, posY, posZ, sector, frame))
        
        ## Debugging
        #print("x, y, z, s, f : %s, %s, %s, %s, %s" % (posX, posY, posZ, sector, frame))
        
    return ls
    
def getData(_params) -> list:
    # Clearing all pre-initialized data
    basicFuncs.deleteAll()

    TRACK = _params['track']
    YEAR = _params['year']

    f1Info.checkLibraries()
    track_points = f1Info.getAllTrackPoints(YEAR, 10, TRACK)
    
    if(track_points is not None):
        print(f"Successfully fetched data for {YEAR}, {TRACK}")

    file_path = f1Info.saveData(track_points, TRACK, YEAR)
    print("File saved at: %s" % file_path)
    
    cData : list[tuple[float, float, float, int, int]] = []

    '''
    We are primarily focused on a few entries from the data points, which are 
    WorldPosX
    WorldPosY
    WorldPosZ
    Sector 
    FrameNumber
    '''
    # Inserting data into list for further processing
    insertDataIntoList(cData, file_path)
    
    return cData

# Function to sort Data based on certain parameters (Sector/Frame)
def sortData(ls):
    ## Debugging
    #print("Sorting on the basis of Sector and Frame Number")
    
    return( sorted( ls, key = lambda ls: (ls[3], ls[4]) ) )

def processData(_params) -> list:
    # Calling the getData() function to get properly generated data
    cData = getData(_params)
    
    '''
    Data is stored in the following format:
    
    lData [index] = Index to Dataframe (Tuple in this case) which contains 5 subitems
    
    lData [index][0] = 1st index within Tuple is the WorldPosX
    lData [index][1] = 2nd index within Tuple is the WorldPosY
    lData [index][2] = 3rd index within Tuple is the WorldPosZ
    lData [index][3] = 4th index within Tuple is the Sector
    lData [index][4] = 5th index within Tuple is the FrameNumber
    '''
    # Sorting the data
    cData = sortData(cData)

    print("Data import and pre-processing done!")

    return cData
