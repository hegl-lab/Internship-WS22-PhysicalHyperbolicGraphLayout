# abstract class Geometry for interface
# Create subclasses by Geometry.register(Name)
from abc import ABC, abstractmethod


class Point(ABC):
    def __init__(self, euclPoint):
        self.euclPoint = euclPoint

    def __add__(self, pb):
        return Point([self.euclPoint[0]+pb.euclPoint[0], self.euclPoint[1]+pb.euclPoint[1]])

    def __sub__(self, pb):
        return Point([self.euclPoint[0]-pb.euclPoint[0], self.euclPoint[1]-pb.euclPoint[1]])

    def __mul__(self, scalar):
        return Point([self.euclPoint[0]*scalar, self.euclPoint[1]*scalar])

    def __truediv__(self, scalar):
        return Point([self.euclPoint[0]/scalar, self.euclPoint[1]/scalar])

    def midpoint(self, pb):
        return (self+pb)*(1/2)
# still needs to inherit Point class?


class Geometry(ABC):

    def __init__(self, origin):
        self.origin = Point(origin)

    @abstractmethod
    def translate(self, pa, direct):
        pass

    @abstractmethod
    def getDistance(self, pa, pb):
        pass

    @abstractmethod
    def direction(self, pa, pb):
        pass

    @abstractmethod
    def paralleltransport(self, direct, pa, pb):
        pass
    
    @abstractmethod
    def getOrigin(self):
        return self.origin

    @abstractmethod
    def randomPoint(self, range):
        pass

    @abstractmethod
    def initiateImage(self, inputRadius, imageSize, name, defaultRGBColour, defaultLineWidth, defaultPointSize):
        pass

    @abstractmethod
    def transform(self, Point):
        pass

    @abstractmethod
    def drawPoint(self, Point, RGBcolour, pointSize):
        pass

    @abstractmethod
    def drawGeodesic(self, pa, pb, RGBcolour, lineWidth):
        pass

    @abstractmethod
    def drawDirection(self, Point, Direction,  RGBcolour, lineWidth):
        pass

    @abstractmethod
    def drawGraph(self, inputRadius, name, imageSize,  defaultRGBColour, defaultLineWidth, defaultPointSize):
        pass