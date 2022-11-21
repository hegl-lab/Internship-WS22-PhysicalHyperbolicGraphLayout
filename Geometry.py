# abstract class Geometry for interface
# Create subclasses by Geometry.register(Name)
from abc import ABC, abstractmethod


class Point(ABC):

    def __init__(self, dist, direct):
        self.dist
        self.direct

    def getDist(self):
        return self.dist

    def getDirect(self):
        return self.direct

    def setDist(self, dist):
        self.dist = dist

    def setDirect(self, direct):
        self.direct = direct

# still needs to inherit Point class?
class Geometry(ABC):

    def __init__(self, origin):
        self.origin = origin


    @abstractmethod
    def translate(self, pa, pb):
        pass

    @abstractmethod
    def getDistance(self, pa, pb):
        pass

    @abstractmethod
    def direction(pa, pb):
        pass

    @abstractmethod
    def paralleltransport(direct, pa):
        pass

    def getOrigin(self):
        return origin
