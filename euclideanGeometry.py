import Geometry
import numpy as np
import random
import cairo  # for imaging. For a good introduction https://zetcode.com/gfx/pycairo/
import math

# 2D euclidean geometry


class EuclideanGeometry(Geometry.Geometry):

    def translate(self, pa, direct):
        """Returns translated Point object.
        Care: Information about distance should be carried in direction"""
        return pa + direct

    def getDistance(self, pa, pb):
        """Returns the euclidean metric between pa and pb as float."""
        return np.linalg.norm((pa-pb).euclPoint)

    def direction(self, pa, pb, dummy=None):
        """Returns the direction from pa to pb as a Point object."""
        return pb - pa

    # trivial in the euclidean case but not in others, like in the hyperbolic case
    def paralleltransport(direct, pa, pb):
        """Returns the first argument."""
        return direct

    def getOrigin(self):
        """Returns the origin."""
        return self.origin

    def unit_vector(self, direct):
        """Returns the unit vector of the vector."""
        return direct / np.linalg.norm(direct.euclPoint)

    def angle_between(self, v1, v2):
        """Returns the angle in radians between vectors 'v1' and 'v2'."""
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u.euclPoint, v2_u.euclPoint), -1.0, 1.0))

    def randomPoint(self, range=1000):
        """Returns a random point object in a n*n square around the center."""
        range = range/2
        return Geometry.Point([random.randint(-range, range), random.randint(-range, range)])

    # unique to euclidean case
    def getTangent(self, center, pa):
        """Gets the tangent of the circle through "pa" with midpoint "center" at the point "pa" """
        tangent = self.direction(center, pa)

        # getting the orthogonal
        tangent.euclPoint[0], tangent.euclPoint[1] = tangent.euclPoint[1], - \
            tangent.euclPoint[0]
        return tangent

    # producing the image. For a good introduction into pycairo https://zetcode.com/gfx/pycairo/

    def initiateImage(self, inputRadius, imageSize, name, defaultRGBColour, defaultLineWidth, defaultPointSize):
        """Setting up the image and the parameters of it

        Arguments:
        inputRadius -- the maximum of the maximum norm of all points that should be imaged (important for transform method image-coordinates)
        imageSize -- the pixelsize of the image
        name -- filename of the image
        defaultRGBColour -- default colour of all the lines and points. List with RGB-Values i.e. [0,0,0] for black
        defaultLineWidth -- default size of all lines, mainly the geodesics, scaling from 0 to 1 with 1 being the whole disk and 0 being no visible line
        defaultPointSize -- default size of all points, scaling from 0 to 1 with 1 being the whole disk and 0 being no visible point
        """
        # Initiate size of the image, the radius of the PDM and the framework for the image
        self.n = imageSize
        # (pixel-)sidelength of the boundary of the coordinate system
        self.radius = self.n/2*0.9
        self.ps = cairo.SVGSurface(name, self.n, self.n)
        self.cr = cairo.Context(self.ps)
        self.inputRadius = inputRadius

        # initiate default values
        self.defaultLineWidth = defaultLineWidth * \
            self.radius  # getting the actual pixelvalue
        self.defaultPointSize = defaultPointSize * \
            self.radius  # getting the actual pixelvalue
        self.defaultRGBColour = defaultRGBColour

        # creating background
        self.cr.set_source_rgb(255, 255, 255)  # setting background colour
        self.cr.rectangle(0, 0, self.n, self.n)  # drawing background
        self.cr.fill()
        self.cr.set_line_width(self.defaultLineWidth)

        # creating origin
        self.drawPoint(self.origin)
        return

    def transform(self, Point):
        """Takes a Point object and returns the proper scaled and rotated (pixel-)coordinates as a list."""
        xy = Point.euclPoint
        return [((xy[0]+self.inputRadius)*self.radius)/self.inputRadius + self.n/2 - self.radius, self.n/2 - ((xy[1]+self.inputRadius)*self.radius)/self.inputRadius + self.radius]

    def drawPoint(self, Point, RGBcolour=None, pointSize=None):
        """Takes a Point object and draws it in the image"""
        # Setting up colour and pointsize
        if pointSize is None:
            pointSize = self.defaultPointSize
        if RGBcolour is None:
            self.cr.set_source_rgb(*self.defaultRGBColour)
        else:
            self.cr.set_source_rgb(*RGBcolour)

        # Drawing the Point
        self.cr.arc(*self.transform(Point), pointSize, 0, 2*math.pi)
        self.cr.fill()
        return

    def drawGeodesic(self, Point1, Point2, RGBcolour=None, lineWidth=None):
        """Takes two Point objects and draws the geodesic between them"""
        # Setting up colour and pointsize
        if lineWidth is None:
            self.cr.set_line_width(self.defaultLineWidth)
        else:
            self.cr.set_line_width(lineWidth)
        if RGBcolour is None:
            self.cr.set_source_rgb(*self.defaultRGBColour)
        else:
            self.cr.set_source_rgb(*RGBcolour)

        # Drawing the geodesic
        self.cr.move_to(self.transform(Point1)[0], self.transform(Point1)[1])
        self.cr.line_to(self.transform(Point2)[0], self.transform(Point2)[1])
        self.cr.stroke()
        return

    def drawDirection(self, Point, Direction, RGBcolour=None, lineWidth=None):
        """Takes a Point object and a direction as a Point object and draws the direction as a straight line from the given point"""
        # Setting up colour and pointsize
        if lineWidth is None:
            self.cr.set_line_width(self.defaultLineWidth)
        else:
            self.cr.set_line_width(lineWidth)
        if RGBcolour is None:
            self.cr.set_source_rgb(*self.defaultRGBColour)
        else:
            self.cr.set_source_rgb(*RGBcolour)

        # Drawing the direction
        self.cr.move_to(*self.transform(Point))
        self.cr.line_to(*self.transform(Point+Direction))
        self.cr.stroke()
        return

    def findInputRadius(self, points):
        """Takes a list of all Point objects and returns the proper choice for the inputRadius"""
        return max([max([abs(point.euclPoint[0]) for point in points]), max([abs(point.euclPoint[1]) for point in points])])

    def drawGraph(self, graph, points, name="euclideanGeometry.svg", imageSize=100,  defaultRGBColour=[0, 0, 0], defaultLineWidth=0.005, defaultPointSize=0.0075):
        '''Takes a List of Point objects and a Graph object and returns an image

        Arguments: 
        graph -- Graph object
        points -- Corresponding list of points classes
        name -- filename of the image
        imageSize -- the pixelsize of the image
        defaultRGBColour -- default colour of all the lines and points. List with RGB-Values i.e. [0,0,0] for black
        defaultLineWidth -- default size of all lines, mainly the geodesics, scaling from 0 to 1 with 1 being the whole disk
        defaultPointSize -- default size of all points, scaling from 0 to 1 with 1 being the whole disk
        '''
        inputRadius = self.findInputRadius(points)
        # 5000 chosen more or less randomly (enough to get a smooth looking picture but not do big to handle)
        imageSize = inputRadius*5000
        self.initiateImage(**dict(list(locals().items())[3:]))

        # draw every vertex
        for v in graph.iter_vertices():
            self.drawPoint(points[v])

        # draw every edge
        for s, t in graph.iter_edges():
            self.drawGeodesic(points[s], points[t])

        # TODO: Attempt to draw the coordinate system

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
