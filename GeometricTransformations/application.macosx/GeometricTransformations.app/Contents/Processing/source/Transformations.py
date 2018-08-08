from cmath import *

class Transformation(object):
    def __init__(self, fixedPoints, transformation, name=""):
        self.fixedPoints = fixedPoints
        def trans2(z):
            try:
                return transformation(z)
            except:
                return None
        self.transformation = trans2
        self.name = name
        
###        
steps = 150
CIFixedPoints = [ exp(complex(0,a*2*PI/steps)) for a in range(0,steps)]
def CircleInversion(z):
    if (z==0):
        return None
    return 1/z.conjugate()
###
CI2FixedPoints = [exp(complex(0,i*2*PI/3)) for i in range(0,3)]
def CircleInversion2(z):
    if (z==0):
        return None
    return 1/(z*z)
###
ExpFixedPoints = [] # TODO
def ExpMapping(z):
    return exp(z)
###
SqrFixedPoints = [0,1]
def SqrMapping(z):
    return z*z
###
JoukFixedPoints = []
def JoukMapping(z):
    if (z==0):
        return None
    return (z+1/z)
transformations = [Transformation((CIFixedPoints, True),CircleInversion, "1/(a-bi)"), Transformation((CI2FixedPoints, False),CircleInversion2, "1/z^2"), 
                   Transformation((ExpFixedPoints, True),ExpMapping, "exp(z)"),Transformation((SqrFixedPoints, False),SqrMapping, "z^2"),Transformation((JoukFixedPoints,True),JoukMapping, "(z+1/z)")]