# abstract class Geometry for interface
# Create subclasses by Geometry.register(Name)
from abc import ABC, abstractmethod
import numpy as np


class Point(ABC):
    def __init__(self, euclPoint):
        # This will be the main property, we will work with
        self.euclPoint = euclPoint

    # adding coordinatewise operations
    def __add__(self, pb):
        return Point([a_i + b_i for a_i, b_i in zip(self.euclPoint, pb.euclPoint)])

    def __sub__(self, pb):
        return Point([a_i - b_i for a_i, b_i in zip(self.euclPoint, pb.euclPoint)])

    def __mul__(self, scalar):
        return Point([a_i*scalar for a_i in self.euclPoint])

    def __truediv__(self, scalar):
        return Point([a_i/scalar for a_i in self.euclPoint])

    def midpoint(self, pb):
        return (self+pb)*(1/2)
# still needs to inherit Point class?


class Geometry(ABC):

    def __init__(self, origin):
        self.origin = Point(origin)

    # setting framework for the different geometries
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
    def drawGraph(self,  graph, points, name, imageSize,  defaultRGBColour, defaultLineWidth, defaultPointSize):
        pass
