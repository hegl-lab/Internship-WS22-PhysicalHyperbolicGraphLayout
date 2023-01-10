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

    def __div__(self, scalar):
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
    def direction(pa, pb):
        pass

    @abstractmethod
    def paralleltransport(direct, pa, pb):
        pass

    def getOrigin(self):
        return self.origin

    #def randomPoint