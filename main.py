# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 08:23:53 2018

@author: Alex
"""
from node import node
from path_matrix import PathMatrix
from route_grid import routeGrid
from route_grid import onegrid

start = node(37.650028, 55.947828)
#end = node(37.648277, 55.949082)

end = node(37.647544, 55.949747)

# создать объект построения гео сетки
matrix = PathMatrix(start, end)

# построить сетку
grid_geo = matrix.matrix()

rows = len(grid_geo)
cols = len(grid_geo[0])
print("Строк = {}, Столбцов = {} ".format(rows, cols))

# построить исходную сетку препятствий - все 1
grid_shema = onegrid.fill(rows=rows, cols=cols)

# установить препятствия
grid_shema[2][3] = 0
grid_shema[2][4] = 0
grid_shema[2][5] = 0
grid_shema[2][6] = 0

# создать объект построения маршрута
routeG = routeGrid(grid=grid_shema)

# построить маршрут
path = routeG.route()

 
print("Карта")
print(routeG.str())


print("Маршрут")
# отобразить путь на геосетку
for x, y in path:
    lons1, lats1 = grid_geo[y][x]
    print("{:f}, {:f}".format(lats1, lons1))