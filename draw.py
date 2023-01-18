import cairo
import math
import PoincareDiskModel
import Geometry
import euclideanGeometry

pdm = PoincareDiskModel.PoincareDiskModel([0, 0])
eG = euclideanGeometry.EuclideanGeometry([0, 0])


class DrawPoincareDisk():
    def __init__(self, size):
        self.n = size
        self.radius = self.n/2*0.9
        self.ps = cairo.SVGSurface("svgfile.svg", self.n, self.n)
        self.cr = cairo.Context(self.ps)

    def transform(self, Point):
        xy = Point.euclPoint
        return [(xy[0]+1)*self.radius + self.n/2 - self.radius, self.n - (xy[1]+1)*self.radius - (self.n/2 - self.radius)]

    def drawPoint(self, Point, colour1=0, colour2=0, colour3=0):
        self.cr.set_source_rgb(colour1, colour2, colour3)
        self.cr.arc(self.transform(Point)[0], self.transform(
            Point)[1], self.radius*0.005, 0, 2*math.pi)
        self.cr.fill()
        return

    def drawGeodesic(self, Point1, Point2, colour1=0, colour2=0, colour3=0):
        C, r = pdm.getGeodesic(Point1, Point2)
        self.cr.set_source_rgb(colour1, colour2, colour3)

        if r == 0:
            self.cr.move_to(self.transform(Point1)[
                            0], self.transform(Point1)[1])
            self.cr.line_to(self.transform(Point2)[
                            0], self.transform(Point2)[1])
            self.cr.stroke()
        else:
            #self.cr.arc(self.transform(C)[0], self.transform(C)[
                       # 1], r*self.radius, eG.angle_between(eG.direction(C, Point1), Geometry.Point([1, 0])), eG.angle_between(eG.direction(C, Point2), Geometry.Point([1, 0])))
            self.cr.arc(self.transform(C)[0], self.transform(C)[
                        1], r*self.radius, 0, 2*math.pi)           
            self.cr.stroke()
        return

    def drawDirection(self, Point, Direction, colour1=0, colour2=0, colour3=0):
        self.cr.set_source_rgb(colour1, colour2, colour3)
        self.cr.move_to(self.transform(Point)[
                            0], self.transform(Point)[1])
        self.cr.line_to(self.transform(Point+Direction)[
                            0], self.transform(Point+Direction)[1])
        self.cr.stroke()
        return
    def main(self):
        # creating background
        self.cr.set_source_rgb(255, 255, 255)
        self.cr.rectangle(0, 0, self.n, self.n)
        self.cr.fill()
        self.cr.set_line_width(0.05)
# creating disk
        self.cr.set_source_rgb(0, 0, 0)
        self.cr.arc(self.n/2, self.n/2, self.radius, 0, 2*math.pi)
        self.cr.stroke()

# creating origin
        self.drawPoint(Geometry.Point([0, 0]))

# example
        p1 = Geometry.Point([0.9, 0.1])
        p2 = Geometry.Point([0.7, 0.5])
        #self.drawGeodesic(p1, p2)
        self.drawPoint(p1, 255)
        for i in range(0, 15):
            self.drawPoint(pdm.translate(p1, Geometry.Point([math.cos((2*math.pi/15)*i), math.sin((2*math.pi/15)*i)]), 0.5))
        v = Geometry.Point([5,1])
        p2i = p2
        self.drawGeodesic(p2, pdm.translate(p2, v, 0.1))
        for i in range(1, 15):
            p2 = pdm.translate(p2i, v, 0.1)
            v = pdm.paralleltransport(v, p2i, p2)
            self.drawPoint(p2)
            p2i=p2
        return
c = DrawPoincareDisk(100)
c.main()
