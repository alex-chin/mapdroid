# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 11:09:51 2018

@author: Alex
"""

import pyproj
from node import node

ellipsis = 'SGS85'
step = 50
is_log = False

class PathMatrix:
    
#   конструктор
    def __init__ (self, start, end):
        self.start = start
        self.end = end
        self.geod = pyproj.Geod(ellps=ellipsis)
        
#   расчитать дистанцию между точками
    def calc_dist(self):
        lons1, lats1 = self.start.coord()
        lons2, lats2 = self.end.coord()
        self.forward_azimuth, self.back_azimuth, self.distance = \
            self.geod.inv(lons1, lats1, lons2, lats2)

        return self.distance
    
#    построить гео сетку
    def matrix(self):
        self.calc_dist()
        self._log_head()
        # количество шагов + 1
        num_step = self.distance // step + 1
        # длина маршрута
        self.step_long = num_step
        distance_grid = num_step * step
        # конечная точка с зазором
        lons, lats, _ = self.geod.fwd(self.start.lons, self.start.lats, self.forward_azimuth, distance_grid)
        self.end_grid = node(lons, lats)
        # список точек с шагом step в направлении конечной точки
        npts1 = self.geod.npts(self.start.lons, self.start.lats, lons, lats, num_step -1)
        npts1.extend([(self.end_grid.lons, self.end_grid.lats)])
        # количество точек в стороны
        num_step2 = num_step // 2
        # азимуты вправо и влево
        right_az = self.forward_azimuth + 90
        left_az = self.forward_azimuth - 90
        
        npts = [(self.start.lons, self.start.lats)]
        npts.extend(npts1)
        list = []
        
        self._log_prepare(num_step, self.end_grid, npts)
        
        for (dlons, dlats) in npts:
            n1 = node(dlons, dlats)
            l_list = self._npts(n1, left_az, num_step2)
            r_list = self._npts(n1, right_az, num_step2)
            l_list.reverse()
            l_list.extend([(dlons, dlats)])
            l_list.extend(r_list)
            list.append(l_list) 
            
        self._log_matrix(list)
        return list
            
        
    def _npts(self, node, azimuth, num):
        distance = step * num
        lons, lats = node.coord()
        elons, elats, _ = self.geod.fwd(lons, lats, azimuth, distance)
        npts = self.geod.npts(lons, lats, elons, elats, num - 1)
        npts.extend([(elons, elats)])
        return npts
    
    def _log_head(self):
        if not is_log:
            return
        self.start.print("Начало")
        self.end.print("Конец")
        print("Прямой азимут = ", self.forward_azimuth)
        print("Обратный азимут = ", self.back_azimuth)
        print("Дистанция = ", self.distance)
       
    def _log_prepare(self, num_step, end_grid, npts):
        if not is_log:
            return
        print("===================")
        print("Количество шагов = ", num_step)
        print("Конечная точка")
        end_grid.print()
        print("====Осевая=========")
        i=1
        for lons, lats in npts:
            print("{} : {:f}, {:f}".format(i, lats, lons))  
            i+=1
    
    def _log_matrix(self, matrix):
        if not is_log:
            return
        print("======матрица=====")
        i=1
        for line in matrix:
            print(i,". Строка")
            i+=1
            for lons, lats in line:
                print(" : {:f}, {:f}".format( lats, lons))
        
        
    