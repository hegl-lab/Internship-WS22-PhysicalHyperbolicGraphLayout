import cairo
import math
import PoincareDiskModel
import Geometry
import euclideanGeometry
import numpy as np


pdm = PoincareDiskModel.PoincareDiskModel([0, 0])
eG = euclideanGeometry.EuclideanGeometry([0, 0])


class DrawPoincareDisk():
    def __init__(self, size):
        '''Initiate size of the image, the radius of the PDM and the framework for the image'''
        self.n = size
        self.radius = self.n/2*0.9
        self.ps = cairo.SVGSurface("PoincareDiskModel.svg", self.n, self.n)
        self.cr = cairo.Context(self.ps)
        self.defaultLineWidth = 0.005*self.radius
        self.defaultPointSize = 0.0075*self.radius
        self.defaultColour = [0, 0, 0]
        self.drawPDM()

    def transform(self, Point):
        '''Takes a point from the unitcircle and retunrns transformed  image coordinates as an array'''
        xy = Point.euclPoint
        return [(xy[0]+1)*self.radius + self.n/2 - self.radius, self.n - (xy[1]+1)*self.radius - (self.n/2 - self.radius)]

    def drawPoint(self, Point, colour1=None, colour2=None, colour3=None, pointSize=None):
        '''Takes a point and draws it into the image'''

        # Setting up colour and pointsize
        if pointSize is None:
            pointSize = self.defaultPointSize
        if colour1 is None:
            self.cr.set_source_rgb(
                self.defaultColour[0], self.defaultColour[1], self.defaultColour[2])
        else:
            self.cr.set_source_rgb(colour1, colour2, colour3)

        #Drawing the Point
        self.cr.arc(self.transform(Point)[0], self.transform(
            Point)[1], pointSize, 0, 2*math.pi)
        self.cr.fill()
        return

    def drawGeodesic(self, Point1, Point2, colour1=0, colour2=0, colour3=0, lineWidth=None):
        '''Drawing the geodesic of two points'''
        # Setting up line width and colour
        if lineWidth is None:
            self.cr.set_line_width(self.defaultLineWidth)
        else:
            self.cr.set_line_width(lineWidth)
        if colour1 is None:
            self.cr.set_source_rgb(
                self.defaultColour[0], self.defaultColour[1], self.defaultColour[2])
        else:
            self.cr.set_source_rgb(colour1, colour2, colour3)

        # Calculating the ideal circle
        C, r = pdm.getGeodesic(Point1, Point2)
        
        #Case, where the geodesic is a straight line through the origin
        if r == 0:
            self.cr.set_source_rgb(
                255, 0, 0)
            self.cr.move_to(self.transform(Point1)[
                            0], self.transform(Point1)[1])
            self.cr.line_to(self.transform(Point2)[
                            0], self.transform(Point2)[1])
            self.cr.stroke()
        
        #Case, where the geodesic is a arc
        else:
            angle1 = eG.angle_between(eG.direction(C, Point1), Geometry.Point([1, 0]))
            angle2 = eG.angle_between(eG.direction(C, Point2), Geometry.Point([1, 0]))
            angle12 = eG.angle_between(eG.direction(C, Point1), eG.direction(C, Point2)) 

            #Checking all cases
            if C.euclPoint[1]>Point1.euclPoint[1] and C.euclPoint[1]>Point2.euclPoint[1]:
                if angle1 > angle2: 
                    angle1, angle2 = angle2, angle1
                angle12 += angle1 
            elif C.euclPoint[1]>Point1.euclPoint[1] and C.euclPoint[1]<Point2.euclPoint[1]:
                angle12 = 2*math.pi  - angle2  
            elif C.euclPoint[1]<Point1.euclPoint[1] and C.euclPoint[1]>Point2.euclPoint[1]:
                angle1, angle2 = angle2, angle1
                angle12 = 2*math.pi - angle2
            elif C.euclPoint[1]<Point1.euclPoint[1] and C.euclPoint[1]<Point2.euclPoint[1]:
                if angle1 < angle2: angle1, angle2 = angle2, angle1
                angle1 = 2*math.pi - angle1 
                angle12 += angle1 

            #Making sure, that it draws the right side of the arc    
            if angle12 - angle1 > math.pi : angle1, angle12 = angle12, angle1

            #Drawing the arc
            self.cr.arc(self.transform(C)[0], self.transform(C)[1], r*self.radius, angle1, angle12)
            self.cr.stroke()
        return

    def drawDirection(self, Point, Direction, colour1=0, colour2=0, colour3=0, lineWidth=None):
        '''Takes a starting point and a direction (including scaling) and draws it'''
        # Setting up line width and colour
        if lineWidth is None:
            self.cr.set_line_width(self.defaultLineWidth)
        else:
            self.cr.set_line_width(lineWidth)
        if colour1 is None:
            self.cr.set_source_rgb(
                self.defaultColour[0], self.defaultColour[1], self.defaultColour[2])
        else:
            self.cr.set_source_rgb(colour1, colour2, colour3)

        #Drawing the line
        self.cr.move_to(self.transform(Point)[
            0], self.transform(Point)[1])
        self.cr.line_to(self.transform(Point+Direction)[
            0], self.transform(Point+Direction)[1])
        self.cr.stroke()
        return

    def drawPDM(self):
        '''Draws the PDM including background'''
        # creating background
        self.cr.set_source_rgb(255, 255, 255)
        self.cr.rectangle(0, 0, self.n, self.n)
        self.cr.fill()
        self.cr.set_line_width(self.defaultLineWidth)

        # creating disk
        self.cr.set_source_rgb(0, 0, 0)
        self.cr.arc(self.n/2, self.n/2, self.radius, 0, 2*math.pi)
        self.cr.stroke()

        # creating origin
        self.drawPoint(Geometry.Point([0, 0]))
        return

    def main(self):
        p1 = pdm.randomPoint(1)
        p2 = pdm.randomPoint(1)
        self.drawPoint(p1)
        self.drawPoint(p2)
        self.drawGeodesic(p1, p2)
        return

    def plotGraph(self, graph):
        '''Takes a List of '''



c = DrawPoincareDisk(50)
for i in range(60): c.main()
