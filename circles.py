from tkinter import *
from datetime import datetime
import math

t = Tk()
t.resizable(False, False)
c = Canvas(t, width=720, height=480, bg="#ffffff")
c.pack()

class Object:
    def __init__(self, x, y, z=0, shape="circle", colour="#000000"):
        self.x = x
        self.y = y
        self.z = z
        self.properties = {"shape" : shape, "colour" : colour, "moveable" : True}

    def move(self, x, y):
        self.x += x
        self.y += y

    def setZIndex(self, z):
        self.z = z

    def distance(self, x1, y1):
        xChange = abs(self.x - x1)
        yChange = abs(self.y - y1)
        return math.sqrt(xChange ** 2 + yChange ** 2)

    def setProperty(self, name, value):
        self.properties[name] = value

    def hasProperty(self, name):
        return name in self.properties

    def containsPoint(self, x, y):
        if self.getProperty("shape") == "circle":
            radius = self.getProperty("radius")
            if radius == None:
                radius = 5
            dist = self.distance(x, y)
            return dist < radius
        return False

    def getProperty(self, name):
        if self.hasProperty(name):
            return self.properties[name]
        return None

objects = {}
global draggedObject
draggedObject = None

def drag(event):
    global draggedObject
    if draggedObject != None:
        draggedObject.x = event.x
        draggedObject.y = event.y
        onMove = draggedObject.getProperty("onmove")
        if onMove != None:
            onMove()
    else:
        for objK in objects:
            obj = objects[objK]
            moveable = obj.getProperty("moveable")
            if moveable != None and moveable == False:
                continue
            if obj.containsPoint(event.x, event.y):
                draggedObject = obj
                break

def release(event):
    global draggedObject
    draggedObject = None

t.bind("<B1-Motion>", drag)
t.bind("<ButtonRelease-1>", release)

oldTime = datetime.now().timestamp()
currTime = datetime.now().timestamp()

objects["a"] = Object(0, 0, 10)
objects["a"].setProperty("moveable", False)
objects["b"] = Object(0, 0, 10)
objects["b"].setProperty("moveable", False)

def moveBoth():
    objects["tcircle"].x = objects["x"].x + objects["tcircle"].getProperty("radius")
    objects["tcircle"].y = objects["x"].y
    
    objects["scircle"].x = objects["x"].x - objects["scircle"].getProperty("radius")
    objects["scircle"].y = objects["x"].y

    objects["a"].x = objects["scircle"].x
    objects["a"].y = objects["scircle"].y - objects["scircle"].getProperty("radius")

    objects["b"].x = objects["tcircle"].x
    objects["b"].y = objects["tcircle"].y - objects["tcircle"].getProperty("radius")


objects["scircle"] = Object(100, 100, colour="#ff0000")
objects["scircle"].setProperty("radius", 20)
objects["scircle"].setProperty("moveable", False)

def sResize():
    objects["ssize"].y = 50

    if objects["ssize"].x < 60:
        objects["ssize"].x = 60
    elif objects["ssize"].x > 210:
        objects["ssize"].x = 210
    
    objects["scircle"].setProperty("radius", objects["ssize"].x - 50)
    moveBoth()

objects["ssize"] = Object(100, 50, 10, colour="#ff0000")
objects["ssize"].setProperty("onmove", sResize)

objects["sbar"] = Object(60, 50, -1, "line", "#555555")
objects["sbar"].setProperty("moveable", False)
objects["sbar"].setProperty("length", 150)
objects["sbar"].setProperty("orientation", "horizontal")


objects["tcircle"] = Object(100, 100, colour="#0000ff")
objects["tcircle"].setProperty("radius", 20)
objects["tcircle"].setProperty("moveable", False)

def tResize():
    objects["tsize"].y = 50

    if objects["tsize"].x < 510:
        objects["tsize"].x = 510
    elif objects["tsize"].x > 660:
        objects["tsize"].x = 660
    
    objects["tcircle"].setProperty("radius", objects["tsize"].x - 500)
    moveBoth()

objects["tsize"] = Object(550, 50, 10, colour="#0000ff")
objects["tsize"].setProperty("onmove", tResize)

objects["tbar"] = Object(510, 50, -1, "line", "#555555")
objects["tbar"].setProperty("moveable", False)
objects["tbar"].setProperty("length", 150)
objects["tbar"].setProperty("orientation", "horizontal")

objects["x"] = Object(360, 240, 10)

objects["x"].setProperty("onmove", moveBoth)

moveBoth()
sResize()
tResize()

while True:
    currTime = datetime.now().timestamp()
    if datetime.fromtimestamp(currTime - oldTime).microsecond > 10000:
        oldTime = currTime
        c.delete("all")
        
        for objKey in sorted(objects, key=lambda objK: objects[objK].z):
            obj = objects[objKey]
            shape = obj.getProperty("shape")
            colour = obj.getProperty("colour")
            if shape == "circle":
                radius = obj.getProperty("radius")
                if radius == None:
                    radius = 5
                c.create_oval(obj.x - radius, obj.y - radius, obj.x + radius, obj.y + radius, fill=colour)
            elif shape == "line":
                length = obj.getProperty("length")
                if length == None:
                    length = 5
                orientation = obj.getProperty("orientation")
                if orientation == None or orientation != "vertical":
                    orietation = "horizontal"
                if orientation == "horizontal":
                    c.create_line(obj.x, obj.y, obj.x + length, obj.y, fill=colour)
                else:
                    c.create_line(obj.x, obj.y, obj.x, obj.y + length, fill=colour)
        
        c.update()
        t.update()
