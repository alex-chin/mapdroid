# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 17:37:43 2018

@author: Alex
"""

from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder

class onegrid():
    def fill(rows, cols):
       return [[1] * rows for i in range(cols)]  

class routeGrid():
    def __init__(self, grid):
        self.grid = Grid(matrix=grid)
        rows = len(grid)
        cols = len(grid[0])
        self.node_start = self.grid.node(cols // 2, 0)
        self.node_end = self.grid.node(cols // 2, rows - 1) 
    
    def route(self):
        finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle)
        self.path, self.runs = finder.find_path(self.node_start, self.node_end, self.grid)
        return self.path
    
    def str(self):
        return self.grid.grid_str(path=self.path, start=self.node_start, end=self.node_end)
    