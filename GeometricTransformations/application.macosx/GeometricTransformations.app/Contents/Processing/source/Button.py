import Transformations
allButtons = []

class Button(object):

    def __init__(self, x, y, w, h, label, action):
        allButtons.append(self)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label
        self.action = action
        
        self.strokeColor = color(0)

    def drawButton(self):
        strokeWeight(2)
        stroke(self.strokeColor)
        fill(255)
        rect(self.x, self.y, self.w, self.h)
        textAlign(CENTER, CENTER)
        textSize(12)
        fill(0)
        text(self.label, self.x + self.w / 2, self.y + self.h / 2)

    def mouseOver(self):
        return (mouseX >= self.x and mouseX <= self.x + self.w and mouseY >= self.y and mouseY <= self.y + self.h)


def testButtons(config):
    for b in allButtons:
        if b.mouseOver():
            b.action(config)
            return True
    return False

def gridButtonAction(config):
    config.showGrid = not config.showGrid
def ellipseButtonAction(config):
    config.ellipseOn = not config.ellipseOn
def resetButtonAction(config):
    config._reset()
def zoomInButtonAction(config):
    config.zoomIn()
def zoomOutButtonAction(config):
    config.zoomOut()
def saveButtonAction(config):
    config.save()
def customButtonAction(config):
    config.customInField = True
    
def setupButtons():
    gridButton = Button(5, 5, 100, 20, "Show/Hide Grid", gridButtonAction)
    ellipseButton = Button(110,5,100,20,"Draw Ellipse", ellipseButtonAction)
    resetButton = Button(215,5,100,20,"Reset",resetButtonAction)
    zoomInButton = Button(320,5,20,20, "+",zoomInButtonAction)
    zoomOutButton = Button(345,5,20,20, "-",zoomOutButtonAction)
    saveButton = Button(370,5,100,20,"Save", saveButtonAction)
    customButton = Button(475,5,100,20,"Custom",customButtonAction)
    
    i=0
    actions = [lambda config: config.setTransformation(Transformations.transformations[0]), lambda config: config.setTransformation(Transformations.transformations[1]),
               lambda config: config.setTransformation(Transformations.transformations[2]), lambda config: config.setTransformation(Transformations.transformations[3]),
               lambda config: config.setTransformation(Transformations.transformations[4])]
    for trans in Transformations.transformations:
        CIButton = Button(5+105*i,30, 100,20, trans.name, actions[i])
        i+=1
        
def drawButtons():
    for b in allButtons:
        b.drawButton()
