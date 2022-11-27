import Geometry
import euclideanGeometry
import numpy as np

eG = euclideanGeometry.EuclideanGeometry([0,0])

class PoincareDiskModel(Geometry.Geometry):

    def translate(self, pa, pb):
        pass

    
    def getDistance(self, pa, pb):
       r = 2 * np.pi
       euclDistPaPb = eG.getDistance(pa ,pb)
       euclDistPaO = eG.getDistance(pa ,self.getOrigin())
       euclDistPbO = eG.getDistance(pb ,self.getOrigin())
       x = np.arccosh(1+(2 * euclDistPaPb**2 * r**2 )/((r**2 - euclDistPaO**2)*(r**2 - euclDistPbO**2)))
       return x 

    
    def direction(self, pa, pb):
        pass
    
    def paralleltransport(direct, pa):
        pass

    def getOrigin(self):
        return self.origin

c = PoincareDiskModel([0,0])

p1 = [0.5, 0.7]
p2 = [0.2, 0.6]
print(c.getDistance(p1, p2))
