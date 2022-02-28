import bpy
from math import radians
import os
# To pull the dataset off of the web (We don't require any keys or anything atm)
import requests

# Getting path
dir = os.getcwd()

# A reference to the basic functions that are present in the other script
from . import basicFunctions as basicFuncs

# Global Dictionary for storing the API Links
# The value is stored in form of a Tuple with 3 links
# (LeftData, RightData, CenterData)
# API001 - Melbourne
# API002 - Texas
# API003 - Sakhir
apiLinks = { 'api001' : ("14723197675720646148", "3447308828675135472", "6424586751601551341"),
             'api002' : ("12739104041678494733", "12959366596380051521", "9742647087467354271"),
             'api003' : ("9065767181428164173", "3370806962101808516", "14198929888436051103") }

             
''' 
Importing and Core Data Functions
'''
## The apiName is linked to the UI and we have a pre-defined dictionary for getting the data based on the API chosen
# Currently Melbourne, Texas and Sakhir (Baharain)
def importData(apiName):
    # Clearing all pre-initialized data
    basicFuncs.deleteAll()

    # Setting up the path for the data
    dataPath = "https://apigw.withoracle.cloud/formulaai/trackData/"

    # Loading the actual data
    ## Left Track Data
    leftData = (requests.get(dataPath + apiLinks[apiName][0] + "/1")).json()
    rightData = (requests.get(dataPath + apiLinks[apiName][1] + "/1")).json()
    centerData = (requests.get(dataPath + apiLinks[apiName][2] + "/1")).json()

    return leftData, rightData, centerData

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
    
def getData(apiName):
    leftData, rightData, centerData = importData(apiName)
    
    '''
    We are primarily focused on a few entries from the data points, which are 
    WorldPosX
    WorldPosY
    WorldPosZ
    Sector 
    FrameNumber
    '''
    
    # Defining the data structures for storing the data frame
    lData = []
    rData = []
    cData = []
    
    # Generating the dataframe for Left Side
    lData = insertDataIntoList(lData, leftData)
    
    # Generating the dataframe for Right Side
    rData = insertDataIntoList(rData, rightData)
    
    # Generating the dataframe for Center Side
    cData = insertDataIntoList(cData, centerData)
    
    return lData, rData, cData

# Function to sort Data based on certain parameters (Sector/Frame)
def sortData(ls):
    ## Debugging
    #print("Sorting on the basis of Sector and Frame Number")
    
    return( sorted( ls, key = lambda ls: (ls[3], ls[4]) ) )

def processData(apiName):
    # Calling the getData() function to get properly generated data
    lData, rData, cData = getData(apiName)
    
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
    lData = sortData(lData)
    rData = sortData(rData)
    cData = sortData(cData)
    
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
    
    return lData, rData, cData