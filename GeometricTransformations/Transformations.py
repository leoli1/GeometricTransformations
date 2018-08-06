from cmath import *

class Transformation(object):
    def __init__(self, fixedPoints, transformation, name=""):
        self.fixedPoints = fixedPoints
        self.transformation = transformation
        self.name = name
steps = 150
CIFixedPoints = [ exp(complex(0,a*2*PI/steps)) for a in range(0,steps)]
def CircleInversion(z):
    if (z==0):
        return None
    return 1/z.conjugate()

transformations = [Transformation(CIFixedPoints,CircleInversion, "Circle Inversion")]