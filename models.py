"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted from the
data files from NASA, so these objects should be able to handle all of the
quirks of the data set, such as missing names and unknown diameters.

You'll edit this file in Task 1.
"""
from helpers import cd_to_datetime, datetime_to_str

class NearEarthObject:
    
    def __init__(self, **info):
        self.designation = info['designation'] if info['designation'] else ''
        self.name = info['name'] if info['name'] else  None
        self.diameter  = info['diameter'] if info['diameter'] else None
        self.hazardous = info['hazardous'] if info['hazardous'] != None  else  None
        self.approaches = []
        
    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        full = self.name + ": " + self.designation if self.name != None else  self.designation
        return full

    def __str__(self):
        """Return `str(self)`."""
        name = self.fullname
        diameter = float(self.diameter)
        bad = 'is not hazardous' if self.hazardous == False else 'is very bad hazardous'
        return f"{name}:A NearEarthObject with a diameter of {diameter:.3f} and {bad}."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, "
                f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})")
    
    def serialize(self, filetype, fieldnames):
        """ Format output of csv and json files """
        if filetype == 'csv':
            csvneo = {}
            csvneo[fieldnames[0]] = datetime_to_str(self.time)
            csvneo[fieldnames[1]] = float(self.distance)
            csvneo[fieldnames[2]] = float(self.velocity)
            csvneo[fieldnames[3]] = str(self.designation)
            csvneo[fieldnames[4]] = str(self.name) if self.name else ""
            csvneo[fieldnames[5]] = float(self.diameter) if self.diameter else float('nan')
            csvneo[fieldnames[6]] = self.hazardous
            return csvneo
        if filetype == 'json':
            jsonneo = {fieldnames[0] : datetime_to_str(self.time), 
                      fieldnames[1] : float(self.distance), 
                      fieldnames[2] : float(self.velocity), 
                      "neo" : {fieldnames[3]: str(self.designation), 
                               fieldnames[4] : str(self.name), 
                               fieldnames[5] : float(self.diameter), 
                               fieldnames[6] : self.hazardous}}
            return jsonneo
                             
     
class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    
    def __init__(self, **info):
        timelist = []
        self._designation = info['designation'] if info['designation'] else None      
        if cd_to_datetime(info['time']) in timelist:
            self.time = info['time']
        else:
            self.time = cd_to_datetime(info['time']) if info['time'] else  None
            timelist.append(self.time)
        self.distance = info['distance'] if info['distance'] else None
        self.velocity = info['velocity'] if  info['velocity'] else None
        self.neo  =   None
        
    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object. While a
        `datetime` object has a string representation, the default representation
        includes seconds - significant figures that don't exist in our input
        data set.

        The `datetime_to_str` method converts a `datetime` object to a
        formatted string that can be used in human-readable representations and
        in serialization to CSV and JSON files.
        """
        newtime = datetime_to_str(self.time)
        return newtime
    
    @property
    def fullname(self):
        full = self.neo.name + ": " + self._designation if self.neo.name != None else                     self._designation

    def __str__(self):
        """Return `str(self)`."""
        
        name = self.fullname
        time = self.time_str
        
        return f"At {time}, NEO {name} approachs the earth at a distance of {self.distance:.3f} and velocity of {self.velocity:.3f}."

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(designation = {self._designation}, time={self.time_str!r}, distance={self.distance:.2f}, velocity={self.velocity:.2f}, neo={self.neo!r}")
    
    def serialize(self, filetype, fieldnames):
        """ Format output of csv and json files """
        if filetype == 'csv':
            csvneo = {}
            csvneo[fieldnames[0]] = datetime_to_str(self.time) if self.time else ""
            csvneo[fieldnames[1]] = float(self.distance)
            csvneo[fieldnames[2]] = float(self.velocity)
            csvneo[fieldnames[3]] = str(self._designation)
            csvneo[fieldnames[4]] = str(self.neo) if self.neo else ""
            csvneo[fieldnames[5]] = float(self.neo.diameter) if self.neo.diameter else                                                 float('nan')
            csvneo[fieldnames[6]] = self.neo.hazardous
            return csvneo
    
        if filetype == 'json':
            jsonneo = {fieldnames[0] : datetime_to_str(self.time), 
                       fieldnames[1] : float(self.distance), 
                       fieldnames[2] : float(self.velocity), 
                       "neo" : {fieldnames[3]: str(self._designation), 
                                fieldnames[4] : str(self.neo), 
                                fieldnames[5] : float(self.neo.diameter), 
                                fieldnames[6] : self.neo.hazardous}}
            return jsonneo