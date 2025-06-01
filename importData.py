import bpy
from math import radians
import os
import pandas as pd
import numpy as np

# Getting path
dir = os.path.dirname(os.path.realpath(__file__))

# A reference to the basic functions that are present in the other script

# from . import basicFunctions as basicFuncs
basicFuncs = bpy.data.texts["basicFunctions.py"].as_module()

# from . import f1Info as f1Info
f1Info = bpy.data.texts["f1Info.py"].as_module()
             
''' 
Importing and Core Data Functions
'''
def importData(apiName):
    # Clearing all pre-initialized data
    basicFuncs.deleteAll()

    # TODO : Import data using FastF1 and adjust for current code
    data = f1Info.getAllTrackPoints(2024, 10, 'Melbourne')
    f1Info.saveData(data, 'Melbourne', 2024)

    # Loading the actual data
    ## Left Track Data
    # TODO : Read the saved json from the cache
    centerData = []

    return centerData

# Just to avoid redundant for loops in the subsequent function
def insertDataIntoList(ls, js):
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
    
def getData(apiName) -> list:
    centerData = importData(apiName)
    
    '''
    We are primarily focused on a few entries from the data points, which are 
    WorldPosX
    WorldPosY
    WorldPosZ
    Sector 
    FrameNumber
    '''
    
    # Defining the data structures for storing the data frame
    cData = []
    
    # Generating the dataframe for Center Side
    cData = insertDataIntoList(cData, centerData)
    
    return cData

# Function to sort Data based on certain parameters (Sector/Frame)
def sortData(ls):
    ## Debugging
    #print("Sorting on the basis of Sector and Frame Number")
    
    return( sorted( ls, key = lambda ls: (ls[3], ls[4]) ) )

def processData(apiName) -> list:
    # Calling the getData() function to get properly generated data
    # cData = getData(apiName)
    TRACK = 'Melbourne'
    YEAR = 2024

    f1Info.checkLibraries()
    track_points = f1Info.getAllTrackPoints(2024, 10, 'Melbourne')
    
    if(track_points is not None):
        print(f"Successfully fetched data for {YEAR}, {TRACK}")

    file_path = f1Info.saveData(track_points, TRACK, YEAR)
    
    '''
    Data is stored in the following format:
    
    lData [index] = Index to Dataframe (Tuple in this case) which contains 5 subitems
    
    lData [index][0] = 1st index within Tuple is the WorldPosX
    lData [index][1] = 2nd index within Tuple is the WorldPosY
    lData [index][2] = 3rd index within Tuple is the WorldPosZ
    lData [index][3] = 4th index within Tuple is the Sector
    lData [index][4] = 5th index within Tuple is the FrameNumber
    '''
    ## Debugging
    #print("L\nR\nC : %s\n%s\n%s" % (lData, rData, cData))
    
    # Sorting the data
    # cData = sortData(cData)
    
    '''
    The datasets are inconsistent
    lData starts at 1709 and ends at 5910
    cData starts at 512 and ends at 4605
    rData starts at 512 and ends at 5208
    '''
    ## Debugging
    #print("\nThe content of lData are as follows:")
    #for row in lData:
    #    print(row)
        
    #print("L, R, bpy.context : %s, %s, %s" % (lData[0], rData[0], cData[0]))

    print("Data import and pre-processing done!")
    print("File saved at: %s" % file_path)
    
    return []