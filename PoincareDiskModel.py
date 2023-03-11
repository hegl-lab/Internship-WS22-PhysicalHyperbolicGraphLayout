import Geometry
import euclideanGeometry
import numpy as np
import math
import random
import cmath
import gi.repository 
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo


eG = euclideanGeometry.EuclideanGeometry([0, 0])


class MouseButtons:

    LEFT_BUTTON = 1
    RIGHT_BUTTON = 3


class PoincareDiskModel(Geometry.Geometry):

    def checkOnOriginLine(self, pa, pb, epsilon):
        """Returns True if the connecting line through pa and pb is going through the origin, where the epsilon value gives some error margin."""
        return abs((-pa.euclPoint[1] * (pb.euclPoint[0] - pa.euclPoint[0]) - pa.euclPoint[0] * (pb.euclPoint[1] - pa.euclPoint[1]))) < epsilon

    # returns Center and radius of the circle or in case the geodesic is a line the direction of the line and 0
    def getGeodesic(self, pa, pb):
        """Takes two points and returns a Point object and a float which are representing the center and the radius of the connecting geodesic. In case that the geodesic is a straight line it just returns the euclidean direction and 0."""
        if self.checkOnOriginLine(pa, pb, 0.000001) == True:
            return eG.direction(pa, pb), 0
        # Naming of the variables and calculations following Wikipedia https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model#Compass_and_straightedge_construction (Second Way)
        midpointPaPb = pa.midpoint(pb)
        pPrime = pa * (1/(eG.getDistance(Geometry.Point([0, 0]), pa)**2))
        midpointPPPrime = pa.midpoint(pPrime)
        slopeLineN = eG.direction(Geometry.Point([0, 0]), pa)
        slopeLineN.euclPoint[0], slopeLineN.euclPoint[1] = slopeLineN.euclPoint[1], - \
            slopeLineN.euclPoint[0]
        slopeLineM = eG.direction(pb, pa)
        slopeLineM.euclPoint[0], slopeLineM.euclPoint[1] = slopeLineM.euclPoint[1], - \
            slopeLineM.euclPoint[0]
        # Calculating intersection of both lines
        t = (slopeLineN.euclPoint[1]*(midpointPPPrime.euclPoint[0]-midpointPaPb.euclPoint[0])-slopeLineN.euclPoint[0]*(midpointPPPrime.euclPoint[1] -
             midpointPaPb.euclPoint[1]))/(slopeLineM.euclPoint[0]*slopeLineN.euclPoint[1]-slopeLineN.euclPoint[0]*slopeLineM.euclPoint[1]+0.00001)  # Slightly disturbe denominator to avoid Division by zero for
        C = Geometry.Point([midpointPaPb.euclPoint[0] + slopeLineM.euclPoint[0]
                           * t, midpointPaPb.euclPoint[1] + slopeLineM.euclPoint[1] * t])
        return C, eG.getDistance(C, pa)

    def translate(self, pa, direct, dist):
        """Returns the by direct and dist translated point object."""
        # Conjugating the system, so that pa is at the origin
        z_0 = complex(pa.euclPoint[0], pa.euclPoint[1])
        direct = complex(eG.unit_vector(
            direct).euclPoint[0], eG.unit_vector(direct).euclPoint[1])
        # Calculating the translation at the origin
        pa = (cmath.exp(dist) - 1)/(cmath.exp(dist) + 1)*direct
        # Conjugating it back to the original coordinate system
        return Geometry.Point([((pa + z_0)/(pa*z_0.conjugate() + 1)).real, ((pa + z_0)/(pa*z_0.conjugate() + 1)).imag])

    def getDistance(self, pa, pb):
        """Returns the hyperbolic distance of oa and pb as a float."""
        # Using the second formula https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model#Distance
        r = 1
        euclDistPaPb = eG.getDistance(pa, pb)
        euclDistPaO = eG.getDistance(pa, self.getOrigin())
        euclDistPbO = eG.getDistance(pb, self.getOrigin())
        return np.arccosh(1+abs((2 * euclDistPaPb**2 * r**2) /
                                abs((r**2 - euclDistPaO**2)*(r**2 - euclDistPbO**2)+0.000001)))  # Absolute value and disturbance to avoid invalid arguments

    def direction(self, pa, pb):
        """Returns the hyperbolic direction at the pa from pa to pb"""
        # Getting the connecting geodesic
        Center, r = self.getGeodesic(pb, pa)
        # Calculating the radius
        direct = eG.direction(Center, pa)
        # Get the original of the radius, to get the tangent line, which is then the direction
        direct.euclPoint[0], direct.euclPoint[1] = - \
            direct.euclPoint[1], direct.euclPoint[0]
        # Making sure the orientation is correct
        if np.linalg.det([pa.euclPoint, pb.euclPoint]) < 0:
            return direct
        else:
            return self.origin-direct

    def paralleltransport(self, direct, pa, pb):
        """Returns the from pa to pb parrallel transported direction as point object"""
        # Getting the connecting geodesic
        center, r = self.getGeodesic(pa, pb)
        # Calculating the relative position of the direction relative to the tangent of the circle at point pa
        theta = eG.angle_between(eG.getTangent(center, pa), direct)
        # Creating the rotation matrix
        rot = np.array([[math.cos(theta), -math.sin(theta)],
                       [math.sin(theta), math.cos(theta)]])
        # Returning the rotated tangent of the circle at pb which is then the parallel transported direction
        return Geometry.Point(np.dot(rot, eG.getTangent(center, pb).euclPoint))

    def randomPoint(self, range=1):
        '''Giving a random Point within the radius range'''
        alpha = 2 * math.pi * random.random()
        r = range * math.sqrt(random.random())
        return Geometry.Point([r * math.cos(alpha), r * math.sin(alpha)])

    def getOrigin(self):
        return self.origin

    # Drawing

    def initiateImage(self, inputRadius, imageSize, name,  defaultRGBColour, defaultLineWidth, defaultPointSize):
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
        # (pixel-)radius of the boundary of the disk
        self.radius = self.n/2*0.9
        self.ps = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.n, self.n)
        self.cr = cairo.Context(self.ps)
        self.inputRadius = inputRadius

        # initiate default values
        self.defaultLineWidth = defaultLineWidth*self.radius
        self.defaultPointSize = defaultPointSize*self.radius
        self.defaultRGBColour = defaultRGBColour

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
        self.drawPoint(self.origin)
        return

    def transform(self, Point):
        """Takes a Point object in the PDM(unitcircle) and returns the proper scaled and rotated (pixel-)coordinates as a list."""
        xy = Point.euclPoint
        return [((xy[0]+self.inputRadius)*self.radius)/self.inputRadius + self.n/2 - self.radius, self.n/2 - ((xy[1]+self.inputRadius)*self.radius)/self.inputRadius + self.radius]

    def drawPoint(self, Point, RGBcolour=None, pointSize=None):
        '''Takes a point and draws it into the image'''

        # Setting up colour and pointsize
        if pointSize is None:
            pointSize = self.defaultPointSize
        if RGBcolour is None:
            self.cr.set_source_rgb(*self.defaultRGBColour)
        else:
            self.cr.set_source_rgb(*RGBcolour)

        # Drawing the Point
        self.cr.arc(self.transform(Point)[0], self.transform(
            Point)[1], pointSize, 0, 2*math.pi)
        self.cr.fill()
        return

    def drawGeodesic(self, Point1, Point2, RGBcolour=None, lineWidth=None):
        """Takes two Point objects and draws the geodesic between them"""
        # Setting up line width and colour
        if lineWidth is None:
            self.cr.set_line_width(self.defaultLineWidth)
        else:
            self.cr.set_line_width(lineWidth)
        if RGBcolour is None:
            self.cr.set_source_rgb(*self.defaultRGBColour)
        else:
            self.cr.set_source_rgb(*RGBcolour)

        # Calculating the ideal circle
        C, r = self.getGeodesic(Point1, Point2)

        # Case, where the geodesic is a straight line through the origin
        if r == 0:
            self.cr.move_to(self.transform(Point1)[
                            0], self.transform(Point1)[1])
            self.cr.line_to(self.transform(Point2)[
                            0], self.transform(Point2)[1])
            self.cr.stroke()

        # Case, where the geodesic is an arc
        else:
            # calculating the angle that pycairo needs
            angle1 = eG.angle_between(eG.direction(
                C, Point1), Geometry.Point([1, 0]))
            angle2 = eG.angle_between(eG.direction(
                C, Point2), Geometry.Point([1, 0]))
            angle12 = eG.angle_between(eG.direction(
                C, Point1), eG.direction(C, Point2))

            # Checking all cases of possible orientations
            if C.euclPoint[1] > Point1.euclPoint[1] and C.euclPoint[1] > Point2.euclPoint[1]:
                if angle1 > angle2:
                    angle1, angle2 = angle2, angle1
                angle12 += angle1
            elif C.euclPoint[1] > Point1.euclPoint[1] and C.euclPoint[1] < Point2.euclPoint[1]:
                angle12 = 2*math.pi - angle2
            elif C.euclPoint[1] < Point1.euclPoint[1] and C.euclPoint[1] > Point2.euclPoint[1]:
                angle1, angle2 = angle2, angle1
                angle12 = 2*math.pi - angle2
            elif C.euclPoint[1] < Point1.euclPoint[1] and C.euclPoint[1] < Point2.euclPoint[1]:
                if angle1 < angle2:
                    angle1, angle2 = angle2, angle1
                angle1 = 2*math.pi - angle1
                angle12 += angle1

            # Making sure, that it draws the right side of the arc
            if angle12 - angle1 > math.pi:
                angle1, angle12 = angle12, angle1

            # Drawing the arc
            self.cr.arc(self.transform(C)[0], self.transform(C)[
                        1], r*self.radius, angle1, angle12)
            self.cr.stroke()
        return

    def drawDirection(self, Point, Direction, RGBcolour=None, lineWidth=None):
        """Takes a Point object and a direction as a Point object and draws the direction as a straight line from the given point"""
        # Setting up line width and colour
        if lineWidth is None:
            self.cr.set_line_width(self.defaultLineWidth)
        else:
            self.cr.set_line_width(lineWidth)
        if RGBcolour is None:
            self.cr.set_source_rgb(*self.defaultRGBColour)
        else:
            self.cr.set_source_rgb(*RGBcolour)

        # Drawing the line
        self.cr.move_to(self.transform(Point)[
            0], self.transform(Point)[1])
        self.cr.line_to(self.transform(Point+Direction)[
            0], self.transform(Point+Direction)[1])
        self.cr.stroke()
        return

    def drawGraph(self, graph, points, name="PoincareDiskModel.svg", imageSize=100,  defaultRGBColour=[0, 0, 0], defaultLineWidth=0.005, defaultPointSize=0.0075):
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
        inputRadius = 1
        self.initiateImage(**dict(list(locals().items())[3:]))
        # draw every vertex
        for v in graph.iter_vertices():
            self.drawPoint(points[v])

        # draw every edge
        for s, t in graph.iter_edges():
            self.drawGeodesic(points[s], points[t])
        self.ps.write_to_png(name)
        return


PDM = PoincareDiskModel([0, 0])

# This is just a first draft of an interface, where one could move the vertices of the graph after every iteration of FA2


class Interface(Gtk.Window):

    def __init__(self, graph, points, size,  kr, kg, ks, ksmax, kstol):
        # initiate the interface and all the parameters we need
        super().__init__()
        self.graph = graph
        self.points = points
        self.size = size
        self.inputRadius = 1
        self.radius = (0.9 * self.size) / 2
        self.kr, self.kg, self.ks, self.ksmax, self.kstol = kr, kg, ks, ksmax, kstol
        self.init_ui()  # Here is where the magic happens

    def init_ui(self):
        """Initiating the UI"""
        self.darea = Gtk.DrawingArea()
        # Connecting the internal draw-action to our draw method
        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)
        self.add(self.darea)
        self.pointsToMove = []  # Our list for the moving points (See below)

        # Connecting a buttonpress with our buttonpress method
        self.darea.connect("button-press-event", self.on_button_press)

        self.set_title("Graph")
        self.resize(self.size, self.size)  # Getting the right size
        self.set_position(Gtk.WindowPosition.CENTER)  # Centering the window
        # Making sure the window is closed properly
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def transform(self, Point):
        """Takes a Point object in the PDM(unitcircle) and returns the proper scaled and rotated (pixel-)coordinates as a list."""
        xy = Point.euclPoint
        return [((xy[0]+self.inputRadius)*self.radius)/self.inputRadius + self.size/2 - self.radius, self.size/2 - ((xy[1]+self.inputRadius)*self.radius)/self.inputRadius + self.radius]

    def drawGeodesic():
        return

    def on_draw(self, wid, cr):
        """Drawing the Graph"""
        #Origin and boundary
        cr.set_source_rgb(0, 0, 0)
        cr.arc(self.size/2, self.size/2, self.radius, 0, 2*math.pi)
        cr.stroke()
        cr.arc(self.size/2, self.size/2, 3, 0, 2*math.pi)
        cr.fill()

        # Vertices
        for v in self.graph.iter_vertices():
            cr.arc(self.transform(self.points[v])[0], self.transform(
                self.points[v])[1], 3, 0, 2*math.pi)
            cr.fill()
            print(self.transform(self.points[v]))

        # Edges
        # Disclaimer: Copy-pasted from the getGeodesic function from PDM-Class (Ugly)
        for s, t in self.graph.iter_edges():
            # Drawing the geodesic of two points
            # Calculating the ideal circle
            C, r = PDM.getGeodesic(self.points[s], self.points[t])

            # Case, where the geodesic is a straight line through the origin
            if r == 0:
                cr.move_to(self.transform(Point1)[
                    0], self.transform(Point1)[1])
                cr.line_to(self.transform(Point2)[
                    0], self.transform(Point2)[1])
                cr.stroke()

            # Case, where the geodesic is a arc
            else:
                angle1 = eG.angle_between(eG.direction(
                    C, self.points[s]), Geometry.Point([1, 0]))
                angle2 = eG.angle_between(eG.direction(
                    C, self.points[t]), Geometry.Point([1, 0]))
                angle12 = eG.angle_between(eG.direction(
                    C, self.points[s]), eG.direction(C, self.points[t]))

                # Checking all cases
                if C.euclPoint[1] > self.points[s].euclPoint[1] and C.euclPoint[1] > self.points[t].euclPoint[1]:
                    if angle1 > angle2:
                        angle1, angle2 = angle2, angle1
                    angle12 += angle1
                elif C.euclPoint[1] > self.points[s].euclPoint[1] and C.euclPoint[1] < self.points[t].euclPoint[1]:
                    angle12 = 2*math.pi - angle2
                elif C.euclPoint[1] < self.points[s].euclPoint[1] and C.euclPoint[1] > self.points[t].euclPoint[1]:
                    angle1, angle2 = angle2, angle1
                    angle12 = 2*math.pi - angle2
                elif C.euclPoint[1] < self.points[s].euclPoint[1] and C.euclPoint[1] < self.points[t].euclPoint[1]:
                    if angle1 < angle2:
                        angle1, angle2 = angle2, angle1
                    angle1 = 2*math.pi - angle1
                    angle12 += angle1

                # Making sure, that it draws the right side of the arc
                if angle12 - angle1 > math.pi:
                    angle1, angle12 = angle12, angle1

                # Drawing the arc
                cr.arc(self.transform(C)[0], self.transform(
                    C)[1], r*self.radius, angle1, angle12)
                cr.stroke()
        return

    def on_button_press(self, w, e):
        """Adding the feature to select points with the left mouse button and moving them with a right mouse click"""
        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.LEFT_BUTTON:

            for v in self.graph.iter_vertices():
                # Checking if the point should be selected
                # 10 is a random selected "cursorsize"
                if self.transform(self.points[v])[0] > e.x-10 and self.transform(self.points[v])[0] < e.x+10 and self.transform(self.points[v])[1] > e.y-10 and self.transform(self.points[v])[1] < e.y+10:
                    # Putting the point in the list of points to move
                    self.pointsToMove.append(v)

        if e.type == Gdk.EventType.BUTTON_PRESS \
                and e.button == MouseButtons.RIGHT_BUTTON:

            # moving every point to the location of the right click
            for v in self.pointsToMove:
                # Inverse of the transform method
                self.points[v] = Geometry.Point([(e.x + self.radius - self.size/2)*self.inputRadius/self.radius - self.inputRadius, (-e.y + self.radius + self.size/2)
                                                * self.inputRadius/self.radius - self.inputRadius]) + PDM.randomPoint(0.05)  # The random point is just there to unclump the points
            self.pointsToMove = []
            self.darea.queue_draw()
