import tkinter as tk
import tkinter.font as tkFont
import math

class App(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("1500x1000+0+0")
        self.title("Parcheesi")
        self.titlefont = tkFont.Font(family="Arial", size=20, slant="italic")
        self.smallmono = tkFont.Font(family="consolas", size=15)
        self.theCanvas = tk.Canvas(self,width=1000,height=1000,bg="blue")
        self.theCanvas.grid(row=0,column=0, sticky="NW")
        self.frames = [ ]
        self.columnconfigure(1,weight=100)
        self.addConnectionFrame()
        self.makeBoard()
        self.showFrame(0)
        #self.theCanvas.bind("<Button>",self.clicking)
        self.theCanvas.bind("<Motion>",self.testmouse)
        self.makePosArrays()
        self.highlights = []
        self.mainloop()


    def makeBoard(self):
        self.boardImage = tk.PhotoImage(file="board.png")
        self.theCanvas.create_image(0,0, image = self.boardImage, anchor="nw")
        self.boardBuffer = 52

    def connect(self):
        # connect to network
        # get a player ID
        pass

    def showFrame(self, frameNumber):
        for f in range(len(self.frames)):
            if f == frameNumber:
                self.frames[f].grid(row=0, column=1, sticky="NSEW")
            else:
                self.frames[f].grid_forget()

    def testmouse(self,e):
        nearestDist = math.inf
        nearestPos = None
        for square in range(1,69):
            p1 = self.positions[square][0]
            p2 = self.positions[square][1]
            dist = math.sqrt((p1[0]-e.x)**2 + (p1[1]-e.y)**2)
            if dist < nearestDist:
                nearestDist = dist
                nearestPos = square,p1
            dist = math.sqrt((p2[0]-e.x)**2 + (p2[1]-e.y)**2)
            if dist < nearestDist:
                nearestDist = dist
                nearestPos = square,p2
        for h in self.highlights:
            self.theCanvas.delete(h)
        self.highlights.append(self.theCanvas.create_oval(nearestPos[1][0],nearestPos[1][1],nearestPos[1][0]+20,nearestPos[1][1]+20,fill="green" ))

        

    def addConnectionFrame(self):
        self.connectionFrame = tk.Frame(self, bg="#dba6ea")
        cl1 = tk.Label(self.connectionFrame, text="Connecting to game", font=self.titlefont,bg="#dba6ea")
        cl1.grid(row=0, column=0, sticky="NEW")
        self.frames.append(self.connectionFrame)
        self.cl2 = tk.Label(self.connectionFrame, text="Connection information\nwill appear here", justify="left", font=self.smallmono,bg="#ead7ef") 
        self.cl2.grid(row=3,column=0,sticky="NSEW")
        cb1 = tk.Button(self.connectionFrame, text="Start Game")
        cb1. grid(row=4,column=0, sticky="EW")
        self.connectionFrame.rowconfigure(1,minsize=50)
        self.connectionFrame.rowconfigure(3,weight=80)
        self.connectionFrame.rowconfigure(4,weight=20)
        self.connectionFrame.columnconfigure(0,weight=100)

    def makePosArrays(self):
        f = open("places.txt","r")
        line = f.read()
        lines = line.split("-")
        self.positions = [None]
        pos = 0
        while pos < len(lines)-1:
            self.positions.append((eval(lines[pos]),eval(lines[pos+1])))
            pos += 2

        f = open("red.txt","r")
        line = f.read()
        lines = line.split("-")
        self.redpos = []
        pos = 0
        while pos < len(lines)-1:
            self.redpos.append((eval(lines[pos]),eval(lines[pos+1])))
            pos += 2

        f = open("green.txt","r")
        line = f.read()
        lines = line.split("-")
        self.greenpos = []
        pos = 0
        while pos < len(lines)-1:
            self.greenpos.append((eval(lines[pos]),eval(lines[pos+1])))
            pos += 2


        f = open("yellow.txt","r")
        line = f.read()
        lines = line.split("-")
        self.yellowpos = []
        pos = 0
        while pos < len(lines)-1:
            self.yellowpos.append((eval(lines[pos]),eval(lines[pos+1])))
            pos += 2

        f = open("blue.txt","r")
        line = f.read()
        lines = line.split("-")
        self.bluepos = []
        pos = 0
        while pos < len(lines)-1:
            self.bluepos.append((eval(lines[pos]),eval(lines[pos+1])))
            pos += 2

    def clicking(self,e):
        f = open("blue.txt","a")
        f.write(f"({e.x},{e.y})-")
        f.close()
        print(e.x, e.y)
        self.theCanvas.create_rectangle(e.x-10,e.y-10,e.x+10, e.y+10,fill="red")

game = App()
