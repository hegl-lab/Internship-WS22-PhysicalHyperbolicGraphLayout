import Geometry
import numpy as np


class EuclideanGeometry(Geometry.Geometry):

    def translate(self, pa, direct):
        return pa + direct

    def getDistance(self, pa, pb):
        dist = 0
        for index, x in enumerate(pa.euclPoint):
            dist = dist + (pa.euclPoint[index] - pb.euclPoint[index])**2
        dist = np.sqrt(dist)
        return dist

    def direction(self, pa, pb):
        direct = []
        for index, x in enumerate(pa.euclPoint):
            direct.append(pb.euclPoint[index] - pa.euclPoint[index])
        return Geometry.Point(direct)

    def paralleltransport(direct, pa, pb):
        pass

    def getOrigin(self):
        return self.origin
    #def randomPoint maybe 1000*1000 square

c = EuclideanGeometry(0)

p1 = Geometry.Point([1, 1])
p2 = Geometry.Point([3, 4])
#print(c.translate(p1, p2).euclPoint)
#print(c.direction(p1, p2))
