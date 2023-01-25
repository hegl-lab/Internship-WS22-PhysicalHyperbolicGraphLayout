import Geometry
import numpy as np
import random


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
        return direct

    def getOrigin(self):
        return self.origin

    def unit_vector(self, direct):
        """ Returns the unit vector of the vector.  """
        return direct / np.linalg.norm(direct.euclPoint)

    def angle_between(self, v1, v2):
        """ Returns the angle in radians between vectors 'v1' and 'v2'"""
        v1_u = self.unit_vector(v1)
        v2_u = self.unit_vector(v2)
        return np.arccos(np.clip(np.dot(v1_u.euclPoint, v2_u.euclPoint), -1.0, 1.0))

    def randomPoint(self, range=1000):
        return Geometry.Point([random.randint(-range, range), random.randint(-range, range)])

    def getTangent(self, center, pa):
        tangent = self.direction(center, pa)
        tangent.euclPoint[0], tangent.euclPoint[1] = tangent.euclPoint[1], - \
            tangent.euclPoint[0]
        return tangent
