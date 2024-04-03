"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json
from models import NearEarthObject, CloseApproach
from helpers import cd_to_datetime
import pandas as pd

def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    obj = []
    with open(neo_csv_path,'r') as f:
        head = next(f)
        data = csv.reader(f)
        x = 0
        for row in data:
            designation = row[3]
            name = row[4]
            diameter = pd.to_numeric(row[15])
            if row[7] == None:
                hazardous = None 
            if row[7] == "":   
                hazardous = False
            if row[7] == "Y":
                hazardous = True  
            if row[7] == "N":
                hazardous = False 
            name1 = NearEarthObject(designation = designation, name = name, diameter =                      diameter, hazardous = hazardous,approaches = [x])
            obj.append(name1)
    return obj

def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    obj = [] 
    with open(cad_json_path, 'r') as f:
        data = json.load(f)
        x = 0
        for rock in data['data']:
            designation = rock[0]
            time = rock[3]
            distance = rock[4]
            distance = pd.to_numeric(distance)
            velocity = rock[7]
            velocity = pd.to_numeric(velocity)
            obj.append(CloseApproach(designation =designation, time  = time, distance =                         distance, velocity = velocity)) 
           
    return obj
