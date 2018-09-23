# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 11:15:59 2018

@author: Alex
"""

class node:
    
    def __init__(self, lons, lats):
        self.lons = lons
        self.lats = lats
        
    def print(self, str=''):
        print(str, ': ', self.lats, ", ", self.lons)
        
    def coord(self):
        return self.lons, self.lats
        