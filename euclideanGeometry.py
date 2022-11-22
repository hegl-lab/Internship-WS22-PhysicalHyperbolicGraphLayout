import Geometry
import numpy as np

class EuclideanGeometry(Geometry.Geometry):
    def translate(self, pa, pb):
        print("I can walk and run")
    
    def translate(self, pa, pb):
        for index, x in enumerate(pa):
            pa[index] = pa[index] + pb[index] 
        return pa

    
    def getDistance(self, pa, pb):
        dist = 0
        for index, x in enumerate(pa):
            dist = dist + (pa[index] - pb[index])**2
        dist = np.sqrt(dist)
        return dist
        pass

    
    def direction(self, pa, pb):
        direct = []
        for index, x in enumerate(pa):
            direct.append(pb[index] - pa[index])
        return direct

    
    def paralleltransport(direct, pa):
        pass

    def getOrigin(self):
        return origin

c = EuclideanGeometry(0)

p1 = [1, 6]
p2 = [3,4]
print(EuclideanGeometry.translate(c, p1, p2))
print(EuclideanGeometry.direction(c, p1, p2))