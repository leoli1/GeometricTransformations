from cmath import *
from Transformations import *
from Button import *
from GeometrySets import *


windowRange = 12
transformation = transformations[0]
temporaryCurve = ([], False)
curves = []
DomainGraphics = None
ImageGraphics = None
gridPoints = 200
horizRange = [x * windowRange / float(gridPoints)
              for x in range(-gridPoints / 2 - 1, gridPoints / 2 + 2)]

drawingStartPoint = 0

yOffset = 55
timer = 0
saveCount = 0
formulaInputText = ""


class Configuration:

    def __init__(self):
        self.showGrid = False
        self.ellipseOn = False
        self.drawEllipse = False
        self.drawLine = False
        self.customInField = False

    def _reset(self):
        reset()

    def setTransformation(self, trans):
        global transformation
        transformation = trans
        self.customInField = False

    def zoomIn(self):
        global horizRange, windowRange
        if (windowRange > 1):
            windowRange -= 1
        horizRange = [x * windowRange / float(gridPoints)
                      for x in range(-gridPoints / 2 - 1, gridPoints / 2 + 2)]

    def zoomOut(self):
        global horizRange, windowRange
        windowRange += 1
        horizRange = [x * windowRange / float(gridPoints)
                      for x in range(-gridPoints / 2 - 1, gridPoints / 2 + 2)]

    def save(self):
        saveImage()

config = Configuration()

def setup():
    global DomainGraphics, ImageGraphics, formulaInputField
    size(1024, 512 + yOffset)
    setupButtons()
    #DomainGraphics = createGraphics(512, 512, PDF, "temp.pdf")
    #ImageGraphics = createGraphics(512, 512, PDF, "temp2.pdf")
    DomainGraphics = createGraphics(1024, 1024)
    ImageGraphics = createGraphics(1024, 1024)

def draw():
    global timer
    timer += 1
    background(255)

    DomainGraphics.beginDraw()
    ImageGraphics.beginDraw()
    DomainGraphics.background(255)
    ImageGraphics.background(255)

    if config.showGrid:
        allButtons[0].strokeColor = color(0, 255, 0)
    else:
        allButtons[0].strokeColor = color(0)
    if config.ellipseOn:
        allButtons[1].strokeColor = color(0, 255, 0)
    else:
        allButtons[1].strokeColor = color(0)
    if config.customInField:
        allButtons[6].strokeColor = color(0, 255, 0)
    else:
        allButtons[6].strokeColor = color(0)

    drawAxis()
    drawFixedPoints()
    drawCurves(curves)
    if config.showGrid:
        drawGrid()

    # DomainGraphics.dispose()
    # ImageGraphics.dispose()
    DomainGraphics.endDraw()
    ImageGraphics.endDraw()

    image(DomainGraphics, 0, yOffset, 512, 512)
    image(ImageGraphics, width / 2, yOffset, 512, 512)

    drawButtons()
    
    if config.customInField:
        strokeWeight(1)
        fill(0)
        textAlign(LEFT,TOP)
        text(formulaInputText,600,5)
        setTransformFromText()
    
    stroke(0)
    strokeWeight(2)
    line(width / 2, yOffset, width / 2, height)
    line(0, yOffset, width, yOffset)

def mousePressed():
    global drawingStartPoint, temporaryCurve
    if (mouseButton == LEFT):
        if testButtons(config):
            return
        if config.ellipseOn:
            drawingStartPoint = convertWindowToComplex(PVector(mouseX, mouseY))
            config.drawEllipse = True
        else:
            if config.drawLine == True:
                if (len(temporaryCurve[0]) != 0):
                    submitTempCurve()
            config.drawLine = not config.drawLine
            drawingStartPoint = convertWindowToComplex(PVector(mouseX, mouseY))
    elif (mouseButton == RIGHT):
        z = convertWindowToComplex(PVector(mouseX, mouseY))
        temporaryCurve[0].append(z)
def mouseDragged():
    global temporaryCurve
    p = PVector(mouseX, mouseY)
    z = convertWindowToComplex(p)
    if (mouseButton == LEFT):
        if config.drawEllipse:
            temporaryCurve = (Ellipse(drawingStartPoint, z), True)
        elif config.drawLine:
            temporaryCurve = (Line(drawingStartPoint, z), False)
            if (keyPressed and keyCode == SHIFT) and timer % 5 == 0:
                submitTempCurve()
    elif (mouseButton == RIGHT):
        if (len(temporaryCurve[0]) == 0):
            return
        if (z != temporaryCurve[0][-1]):
            temporaryCurve[0].append(z)

def mouseMoved():
    global temporaryCurve
    if config.drawLine:
        z = convertWindowToComplex(PVector(mouseX, mouseY))
        temporaryCurve = (Line(drawingStartPoint, z), False)

def mouseReleased():
    global temporaryCurve
    if (mouseButton == LEFT):
        #config.drawLine = False
        if config.drawEllipse:
            config.ellipseOn = False
            config.drawEllipse = False
    if (len(temporaryCurve[0]) != 0) and not config.drawLine:
        submitTempCurve()

def keyPressed():
    global formulaInputText
    if not config.customInField or keyCode == 10:
        return
    if keyCode == BACKSPACE or keyCode == DELETE or keyCode == 8:
        if len(formulaInputText)>0:
            formulaInputText = formulaInputText[:-1]
            setTransformFromText()
    elif type(key) != int:
        formulaInputText += key
        setTransformFromText()
        

def submitTempCurve():
    global temporaryCurve
    curves.append(temporaryCurve)
    temporaryCurve = ([], False)

def convertWindowToComplex(p):
    """if (p.x<=width/2):
        x = map(p.x, 0, width/2, -windowRange / 2, windowRange / 2)
        y = map(p.y, height, 50, -windowRange / 2, windowRange / 2)
        return complex(x, y)
    else:
        x = map(p.x, width/2, width, -windowRange / 2, windowRange / 2)
        y = map(p.y, height, 50, -windowRange / 2, windowRange / 2)"""
    x = map(p.x, 0, width, -windowRange / 2.0, 3 * windowRange / 2.0)
    y = map(p.y, height, yOffset, -windowRange / 2.0, windowRange / 2.0)
    return complex(x, y)
def convertComplexToWindow(c):
    if c == None:
        return None
    x = map(c.real, -windowRange / 2.0,
            windowRange / 2.0, 0, DomainGraphics.width)
    #x = map(c.real, -windowRange / 2, windowRange / 2, 0, width/2)
    y = map(c.imag, -windowRange / 2.0,
            windowRange / 2.0, DomainGraphics.height, 0)
    #y = map(c.imag, -windowRange / 2, windowRange / 2, height, 0)
    return PVector(int(x), int(y))

def saveImage():
    global saveCount
    pic = createGraphics(1024, 512)
    
    pic.beginDraw()
    pic.image(DomainGraphics, 0, 0, 512, 512)
    pic.image(ImageGraphics, 512, 0, 512, 512)
    pic.stroke(0)
    pic.strokeWeight(2)
    pic.line(width / 2, 0, width / 2, height)
    pic.endDraw()
    
    pic.save("save"+str(saveCount)+".png")
    saveCount += 1
def drawAxis(thickness=1, strokeColor=color(0)):
    DomainGraphics.stroke(strokeColor)
    DomainGraphics.strokeWeight(thickness)
    ImageGraphics.stroke(strokeColor)
    ImageGraphics.strokeWeight(thickness)
    # stroke(strokeColor)
    # strokeWeight(thickness)
    DomainGraphics.line(
        0, DomainGraphics.height / 2, DomainGraphics.width, DomainGraphics.height / 2)
    DomainGraphics.line(
        DomainGraphics.width / 2, 0, DomainGraphics.width / 2, DomainGraphics.height)
    ImageGraphics.line(
        0, ImageGraphics.height / 2, ImageGraphics.width, ImageGraphics.height / 2)
    ImageGraphics.line(
        ImageGraphics.width / 2, 0, ImageGraphics.width / 2, ImageGraphics.height)
    #line(0, height / 2, width, height / 2)
    #line(width / 4, 0, width / 4, height)
    #line(3*width / 4, 0, 3*width / 4, height)

def drawFixedPoints():
    drawCurve(transformation.fixedPoints[
              0], thickness=0.4, drawImage=True, connected=transformation.fixedPoints[1])

def setTransformFromText():
    global transformation
    def trans(z):
        a = z.real
        b = z.imag
        x = z
        return eval(formulaInputText)
    transformation = Transformation(([],True), trans,"")
    
def reset():
    global curves, temporaryCurve
    temporaryCurve = ([], False)
    curves = []

def drawGrid():
    for i in range(0, windowRange + 1):
        p = i / float(windowRange) * DomainGraphics.width
        DomainGraphics.stroke(0)
        DomainGraphics.strokeWeight(1)
        DomainGraphics.line(0, p, DomainGraphics.width, p)
        DomainGraphics.line(p, 0, p, DomainGraphics.height)
        for a in range(0, len(horizRange) - 1):
            j = i - windowRange / 2
            if (horizRange[a] == 0 or horizRange[a + 1] == 0) and j == 0:
                continue
            p1 = convertComplexToWindow(
                transformation.transformation(complex(horizRange[a], j)))
            p2 = convertComplexToWindow(
                transformation.transformation(complex(horizRange[a + 1], j)))
            ImageGraphics.stroke(color(255, 0, 0))
            ImageGraphics.strokeWeight(1)
            ImageGraphics.line(p1.x, p1.y, p2.x, p2.y)

            p1 = convertComplexToWindow(
                transformation.transformation(complex(j, horizRange[a])))
            p2 = convertComplexToWindow(
                transformation.transformation(complex(j, horizRange[a + 1])))
            ImageGraphics.line(p1.x, p1.y, p2.x, p2.y)


def drawCurves(curvesSet, curveColor=color(0), imageCurveColor=color(255, 0, 0)):
    for c in curvesSet:
        drawCurve(c[0], closed=c[1], drawImage=True)
    drawCurve(temporaryCurve[0], closed=temporaryCurve[1], drawImage=True)

def drawCurve(curveSet, closed=True, thickness=1, strokeColor=color(0), drawImage=False, imageCurveColor=color(255, 0, 0), connected=True):
    ImageGraphics.strokeWeight(thickness)
    DomainGraphics.strokeWeight(thickness)
    # strokeWeight(thickness)
    s = 0
    if closed:
        s = -1
    e = len(curveSet)
    if connected:
        e -= 1

    for i in range(s, e):
        if (curveSet[i] == None):
            continue

        p1 = convertComplexToWindow(curveSet[i])
        DomainGraphics.stroke(strokeColor)
        DomainGraphics.fill(strokeColor)
        if connected:
            if (curveSet[i + 1] == None):
                return
            p2 = convertComplexToWindow(curveSet[i + 1])
            DomainGraphics.line(p1.x, p1.y, p2.x, p2.y)
        else:
            DomainGraphics.ellipse(p1.x, p1.y, 3, 3)
        # stroke(strokeColor)
        #line(p1.x, p1.y, p2.x, p2.y)

        if drawImage:
            # pushMatrix()
            # translate(width/2,0)
            p1 = convertComplexToWindow(
                transformation.transformation(curveSet[i]))
            ImageGraphics.stroke(imageCurveColor)
            ImageGraphics.fill(imageCurveColor)
            if (curveSet[i] == None):
                return
            if connected:
                p2 = convertComplexToWindow(
                    transformation.transformation(curveSet[i + 1]))
                if (curveSet[i + 1] == None):
                    return
                ImageGraphics.line(p1.x, p1.y, p2.x, p2.y)
            else:
                ImageGraphics.ellipse(p1.x, p1.y, 3, 3)
            # stroke(imageCurveColor)
            #line(p1.x, p1.y, p2.x, p2.y)

          #  popMatrix()
