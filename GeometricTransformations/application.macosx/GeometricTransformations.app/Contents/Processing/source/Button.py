allButtons = []

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
       text(self.x+self.w/2,self.y+self.h/2,self.label)
    def mouseOver(self):
        return (mouseX>=x and mouseX<=x+w and mouseY>=y and mouseY<=y+h)
    
    
def testButtons():
    for b in allButtons:
        if b.mouseOver():
            b.action()
            return True
    return False
    
def setupButtons():
    pass