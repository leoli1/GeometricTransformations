allButtons = []

showGrid = False

class Button(object):
    
    def __init__(self, x,y,w,h,label, action):
        allButtons.append(self)
        self.x=x
        self.y=y
        self.w=w
        self.h=h
        self.label = label
        self.action = action

    def drawButton(self):
       stroke(0)
       fill(255)
       rect(self.x,self.y,self.w,self.h)
       textAlign(CENTER,CENTER)
       textSize(12)
       fill(0)
       text(self.label,self.x+self.w/2,self.y+self.h/2)
    def mouseOver(self):
        return (mouseX>=self.x and mouseX<=self.x+self.w and mouseY>=self.y and mouseY<=self.y+self.h)
    
    
def testButtons():
    for b in allButtons:
        if b.mouseOver():
            b.action()
            return True
    return False
    
def setupButtons():
    def gridButtonAction():
        global showGrid
        showGrid = not showGrid
    gridButton = Button(5,5,100,20,"Show/Hide Grid", gridButtonAction)
    
def drawButtons():
    for b in allButtons:
        b.drawButton()