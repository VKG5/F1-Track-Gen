# CORE LIBRARIES
# Importing main libraries used in the code
'''
Important : We need to import bpy in every module that will be used in Blender. Blender fails to register the file as a module otherwise?!
'''
import bpy
import fastf1 as ff1
import pandas as pd
import numpy as np
import json
import random

# Visualization
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

## NOTE : PyQT5 or above is required if you want to visualize the data in 3D

import os

from . import installPythonModule as installModule
# installModule = bpy.data.texts["installPythonModule.py"].as_module()

## Checking for all libraries
def checkLibraries():
    req = ["matplotlib", "numpy", "fastf1", "pandas", "scipy", "pyqt5", "json"]

    for lib in req:
        installModule.installModule(lib)
        
    print("All required modules present :)")


## GLOBAL VARIABLES
## Use os.getcwd() instead of os.path.realpath for importing as module in Blender
# Using the latter will give the path as the Blender files location

PARENT_DIR = os.path.dirname(os.path.realpath(__file__))
# PARENT_DIR = os.getcwd()

PARENT_DIR += "\\FastF1"
CACHE_DIR = "\\FF1_Cache"


## HELPER FUNCTIONS
if(not os.path.exists(PARENT_DIR + CACHE_DIR)):
    print(f"Cache Directory doesn't exist. Creating new directory at {PARENT_DIR + CACHE_DIR}")
    os.makedirs(PARENT_DIR + CACHE_DIR)

ff1.Cache.enable_cache(PARENT_DIR + CACHE_DIR)


## CORE FUNCTIONALITY
# Getting the data from FF1 API
def getAllTrackPoints(year : int = 2024, distance_interval : int = 10, track : str = 'Melbourne') -> pd.DataFrame:
    '''
    Extracts the data points for a given year.

    Arguments:
    1. year (int, optional): The year for which the data will be scraped.
    2. distance_interval (int, optional): Distance of interpolation. The data points are scraped based on this parameter,
    and interpolated upon. A smaller number means more data and vice versa.

    Return:
    1. track_points (dictionary): Returns a dictionary with all data points for further processing.
    '''
    schedule = ff1.get_event_schedule(year)
    track_points_df = None
    found = False

    for index, race in schedule.iterrows():
        circuit_name = race['Location']
        
        if(circuit_name == track):
            # Flag for checking if dataset exists
            found = True

            # Debugging
            print(f"Processing {track} for {year}")

            '''
            get_session(year, track_name, session_name {given below})

            Session name abbreviation: 'FP1', 'FP2', 'FP3', 'Q', 'S', 'SS', 'SQ', 'R'
            Full session name: 'Practice 1', 'Practice 2', 'Practice 3', 'Sprint', 
            'Sprint Shootout', 'Sprint Qualifying', 'Qualifying', 'Race'; 
            provided names will be normalized, so that the name is case-insensitive
            '''
            session = ff1.get_session(year, circuit_name, "R")

            # Load session data
            session.load()

            # Picking a random driver from the list
            driver = random.choice(session.drivers)
            
            # Getting the laps
            laps = session.laps.pick_drivers(driver)
            fastest_lap = laps.pick_fastest()
            telemetry = fastest_lap.get_telemetry()

            distance = telemetry['Distance'].to_numpy()
            pos_x, pos_y, pos_z = telemetry['X'].to_numpy(), telemetry['Y'].to_numpy(), telemetry['Z'].to_numpy()

            # Edge Case: If there are less than 2 data points, do not process
            if(len(distance) < 2):
                print("Not enough data points in telemetry for interpolation")
                return None

            # Cubic Spline Interpolation between two points
            interp_x = interp1d(distance, pos_x, kind="cubic")
            interp_y = interp1d(distance, pos_y, kind="cubic")
            interp_z = interp1d(distance, pos_z, kind="cubic")

            # Generating new distnace values at the specified intervals
            max_distance = np.max(distance)
            new_distance = np.arange(np.min(distance), max_distance, distance_interval)

            # Interpolating the coordinates
            new_x = interp_x(new_distance)
            new_y = interp_y(new_distance)
            new_z = interp_z(new_distance)

            # Creating a dataframe for final processing
            track_points_df = pd.DataFrame({
                'distance': new_distance,
                'x': new_x,
                'y': new_y,
                'z': new_z
            })

            # Debugging
            print(f"\n===============================\nFinal Data:\n{track_points_df}\n")

    # If the required track data was not found
    if(not found):
        print(f"Error finding {track} for {year}! Check the name/try changing the year")
        return None

    return track_points_df

def draw2DPlot(df : pd.DataFrame, track : str) -> None:
    plt.figure(figsize=(10, 6))
    
    plt.plot(df['x'], df['y'], marker='o', linestyle='-', color='b', label='Track Path')

    # Adding labels and title
    plt.xlabel("X Coordinate", fontsize=12)
    plt.ylabel("Y Coordinate", fontsize=12)
    plt.title(f"2D Plot of {track}: X vs Y Coordinates", fontsize=14)

    plt.grid(True, linestyle='--', alpha=0.7)

    plt.legend()

    plt.show()

def draw3DPlot(df : pd.DataFrame, track : str) -> None:
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Normalizing the Z coordinates
    df['z'] = 0
    # df['z'] = (df['z'] - df['z'].mean())/df['z'].std()

    ax.scatter(df['x'], df['y'], df['z'], c='r', marker='o', label='Data Points')
    ax.plot(df['x'], df['y'], df['z'], color='b', linestyle='-', label='Track Path')

    # Adding labels and title
    ax.set_xlabel("X Coordinate", fontsize=10)
    ax.set_ylabel("Y Coordinate", fontsize=10)
    ax.set_zlabel("Z Coordinate", fontsize=10)
    ax.set_title(f"3D Plot of {track}: X, Y, and Z Coordinates", fontsize=14)

    ax.legend()

    plt.show()

def saveData(df : pd.DataFrame, track : str, year : int) -> str:
    if(len(df) == 0):
        print("No data to save!")
        return ''

    save_data = []
    sector_factor = len(df) // 4

    for index, data in enumerate(df.values):
        save_data.append({
            'M_SESSION' : track,
            'FRAME': index,
            'YEAR': year,
            'SECTOR': index // sector_factor if index // sector_factor < 4 else 3,
            'LAP_DISTANCE': data[0],
            'WORLDPOSX': data[1],
            'WORLDPOSY': data[2],
            'WORLDPOSZ': data[3] # TODO : Add Z coordinate normalization
        })

    if(not os.path.exists(f"{PARENT_DIR}\\Data")):
        print("Data directory does NOT exist... Creating directory...")
        os.makedirs(f"{PARENT_DIR}\\Data")

    with open(f"{PARENT_DIR}\\Data\\{track}_{year}_data.json", 'w', encoding='utf-8') as file:
        json.dump(save_data, file, indent=4)

    print(f"JSON data saved to {track}_{year}_data.json")

    return f"{PARENT_DIR}\\Data\\{track}_{year}_data.json"
