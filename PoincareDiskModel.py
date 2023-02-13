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
        return abs((-pa.euclPoint[1] * (pb.euclPoint[0] - pa.euclPoint[0]) - pa.euclPoint[0] * (pb.euclPoint[1] - pa.euclPoint[1]))) < epsilon

    # returns Center and radius of the circle or in case the geodesic is a line the direction of the line and 0
    def getGeodesic(self, pa, pb):
        if self.checkOnOriginLine(pa, pb, 0.000001) == True:
            return eG.direction(pa, pb), 0
        # Naming of the variables following Wikipedia second way https://en.wikipedia.org/wiki/Poincar%C3%A9_disk_model#Compass_and_straightedge_construction
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
             midpointPaPb.euclPoint[1]))/(slopeLineM.euclPoint[0]*slopeLineN.euclPoint[1]-slopeLineN.euclPoint[0]*slopeLineM.euclPoint[1]+0.00001) # TODO: Slightly disturbe denominator to avoid Division by zero for
        C = Geometry.Point([midpointPaPb.euclPoint[0] + slopeLineM.euclPoint[0]
                           * t, midpointPaPb.euclPoint[1] + slopeLineM.euclPoint[1] * t])
        return C, eG.getDistance(C, pa)

    def translate(self, pa, direct, dist):
        z_0 = complex(pa.euclPoint[0], pa.euclPoint[1])
        direct = complex(eG.unit_vector(direct).euclPoint[0], eG.unit_vector(direct).euclPoint[1]) 
        pa =  (cmath.exp(dist) - 1)/(cmath.exp(dist) + 1)*direct
        return Geometry.Point([((pa + z_0)/(pa*z_0.conjugate() + 1)).real, ((pa + z_0)/(pa*z_0.conjugate() + 1)).imag]) 

    def getDistance(self, pa, pb):
        r = 1
        euclDistPaPb = eG.getDistance(pa, pb)
        euclDistPaO = eG.getDistance(pa, self.getOrigin())
        euclDistPbO = eG.getDistance(pb, self.getOrigin())
        return np.arccosh(1+abs((2 * euclDistPaPb**2 * r**2) /
                       abs((r**2 - euclDistPaO**2)*(r**2 - euclDistPbO**2)+0.000001))) # Absolute value and disturbance to avoid invalid arguments
        

    def direction(self, pa, pb):
        Center, r = self.getGeodesic(pb, pa)
        direct = eG.direction(Center, pa)
        direct.euclPoint[0], direct.euclPoint[1] = -direct.euclPoint[1], direct.euclPoint[0]
        if np.linalg.det([pa.euclPoint, pb.euclPoint])<0:
            return direct
        else:
            return self.origin-direct

    def paralleltransport(self, direct, pa, pb):
        center, r = self.getGeodesic(pa, pb)
        theta = eG.angle_between(eG.getTangent(center, pa), direct)
        rot = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        return Geometry.Point(np.dot(rot, eG.getTangent(center, pb).euclPoint))

    def randomPoint(self, range=1):
        '''Giving a random Point within the radius range'''
        alpha = 2 * math.pi * random.random()
        r = range * math.sqrt(random.random())
        return Geometry.Point([r * math.cos(alpha), r * math.sin(alpha)])

    def getOrigin(self):
        return self.origin



    #Drawing
    def transform(self, Point):
        '''Takes a point from the unitcircle and returns transformed image coordinates as an array'''
        xy = Point.euclPoint
        print("Transforming")
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

        #Drawing the Point
        self.cr.arc(self.transform(Point)[0], self.transform(
            Point)[1], pointSize, 0, 2*math.pi)
        self.cr.fill()
        return

    def drawGeodesic(self, Point1, Point2, RGBcolour=None, lineWidth=None):
        '''Drawing the geodesic of two points'''
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
        
        #Case, where the geodesic is a straight line through the origin
        if r == 0:
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

    def drawDirection(self, Point, Direction, RGBcolour=None, lineWidth=None):
        '''Takes a starting point and a direction (including scaling) and draws it'''
        # Setting up line width and colour
        if lineWidth is None:
            self.cr.set_line_width(self.defaultLineWidth)
        else:
            self.cr.set_line_width(lineWidth)
        if RGBcolour is None:
            self.cr.set_source_rgb(*self.defaultRGBColour)
        else:
            self.cr.set_source_rgb(*RGBcolour)

        #Drawing the line
        self.cr.move_to(self.transform(Point)[
            0], self.transform(Point)[1])
        self.cr.line_to(self.transform(Point+Direction)[
            0], self.transform(Point+Direction)[1])
        self.cr.stroke()
        return

    def initiateImage(self, inputRadius, name, imageSize,  defaultRGBColour, defaultLineWidth, defaultPointSize):
        '''Draws the PDM including background'''
        #Initiate size of the image, the radius of the PDM and the framework for the image
        self.n = imageSize
        self.radius = self.n/2*0.9
        self.ps = cairo.ImageSurface(cairo.FORMAT_ARGB32, self.n, self.n)
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

        # creating disk
        self.cr.set_source_rgb(0, 0, 0)
        self.cr.arc(self.n/2, self.n/2, self.radius, 0, 2*math.pi)
        self.cr.stroke()

        # creating origin
        self.drawPoint(self.origin)
        return


    def drawGraph(self, graph, points, name="PoincareDiskModel.svg", imageSize=100,  defaultRGBColour=[0,0,0], defaultLineWidth=0.005, defaultPointSize=0.0075):
        '''Takes a List of Points and edges'''
        inputRadius = 1
        self.initiateImage(**dict(list(locals().items())[3:]))
        for v in graph.iter_vertices():
            self.drawPoint(points[v])

        for s, t in graph.iter_edges():
            self.drawGeodesic(points[s], points[t])
        self.ps.write_to_png(name)
        return


PDM = PoincareDiskModel([0,0])

class Interface(Gtk.Window):
    
    def __init__(self, graph, points, size,  kr, kg, ks, ksmax, kstol):
        super().__init__()
        self.graph = graph
        self.points = points
        self.size = size
        self.inputRadius = 1
        self.radius = (0.9 * self.size )/ 2
        self.kr, self.kg, self.ks, self.ksmax, self.kstol =  kr, kg, ks, ksmax, kstol
        self.init_ui()



    def init_ui(self):    

        self.darea = Gtk.DrawingArea()
        self.darea.connect("draw", self.on_draw)
        self.darea.set_events(Gdk.EventMask.BUTTON_PRESS_MASK)        
        self.add(self.darea)
        self.pointsToMove = [] 
                  
        self.darea.connect("button-press-event", self.on_button_press)

        self.darea.connect("key-press-event", self.on_key_press)
        self.set_title("Graph")
        self.resize(self.size, self.size)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.connect("delete-event", Gtk.main_quit)
        self.show_all()

    def transform(self, Point):
        xy = Point.euclPoint
        return [((xy[0]+self.inputRadius)*self.radius)/self.inputRadius + self.size/2 - self.radius, self.size/2 - ((xy[1]+self.inputRadius)*self.radius)/self.inputRadius + self.radius]

    def drawGeodesic():
        return

    def on_draw(self, wid, cr):

        #Origin and boundary
        cr.set_source_rgb(0, 0, 0)
        cr.arc(self.size/2, self.size/2, self.radius, 0, 2*math.pi)
        cr.stroke()
        cr.arc(self.size/2, self.size/2, 3, 0, 2*math.pi)
        cr.fill()

        #Vertices
        for v in self.graph.iter_vertices():
            cr.arc(self.transform(self.points[v])[0], self.transform(self.points[v])[1], 3, 0, 2*math.pi)
            cr.fill()
            print(self.transform(self.points[v]))
        
        #Edges
        for s, t in self.graph.iter_edges():
            '''Drawing the geodesic of two points'''
            # Calculating the ideal circle
            C, r = PDM.getGeodesic(self.points[s], self.points[t])
            
            #Case, where the geodesic is a straight line through the origin
            if r == 0:
                cr.move_to(self.transform(Point1)[
                                0], self.transform(Point1)[1])
                cr.line_to(self.transform(Point2)[
                                0], self.transform(Point2)[1])
                cr.stroke()
            
            #Case, where the geodesic is a arc
            else:
                angle1 = eG.angle_between(eG.direction(C, self.points[s]), Geometry.Point([1, 0]))
                angle2 = eG.angle_between(eG.direction(C, self.points[t]), Geometry.Point([1, 0]))
                angle12 = eG.angle_between(eG.direction(C, self.points[s]), eG.direction(C, self.points[t])) 

                #Checking all cases
                if C.euclPoint[1]>self.points[s].euclPoint[1] and C.euclPoint[1]>self.points[t].euclPoint[1]:
                    if angle1 > angle2: 
                        angle1, angle2 = angle2, angle1
                    angle12 += angle1 
                elif C.euclPoint[1]>self.points[s].euclPoint[1] and C.euclPoint[1]<self.points[t].euclPoint[1]:
                    angle12 = 2*math.pi  - angle2  
                elif C.euclPoint[1]<self.points[s].euclPoint[1] and C.euclPoint[1]>self.points[t].euclPoint[1]:
                    angle1, angle2 = angle2, angle1
                    angle12 = 2*math.pi - angle2
                elif C.euclPoint[1]<self.points[s].euclPoint[1] and C.euclPoint[1]<self.points[t].euclPoint[1]:
                    if angle1 < angle2: angle1, angle2 = angle2, angle1
                    angle1 = 2*math.pi - angle1 
                    angle12 += angle1 

                #Making sure, that it draws the right side of the arc    
                if angle12 - angle1 > math.pi : angle1, angle12 = angle12, angle1

                #Drawing the arc
                cr.arc(self.transform(C)[0], self.transform(C)[1], r*self.radius, angle1, angle12)
                cr.stroke()
        return         
                         
                         
    def on_button_press(self, w, e):
        
        if e.type == Gdk.EventType.BUTTON_PRESS \
            and e.button == MouseButtons.LEFT_BUTTON:
            
            for v in self.graph.iter_vertices():
                
                if self.transform(self.points[v])[0] > e.x-10 and self.transform(self.points[v])[0] < e.x+10 and self.transform(self.points[v])[1] > e.y-10 and self.transform(self.points[v])[1] < e.y+10:
                    self.pointsToMove.append(v)

        if e.type == Gdk.EventType.BUTTON_PRESS \
            and e.button == MouseButtons.RIGHT_BUTTON:
                
            for v in self.pointsToMove:
                self.points[v] = Geometry.Point([(e.x + self.radius - self.size/2)*self.inputRadius/self.radius - self.inputRadius, (-e.y + self.radius + self.size/2)*self.inputRadius/self.radius - self.inputRadius]) + PDM.randomPoint(0.05)
            self.pointsToMove = [] 
            self.darea.queue_draw()   

    def on_key_press(self, w, e):
        print("asd")
        if e.type == Gdk.EventType.KEY_PRESS and e.button == Gdk.KEY_h:
            print("h")
            Gtk.main_quit()  
        return self.points
