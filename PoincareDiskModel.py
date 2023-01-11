import Geometry
import euclideanGeometry
import numpy as np
from math import cos, sin
import random

eG = euclideanGeometry.EuclideanGeometry([0, 0])


class PoincareDiskModel(Geometry.Geometry):
    def checkOnOriginLine(self, pa, pb, epsilon):
        return (-pa.euclPoint[1] * (pb.euclPoint[0] - pa.euclPoint[0]) - pa.euclPoint[0] * (pb.euclPoint[1] - pa.euclPoint[1])) < epsilon

    # returns Center and radius of the circle or in case the geodesic is a line the direction of the line and 0
    def getGeodesic(self, pa, pb):
        if self.checkOnOriginLine(pa, pb, 0.01) == True:
            return eG.direction(pa, pb), 0
        # Returning what in case of straight line?
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
             midpointPaPb.euclPoint[1]))/(slopeLineM.euclPoint[0]*slopeLineN.euclPoint[1]-slopeLineN.euclPoint[0]*slopeLineM.euclPoint[1])
        C = Geometry.Point([midpointPaPb.euclPoint[0] + slopeLineM.euclPoint[0]
                           * t, midpointPaPb.euclPoint[1] + slopeLineM.euclPoint[1] * t])
        return C, eG.getDistance(C, pa)

    def translate(self, pa, pb):
        pass

    def getDistance(self, pa, pb):
        r = 2 * np.pi
        euclDistPaPb = eG.getDistance(pa, pb)
        euclDistPaO = eG.getDistance(pa, self.getOrigin())
        euclDistPbO = eG.getDistance(pb, self.getOrigin())
        x = np.arccosh(1+(2 * euclDistPaPb**2 * r**2) /
                       ((r**2 - euclDistPaO**2)*(r**2 - euclDistPbO**2)))
        return x

    def direction(self, pa, pb):
        Center, r = self.getGeodesic(pb, pa)
        direct = eG.direction(Center, pa)
        direct.euclPoint[0], direct.euclPoint[1] = - \
            direct.euclPoint[1], direct.euclPoint[0]
        return direct

    def paralleltransport(self, direct, pa, pb):
        center, r = self.getGeodesic(pb, pa)
        theta = eG.angle_between(eG.getTangent(center, pa), direct)
        rot = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        return Geometry.Point(np.dot(rot, eG.getTangent(center, pb).euclPoint))

    def randomPoint(self, range):
        '''Giving a random Point within the radius range'''
        alpha = 2 * math.pi * random.random()
        r = range * math.sqrt(random.random())
        return Geometry.Point([r * math.cos(alpha), r * math.sin(alpha)])

    def getOrigin(self):
        return self.origin


c = PoincareDiskModel([0, 0])

direct = Geometry.Point([0, 1])
p1 = Geometry.Point([0.1, 0.5])
p2 = Geometry.Point([0.2, 0.2])
print(random.random())
