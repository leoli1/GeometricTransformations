def Ellipse(z1,z2):
    center = 0.5*(z1+z2)
    a = abs(z1.real-z2.real)/2
    b = abs(z1.imag-z2.imag)/2
    pointsNum = 150
    points = []
    for i in range(0,pointsNum):
        p = i*2*PI/float(pointsNum)
        points.append(center+complex(a*cos(p),b*sin(p)))
    return points

def Line(z1,z2):
    pointsNum = 150
    points = []
    for i in range(0,pointsNum+1):
        points.append(z1+(z2-z1)*i/float(pointsNum))
    return points