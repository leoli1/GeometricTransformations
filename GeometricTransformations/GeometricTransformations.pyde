from cmath import *
from Transformations import *
from Button import *


windowRange = 10
transformation = transformations[0]
temporaryCurve = ([], False)
curves = []
DomainGraphics = None
ImageGraphics = None


def setup():
    global DomainGraphics, ImageGraphics
    size(1024, 512)
    setupButtons()
    #DomainGraphics = createGraphics(512, 512, PDF, "temp.pdf")
    #ImageGraphics = createGraphics(512, 512, PDF, "temp2.pdf")
    DomainGraphics = createGraphics(768, 768)
    ImageGraphics = createGraphics(768, 768)

def draw():
    background(255)
    
    DomainGraphics.beginDraw()
    ImageGraphics.beginDraw()
    
    drawAxis()
    drawFixedPoints()
    drawCurves()
    
    DomainGraphics.dispose()
    ImageGraphics.dispose()
    DomainGraphics.endDraw()
    ImageGraphics.endDraw()
    
    image(DomainGraphics,0,0,512,512)
    image(ImageGraphics,width/2,0,512,512)
    
    drawButtons()
    
    
    strokeWeight(2)
    line(width/2,0,width/2,height)

def mousePressed():
    if testButtons():
        return
    z = convertWindowToComplex(PVector(mouseX, mouseY))
    temporaryCurve[0].append(z)
def mouseDragged():
    if (len(temporaryCurve[0])==0): return
    p = PVector(mouseX, mouseY)
    z = convertWindowToComplex(p)
    if (z != temporaryCurve[0][-1]):
        temporaryCurve[0].append(z)
def mouseReleased():
    global temporaryCurve
    curves.append(temporaryCurve)
    temporaryCurve = ([], False)

def convertWindowToComplex(p):
    if (p.x<=width/2):
        x = map(p.x, 0, width/2, -windowRange / 2, windowRange / 2)
        y = map(p.y, height, 0, -windowRange / 2, windowRange / 2)
        return complex(x, y)
    else:
        x = map(p.x, width/2, width, -windowRange / 2, windowRange / 2)
        y = map(p.y, height, 0, -windowRange / 2, windowRange / 2)
        return complex(x, y)
def convertComplexToWindow(c):
    x = map(c.real, -windowRange / 2, windowRange / 2, 0, DomainGraphics.width)
    y = map(c.imag, -windowRange / 2, windowRange / 2, DomainGraphics.height, 0)
    return PVector(int(x), int(y))

def drawAxis(thickness=1, strokeColor=color(0)):
    DomainGraphics.stroke(strokeColor)
    DomainGraphics.strokeWeight(thickness)
    ImageGraphics.stroke(strokeColor)
    ImageGraphics.strokeWeight(thickness)
    DomainGraphics.line(0, DomainGraphics.height / 2, DomainGraphics.width, DomainGraphics.height / 2)
    DomainGraphics.line(DomainGraphics.width / 2, 0, DomainGraphics.width / 2, DomainGraphics.height)
    ImageGraphics.line(0, ImageGraphics.height / 2, ImageGraphics.width, ImageGraphics.height / 2)
    ImageGraphics.line(ImageGraphics.width / 2, 0, ImageGraphics.width / 2, ImageGraphics.height)

def drawFixedPoints():
    drawCurve(transformation.fixedPoints, thickness=0.4, drawImage=True)

def reset():
    global curves, temporaryCurve
    temporaryCurve = ([], False)
    curves = []

def drawCurves(curveColor=color(0), imageCurveColor=color(255, 0, 0)):
    strokeWeight(1)
    for c in curves:
        drawCurve(c[0], closed=c[1], drawImage=True)
    drawCurve(temporaryCurve[0], closed=temporaryCurve[1], drawImage=True)
    
def drawCurve(curveSet, closed=True, thickness=1, strokeColor=color(0), drawImage=False, imageCurveColor=color(255, 0, 0)):
    ImageGraphics.strokeWeight(thickness)
    DomainGraphics.strokeWeight(thickness)
    s = 0
    if closed:
        s = -1
    for i in range(s, len(curveSet) - 1):
        if (curveSet[i] == None or curveSet[i + 1] == None):
            continue
        p1 = convertComplexToWindow(curveSet[i])
        p2 = convertComplexToWindow(curveSet[i + 1])
        DomainGraphics.stroke(strokeColor)
        DomainGraphics.line(p1.x, p1.y, p2.x, p2.y)

        if drawImage:
            p1 = convertComplexToWindow(
                transformation.transformation(curveSet[i]))
            p2 = convertComplexToWindow(
                transformation.transformation(curveSet[i + 1]))
            ImageGraphics.stroke(imageCurveColor)
            ImageGraphics.line(p1.x, p1.y, p2.x, p2.y)
