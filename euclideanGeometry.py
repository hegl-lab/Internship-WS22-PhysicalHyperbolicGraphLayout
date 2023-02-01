import Geometry
import numpy as np
import random
import cairo
import math


class EuclideanGeometry(Geometry.Geometry):

    def translate(self, pa, direct):
        return pa + direct

    def getDistance(self, pa, pb):
        dist = 0
        for index, x in enumerate(pa.euclPoint):
            dist = dist + (pa.euclPoint[index] - pb.euclPoint[index])**2
        dist = np.sqrt(dist)
        return dist

    def direction(self, pa, pb, dummy=None):
        direct = []
        for index, x in enumerate(pa.euclPoint):
            direct.append(pb.euclPoint[index] - pa.euclPoint[index])
        return Geometry.Point(direct)

    def paralleltransport(direct, pa, pb):
        return direct

    def getOrigin(self):
        return self.origin

    def unit_vector(self, direct):
        """ Returns the unit vector of the vector.  """
        return direct / np.linalg.norm(direct.euclPoint)

    def angle_between(self, v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'"""
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u.euclPoint, v2_u.euclPoint), -1.0, 1.0))

    def randomPoint(self, range=1000):
        return Geometry.Point([random.randint(-range, range), random.randint(-range, range)])

    def getTangent(self, center, pa):
        tangent = self.direction(center, pa)
        tangent.euclPoint[0], tangent.euclPoint[1] = tangent.euclPoint[1], - \
            tangent.euclPoint[0]
        return tangent


    def initiateImage(self, inputRadius, imageSize, name, defaultRGBColour, defaultLineWidth, defaultPointSize):
        '''Draws the coordinate system including background'''
        #Initiate size of the image, the radius of the PDM and the framework for the image
        self.n = imageSize
        self.radius = self.n/2*0.9
        self.ps = cairo.SVGSurface(name, self.n, self.n)
        self.cr = cairo.Context(self.ps)
        self.inputRadius = inputRadius

        #initiate default values
        self.defaultLineWidth = defaultLineWidth*self.radius
        self.defaultPointSize = defaultPointSize*self.radius
        self.defaultRGBColour = defaultRGBColour
        
        # creating background
        self.cr.set_source_rgb(255, 255, 255)
        self.cr.rectangle(0, 0, self.n, self.n)
        self.cr.fill()
        self.cr.set_line_width(self.defaultLineWidth)

        # creating origin
        self.drawPoint(self.origin)
        return

    def transform(self, Point):
        '''Takes a point from the coordinate system and returns transformed image coordinates as an array'''
        xy = Point.euclPoint
        return [((xy[0]+self.inputRadius)*self.radius)/self.inputRadius + self.n/2 - self.radius, self.n/2 - ((xy[1]+self.inputRadius)*self.radius)/self.inputRadius + self.radius]

    def drawPoint(self, Point, RGBcolour=None, pointSize=None):
        # Setting up colour and pointsize
        if pointSize is None:
            pointSize = self.defaultPointSize
        if RGBcolour is None:
            self.cr.set_source_rgb(*self.defaultRGBColour)
        else:
            self.cr.set_source_rgb(*RGBcolour)

        #Drawing the Point
        self.cr.arc(self.transform(Point)[0], self.transform(
            Point)[1], pointSize, 0, 2*math.pi)
        self.cr.fill()
        return


    def drawGeodesic(self, Point1, Point2, RGBcolour=None, lineWidth=None):
        if lineWidth is None:
            self.cr.set_line_width(self.defaultLineWidth)
        else:
            self.cr.set_line_width(lineWidth)
        if RGBcolour is None:
            self.cr.set_source_rgb(*self.defaultRGBColour)
        else:
            self.cr.set_source_rgb(*RGBcolour)

        self.cr.move_to(self.transform(Point1)[0], self.transform(Point1)[1])
        self.cr.line_to(self.transform(Point2)[0], self.transform(Point2)[1])
        self.cr.stroke()
        return

    def drawDirection(self, Point, Direction, RGBcolour=None, lineWidth=None):
        if lineWidth is None:
            self.cr.set_line_width(self.defaultLineWidth)
        else:
            self.cr.set_line_width(lineWidth)
        if RGBcolour is None:
            self.cr.set_source_rgb(*self.defaultRGBColour)
        else:
            self.cr.set_source_rgb(*RGBcolour)

        self.cr.move_to(self.transform(Point)[0], self.transform(Point)[1])
        self.cr.line_to(self.transform(Point+Direction)[0], self.transform(Point+Direction)[1])
        self.cr.stroke()
        return

    def findInputRadius(self, points):
        print(max([max([abs(point.euclPoint[0]) for point in points]), max([abs(point.euclPoint[1]) for point in points])]))
        return max([max([abs(point.euclPoint[0]) for point in points]), max([abs(point.euclPoint[1]) for point in points])])

    def drawGraph(self, graph, points, name="euclideanGeometry.svg", imageSize=100,  defaultRGBColour=[0,0,0], defaultLineWidth=0.005, defaultPointSize=0.0075):
        '''Takes a List of Points and edges and returns an image'''
        inputRadius = self.findInputRadius(points)
        imageSize = inputRadius*5000
        self.initiateImage(**dict(list(locals().items())[3:]))
        for v in graph.iter_vertices():
            self.drawPoint(points[v])

        for s, t in graph.iter_edges():
            self.drawGeodesic(points[s], points[t])
        
        # self.drawGeodesic(Geometry.Point([inputRadius, - inputRadius+inputRadius/100]), Geometry.Point([inputRadius, - inputRadius-inputRadius/100]))
        # self.drawGeodesic(Geometry.Point([inputRadius - inputRadius/5, - inputRadius+inputRadius/100]), Geometry.Point([inputRadius- inputRadius/5, - inputRadius-inputRadius/100]))
        # self.drawGeodesic(Geometry.Point([inputRadius - inputRadius/5, - inputRadius]), Geometry.Point([inputRadius, - inputRadius]))
        # self.cr.set_source_rgb(0, 0, 0)
        # self.cr.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
        # self.cr.set_font_size(inputRadius*1000)
        # print(self.transform(Geometry.Point([inputRadius - inputRadius/5, - inputRadius])))
        # self.cr.move_to(*self.transform(self.origin))
        # self.cr.show_text("######")
        return