import tkinter as tk
import tkinter.font as tkFont
import math
from collections import defaultdict

class Gamestate:
    def __init__(self, posArrays, canvas):
        self.players = [Player(i, posArrays[i], canvas) for i in range(4)]


class Dice:
    def __init__(self, canvas):
        self.canvas = canvas

class Position:
    def __init__(self,x1,y1,x2,y2,name):
        self.coords = ((x1,y1),(x2,y2)) # coordinates for the two possible pieces in this space
        self.name = name
        self.contents = [None, None] # the Pieces in this position
    
    def removePiece(self, piece): 
        if self.contents[0] == piece:
            self.contents[0] = None
        if self.contents[1] == piece:
            self.contents[1] = None

    def addPiece(self,piece): # Returns True if successful
        if self.contents[0] == None:
            self.contents[0] = piece
            piece.position = self
            piece.side = 0
        elif self.contents[1] == None:
            self.contents[1] = piece
            piece.position = self
            piece.side = 1
        else:
            return False
        return True


class Piece:
    def __init__(self,player, position, side, main):
        self.position = position
        self.side = side
        self.player = player
        self.main = main
        colours = ["green","yellow","blue","red"]
        self.image = tk.PhotoImage(file=colours[self.player]+".png")
        self.image2 = tk.PhotoImage(file=colours[self.player]+"2.png")
        self.pieceID = main.theCanvas.create_image(self.position.coords[self.side][0],self.position.coords[self.side][1], image=self.image)
        main.theCanvas.tag_bind(self.pieceID, "<Enter>", self.highlight)
        main.theCanvas.tag_bind(self.pieceID, "<Leave>", self.unhighlight)
        main.theCanvas.tag_bind(self.pieceID, "<Button-1>", self.clicked)        
        main.allPieces[self.pieceID] = self

    def move(self, canvas,oldposition, newposition):
        if newposition.addPiece(self):
            oldposition.removePiece(self)
            self.main.theCanvas.coords(self.pieceID, self.position.coords[self.side][0],self.position.coords[self.side][1],self.position.coords[self.side][0]+20,self.position.coords[self.side][1]+20)
        else:
            print(f"Cannot move {oldposition.name} to {newposition.name}")
            return False
        
    def highlight(self,e):
        self.main.theCanvas.itemconfig(self.pieceID, image = self.image2)

    def unhighlight(self,e):
        self.main.theCanvas.itemconfig(self.pieceID, image = self.image)

    def clicked(self,e):
        print(self.player)

class Player:
    def __init__(self, playerID,posarray, main):
        self.ID = playerID
        self.pieces = []
        self.posarray = posarray
        self.main =main
        self.pieces.append(Piece(playerID, posarray[0], 0, main))
        self.pieces.append(Piece(playerID, posarray[0], 1, main))
        self.pieces.append(Piece(playerID, posarray[1], 0, main))
        self.pieces.append(Piece(playerID, posarray[1], 1, main))



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
        self.addGameplayFrame()
        self.makeBoard()
        self.showFrame(1)
        #self.theCanvas.bind("<Motion>",self.testmouse)
        self.highlights = []
        self.allPieces = {}
        self.startGame()
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
        for pos in range(len(self.positions[self.currentPlayer])):
            p1 = self.positions[self.currentPlayer][pos][0]
            p2 = self.positions[self.currentPlayer][pos][1]
            dist = math.sqrt((p1[0]-e.x)**2 + (p1[1]-e.y)**2)
            if dist < nearestDist:
                nearestDist = dist
                nearestPos = pos,p1
            dist = math.sqrt((p2[0]-e.x)**2 + (p2[1]-e.y)**2)
            if dist < nearestDist:
                nearestDist = dist
                nearestPos = pos,p2
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

    def addGameplayFrame(self):
        self.gameplayFrame = tk.Frame(self, bg="#0a751f")
        cl1 = tk.Label(self.gameplayFrame, text="Let's Play!", anchor = tk.CENTER, font=self.titlefont,fg = "#FFFFFF", bg="#0a751f")
        cl1.grid(row=0, column=1, sticky="NSEW")
        self.frames.append(self.gameplayFrame)
        self.infoBox = tk.Label(self.gameplayFrame, text="Gameplay Info\nHere", anchor = tk.NW, justify=tk.LEFT, font=self.smallmono,fg = "#FFFFFF", bg="#000000")
        self.infoBox.grid(row=2, column=1, sticky="NSEW")
        self.diceCanvas = tk.Canvas(self.gameplayFrame,width=200,height=300,bg="black")
        self.diceCanvas.grid(row=4,column=1)
        rollbutton = tk.Button(self.gameplayFrame,text="Roll", font=self.smallmono, command = self.roll)
        rollbutton.grid(row=5,column=1)
        self.gameplayFrame.rowconfigure(0,minsize=50)
        self.gameplayFrame.rowconfigure(1,minsize=50)
        self.gameplayFrame.rowconfigure(2,minsize=200)
        self.gameplayFrame.rowconfigure(3,minsize=50)
        self.gameplayFrame.columnconfigure(0,minsize=30)
        self.gameplayFrame.columnconfigure(2,minsize=30)
        self.gameplayFrame.columnconfigure(1,weight=100)
        self.gameplayFrame.rowconfigure(6, weight=100)
        
    def roll(self):
        return


    def makePosArrays(self):
        f = open("places.txt","r")
        line = f.read()
        lines = line.split("-")
        pos = 0
        mainrun = [None]
        while pos < len(lines)-1:
            p1 = [int(p) for p in lines[pos][1:-1].split(",")]
            p2 = [int(p) for p in lines[pos+1][1:-1].split(",")]
            mainrun.append(Position(p1[0],p1[1],p2[0],p2[1],str((pos//2)+1)))
            pos += 2

        f = open("red.txt","r")
        line = f.read()
        lines = line.split("-")
        reds = []
        p1 = [int(p) for p in lines[0][1:-1].split(",")]
        p2 = [int(p) for p in lines[1][1:-1].split(",")]
        self.redStart = Position(p1[0],p1[1],p2[0],p2[1], "redStart12")
        reds.append(self.redStart)
        p1 = [int(p) for p in lines[2][1:-1].split(",")]
        p2 = [int(p) for p in lines[3][1:-1].split(",")]
        newPos = Position(p1[0],p1[1],p2[0],p2[1], "redStart34")
        reds.append(newPos)
        reds = reds + mainrun[39:] + mainrun[1:35]
        for linenum in range(4,len(lines),2):
            p1 = [int(p) for p in lines[linenum][1:-1].split(",")]
            p2 = [int(p) for p in lines[linenum+1][1:-1].split(",")]
            newPos = Position(p1[0],p1[1],p2[0],p2[1], "redEnd")
            reds.append(newPos)

        #self.testrun(reds,"red")

        f = open("green.txt","r")
        line = f.read()
        lines = line.split("-")
        greens = []
        p1 = [int(p) for p in lines[0][1:-1].split(",")]
        p2 = [int(p) for p in lines[1][1:-1].split(",")]
        self.greenStart = Position(p1[0],p1[1],p2[0],p2[1], "greenStart12")
        greens.append(self.greenStart)
        p1 = [int(p) for p in lines[2][1:-1].split(",")]
        p2 = [int(p) for p in lines[3][1:-1].split(",")]
        newPos = Position(p1[0],p1[1],p2[0],p2[1], "greenStart34")
        greens.append(newPos)
        greens = greens + mainrun[5:69]
        for linenum in range(4,len(lines),2):
            p1 = [int(p) for p in lines[linenum][1:-1].split(",")]
            p2 = [int(p) for p in lines[linenum+1][1:-1].split(",")]
            newPos = Position(p1[0],p1[1],p2[0],p2[1], "greenEnd")
            greens.append(newPos)

        #self.testrun(greens,"lightgreen")

        f = open("blue.txt","r")
        line = f.read()
        lines = line.split("-")
        blues = []
        p1 = [int(p) for p in lines[0][1:-1].split(",")]
        p2 = [int(p) for p in lines[1][1:-1].split(",")]
        self.blueStart = Position(p1[0],p1[1],p2[0],p2[1], "blueStart12")
        blues.append(self.blueStart)
        p1 = [int(p) for p in lines[2][1:-1].split(",")]
        p2 = [int(p) for p in lines[3][1:-1].split(",")]
        newPos = Position(p1[0],p1[1],p2[0],p2[1], "blueStart34")
        blues.append(newPos)
        blues = blues + mainrun[22:69] + mainrun[1:18]
        for linenum in range(4,len(lines),2):
            p1 = [int(p) for p in lines[linenum][1:-1].split(",")]
            p2 = [int(p) for p in lines[linenum+1][1:-1].split(",")]
            newPos = Position(p1[0],p1[1],p2[0],p2[1], "blueEnd")
            blues.append(newPos)

        #self.testrun(blues,"lightblue")

        f = open("yellow.txt","r")
        line = f.read()
        lines = line.split("-")
        yellows = []
        p1 = [int(p) for p in lines[0][1:-1].split(",")]
        p2 = [int(p) for p in lines[1][1:-1].split(",")]
        self.yellowStart = Position(p1[0],p1[1],p2[0],p2[1], "yellowStart12")
        yellows.append(self.yellowStart)
        p1 = [int(p) for p in lines[2][1:-1].split(",")]
        p2 = [int(p) for p in lines[3][1:-1].split(",")]
        newPos = Position(p1[0],p1[1],p2[0],p2[1], "yellowStart34")
        yellows.append(newPos)
        yellows = yellows + mainrun[56:69] + mainrun[1:52]
        for linenum in range(4,len(lines),2):
            p1 = [int(p) for p in lines[linenum][1:-1].split(",")]
            p2 = [int(p) for p in lines[linenum+1][1:-1].split(",")]
            newPos = Position(p1[0],p1[1],p2[0],p2[1], "yellowEnd")
            yellows.append(newPos)

        #self.testrun(yellows,"yellow")
        return greens, yellows, blues, reds

    def startGame(self):
        # make the pieces and put them in the correct positions
        self.gamestate = Gamestate(self.makePosArrays(), self)
        self.sortlayers()

    def clicking(self,e):
        f = open("blue.txt","a")
        f.write(f"({e.x},{e.y})-")
        f.close()
        print(e.x, e.y)
        self.theCanvas.create_rectangle(e.x-10,e.y-10,e.x+10, e.y+10,fill="red")
  

    def testrun(self,run,colour):
        fig = self.theCanvas.create_oval(0,0,20,20,fill=colour)
        posnum = 0
        self.after(300, lambda x=fig: self.nextpos(x, posnum, run))
    
    def nextpos(self, fig, posnum,run):
        pos = run[posnum]
        self.theCanvas.coords(fig,pos.coords[0][0],pos.coords[0][1],pos.coords[0][0]+20,pos.coords[0][1]+20)
        posnum +=1
        if posnum < len(run):
            self.after(300, lambda x=fig: self.nextpos(x, posnum, run))
        
    def sortlayers(self):
        listofPieces = list(self.allPieces.values())
        listofPieces.sort(key= lambda p: p.position.coords[p.side][1])
        for p in listofPieces:
            print(p.position.coords[p.side])
            self.theCanvas.tag_raise(p.pieceID)

game = App()