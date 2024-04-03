"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase from the
data on NEOs and close approaches extracted by `extract.load_neos` and
`extract.load_approaches`.

You'll edit this file in Tasks 2 and 3.
"""
from helpers import cd_to_datetime
from helpers import datetime_to_str
import filters
from filters import AttributeFilter
from filters import UnsupportedCriterionError
from datetime import datetime

class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        desdict = {i.designation: i for i in neos}
      
        for a in approaches:
            x = a._designation
            a.neo = desdict[x]
            desdict[x].approaches.append(a)
        self.neos = neos
        self.approaches = approaches

    def get_neo_by_designation(self, designation):
        x =[]
        desdict = {i.designation: i for i in self.neos}
        if designation in desdict:
            neo = desdict[designation] if desdict[designation] else None
        else: neo = None
        return neo
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        
    def get_neo_by_name(self, name):
        x =[]
        desdict = {i.name: i for i in self.neos}
        if name in desdict:
            neo = desdict[name] 
        else:
            neo = None
        return neo
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """

    def query(self, filters=()):
        date, start_date, end_date, min_distance, max_distance, min_velocity,                     max_velocity, min_diameter, max_diameter,hazardous = filters
        
        deslist = []
        neolist = []
        
        if not any(elem is not None for elem in filters):
            for i in self.approaches:
                yield i
                
        for a in self.approaches:
            maybe = a
            deslist.append(maybe)
            if date != None:
                if isinstance(a.time, str) == False:
                    if date.__call__(a.time.date()) != True:
                        deslist.remove(maybe) 
                        continue
               
            if start_date is not None: 
                if start_date.__call__(a.time.date()) != True: 
                    deslist.remove(maybe) 
                    continue
                    
            if end_date != None:
                if end_date.__call__(a.time.date()) != True:
                    deslist.remove(maybe) 
                    continue
                    
            if a.distance is not None:
                if min_distance is not None:
                    if min_distance.__call__(a.distance) != True:
                        deslist.remove(maybe) 
                        continue
                        
                if max_distance is not None:   
                    if max_distance.__call__(a.distance) != True:
                        deslist.remove(maybe) 
                        continue
                
            if a.velocity is not None:
                if min_velocity != None: 
                    if min_velocity.__call__(a.velocity) != True: 
                        deslist.remove(maybe) 
                        continue
                        
                if max_velocity is not None:
                    if max_velocity.__call__(a.velocity) != True:
                        deslist.remove(maybe) 
                        continue
                        
            neolist = []
            neodict = {x.designation: x for x in self.neos}
            
            if a._designation in neodict:
                new = neodict[a._designation]
                if new.diameter != None:
                    if min_diameter != None: 
                        if min_diameter.__call__(new.diameter) != True:
                            deslist.remove(maybe)
                            continue
                            
                    if max_diameter is not None:
                        if max_diameter.__call__(new.diameter) != True:
                            deslist.remove(maybe)
                            continue
                            
                if new.hazardous is not None and new.hazardous != "":
                    if hazardous is not None:
                        if hazardous.__call__(new.hazardous) == False:
                            deslist.remove(maybe)
                            continue
                
                if deslist != [] and deslist is not None:
                    yield maybe 
                 
             
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaninfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
       
