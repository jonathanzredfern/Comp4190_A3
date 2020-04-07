__author__ = 'Jacky Baltes <jacky@cs.umanitoba.ca>'

import matplotlib.pyplot as plt
import numpy as np
import random

class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def CalculateOverlap(self, obs):
        #print('CalculateOverlap {0},{1}->{2},{3} with {4},{5}->{6},{7}'.format(self.x, self.y, self.x + self.width, self.y+self.height, obs.x, obs.y, obs.x + obs.width, obs.y + obs.height) )
        if ( self.x < obs.x ):
            min = self.x
        else:
            min = obs.x
        if ( ( self.x + self.width ) < ( obs.x + obs.width ) ):
            max = obs.x + obs.width
        else:
            max = self.x + self.width
        overlapX = ( max - min ) - ( self.width + obs.width )
        #print('CalculateOverlap max', max, 'min', min, 'overlapX', overlapX)
        if ( self.y < obs.y ):
            min = self.y
        else:
            min = obs.y
        if ( ( self.y + self.height ) < ( obs.y + obs.height ) ):
            max = obs.y + obs.height
        else:
            max = self.y + self.height
        overlapY =  ( max - min ) - ( self.height + obs.height )
        #print('CalculateOverlap max', max, 'min', min, 'overlapY', overlapY)
        if ( overlapX < 0 ) and (overlapY < 0 ):
            overlap = overlapX * overlapY
        else:
            overlap = 0.0
        #print('CalculateOverlap returns {0}'.format(overlap))
        return overlap


    def IsNeighbor(self, node):
        min_x1 = self.x - 0.01
        max_x1 = self.x + self.width + 0.01
        max_y1 = self.y + self.height + 0.01
        min_y1 = self.y - 0.01

        min_x2 = node.x
        max_x2 = node.x + node.width
        max_y2 = node.y + node.height
        min_y2 = node.y

        return (min_x1 < max_x2 and max_x1 > min_x2 and max_y1 > min_y2 and min_y1 < max_y2)

class Obstacle(Rectangle):
    def __init__(self, x, y, width, height, color = None ):
        super().__init__( x, y, width, height)
        self.color = color
        if ( color is not None ):
            self.patch = plt.Rectangle((self.x, self.y), self.width, self.height, facecolor=color, edgecolor='#202020')

class PathPlanningProblem:
    def __init__(self, width, height, onum, owidth, oheight):
        self.width = width
        self.height = height
        self.obstacles = self.CreateObstacles(onum, owidth, oheight)

    def CreateObstacles(self, onum, owidth, oheight):
        obstacles = []

        while( len(obstacles) < onum ):
            x = random.uniform(0.0, self.width)
            y = random.uniform(0.0, self.height)
            w = random.uniform(1.0, owidth)
            h = random.uniform(1.0, oheight)
            if ( x + w ) > self.width:
                w = self.width - x
            if ( y + h ) > self.height:
                h = self.height - y
            obs = Obstacle(x,y, w, h, '#808080')
            found = False
            for o in obstacles:
                if ( o.CalculateOverlap(obs) > 0.0 ):
                    found = True
                    break
            if ( not found ):
                obstacles = obstacles + [obs]
        return obstacles

    def CreateProblemInstance(self):
        found = False
        while (not found ):
            ix = random.uniform(0.0, self.width)
            iy = random.uniform(0.0, self.height)

            oinitial = Obstacle(ix, iy, 0.1, 0.1 )
            found = True
            for obs in self.obstacles:
                if (obs.CalculateOverlap(oinitial) > 0.0):
                    found = False
                    break

        found = False
        while (not found ):
            gx = random.uniform(0.0, self.width)
            gy = random.uniform(0.0, self.height)

            ogoal = Obstacle(gx, gy, 0.1, 0.1 )
            found = True
            for obs in self.obstacles:
                if ( obs.CalculateOverlap( ogoal ) > 0.0 ):
                    found = False
                    break
            if (oinitial.CalculateOverlap(ogoal) > 0.0):
                found = False

        return oinitial, ogoal

    def CheckOverlap(self, r):
        overlap = False
        for o in self.obstacles:
            if (r.CalculateOverlap(o) > 0 ):
                overlap = True
                break
        return overlap

    def CalculateCoverage( self, path, dim ):
        x = np.arange(0.0, self.width, dim )
        y = np.arange(0.0, self.height, dim )
        counts = np.zeros((len(y),len(x)))
        for p in path:
            i = int(p[1]/dim)
            j = int(p[0]/dim)
            counts[j][i] = counts[j][i] + 1
        return (x,y,counts)


