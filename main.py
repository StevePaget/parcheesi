import tkinter as tk
import tkinter.font as tkFont
import math, random
from collections import defaultdict

class Gamestate:
    def __init__(self, posArrays, main):
        self.players = [Player(i, posArrays[i], main) for i in range(4)]
        self.currentPlayer = 0
        self.turnstate = 0
        self.currentDice = [0,0]
        self.selectedPiece = None

class Position:
    def __init__(self,x1,y1,x2,y2,postype):
        self.coords = ((x1,y1),(x2,y2)) # coordinates for the two possible pieces in this space
        self.type = postype
        self.contents = [None, None] # the Pieces in this position
    
    def removePiece(self, piece): 
        if self.contents[0] == piece:
            self.contents[0] = None
            if self.contents[1] is not None:
                self.contents[0] = self.contents[1]
                self.contents[1] = None
        elif self.contents[1] == piece:
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
    
    def canAdd(self,piece):
        if self.contents[0] is None:
            return 0
        elif self.contents[1] is None and piece.player == self.contents[0].player:
            return 1
        else:
            return False

class Ghost:
    def __init__(self,position,side,main):
        self.position = position
        self.main = main
        self.id = self.main.theCanvas.create_image(position.coords[side][0],position.coords[side][1],image=self.main.ghostImage)

class Piece:
    def __init__(self,player, position, side, main):
        self.position = position
        self.side = side
        self.player = player
        self.main = main
        self.possiblepositions = []
        colours = ["green","yellow","blue","red"]
        self.image = tk.PhotoImage(file="images/" + colours[self.player]+".png")
        self.image2 = tk.PhotoImage(file="images/" + colours[self.player]+"2.png")
        self.pieceID = main.theCanvas.create_image(self.position.coords[self.side][0],self.position.coords[self.side][1], image=self.image)
        main.theCanvas.tag_bind(self.pieceID, "<Enter>", self.enter)
        main.theCanvas.tag_bind(self.pieceID, "<Leave>", self.leave)
        main.theCanvas.tag_bind(self.pieceID, "<Button-1>", self.clicked)        
        main.allPieces[self.pieceID] = self

    def move(self,oldposition, newposition):
        if newposition.addPiece(self):
            oldposition.removePiece(self)
            self.main.theCanvas.coords(self.pieceID, self.position.coords[self.side][0],self.position.coords[self.side][1],self.position.coords[self.side][0]+20,self.position.coords[self.side][1]+20)
        else:
            print(f"Cannot move {oldposition.name} to {newposition.name}")
            return False
        
    def enter(self,e):
        if self.main.gamestate.turnstate != 1 or self.main.gamestate.currentPlayer != self.player:
            return
        if self.main.gamestate.selectedPiece is None: # nothing currently selected
            self.highlight()

    def highlight(self):
        self.main.theCanvas.itemconfig(self.pieceID, image = self.image2)
        self.getValidPlaces()

    def leave(self,e):
        if self.main.gamestate.turnstate != 1 or self.main.gamestate.currentPlayer != self.player:
            return
        if self.main.gamestate.selectedPiece is None: #nothing selected
            self.unhighlight()

    def unhighlight(self):
        self.main.theCanvas.itemconfig(self.pieceID, image = self.image)
        self.main.clearGhosts()

    def clicked(self,e):
        if self.main.gamestate.turnstate == 1:
            if self.main.gamestate.selectedPiece is None: # no selected piece
                self.main.gamestate.selectedPiece = self
                if len(self.possiblepositions)>0:
                    print("Fresh - showing spaces")
                else:
                    print("Fresh - No valid spaces")
            else:
                if self.main.gamestate.selectedPiece == self: #already selected this piece, so deselect
                    self.unhighlight()
                    self.main.gamestate.selectedPiece = None
                    print("Deselected")
                else: # other piece. cancel old one and select this
                    self.main.gamestate.selectedPiece.unhighlight()
                    self.main.gamestate.selectedPiece = self
                    self.highlight()
                    if len(self.possiblepositions)>0:
                        print("swap - showing spaces")
                    else:
                        print("Swap - No valid spaces")


    def getValidPlaces(self):
        d1,d2 = self.main.gamestate.currentDice
        self.possiblepositions = set()
        self.main.clearGhosts()
        # do they have any fives?
        if d1 == 5 or d2 == 5:
        # is this piece in the home?
            if self.position.type == "start":            
                # check d1
                if d1 == 5:
                    pos = self.main.gamestate.players[self.player].posarray[2]
                    side = pos.canAdd(self)
                    if side is not False:
                        self.main.addGhost(pos,side)
                        self.possiblepositions.add(pos)


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

    def getPosition(self, original, distance):
        start = self.posarray.index(original)
        end = self.posarray[start+ distance]
        return end

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
        self.loadDice()
        self.showFrame(1)
        #self.theCanvas.bind("<Motion>",self.testmouse)
        self.highlights = []
        self.allPieces = {}
        self.startGame()
        self.mainloop()

    def makeBoard(self):
        self.boardImage = tk.PhotoImage(file="images/board.png")
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

        
    def loadDice(self):
        self.dice=[None]
        for i in range(1,7):
            self.dice.append((tk.PhotoImage(file="images/" + str(i)+".png"),tk.PhotoImage(file="images/" + str(i)+"a.png")))


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
        rollbutton = tk.Button(self.gameplayFrame,text="Roll", font=self.smallmono, command = lambda :self.roll(6))
        rollbutton.grid(row=5,column=1)
        self.gameplayFrame.rowconfigure(0,minsize=50)
        self.gameplayFrame.rowconfigure(1,minsize=50)
        self.gameplayFrame.rowconfigure(2,minsize=200)
        self.gameplayFrame.rowconfigure(3,minsize=50)
        self.gameplayFrame.columnconfigure(0,minsize=30)
        self.gameplayFrame.columnconfigure(2,minsize=30)
        self.gameplayFrame.columnconfigure(1,weight=100)
        self.gameplayFrame.rowconfigure(6, weight=100)
        
    def roll(self, rolls):
        if self.gamestate.turnstate == 0:
            d1 = random.randint(1,6)
            d2 = random.randint(1,6)
            d1=5
            self.diceCanvas.delete(tk.ALL)
            self.diceCanvas.create_image(100,80,image=random.choice(self.dice[d1]))
            self.diceCanvas.create_image(100,210,image=random.choice(self.dice[d2]))
            if rolls > 0:
                self.after(100, lambda: self.roll(rolls-1))
            else:
                self.completeRoll(d1,d2)

    def completeRoll(self,d1,d2):
        self.gamestate.currentDice = [d1,d2]
        self.gamestate.turnstate = 1

    def makePosArrays(self):
        f = open("textfiles/places.txt","r")
        line = f.read()
        lines = line.split("-")
        pos = 0
        mainrun = [None]
        while pos < len(lines)-1:
            p1 = [int(p) for p in lines[pos][1:-1].split(",")]
            p2 = [int(p) for p in lines[pos+1][1:-1].split(",")]
            mainrun.append(Position(p1[0],p1[1],p2[0],p2[1],"normal"))
            pos += 2

        f = open("textfiles/red.txt","r")
        line = f.read()
        lines = line.split("-")
        reds = []
        p1 = [int(p) for p in lines[0][1:-1].split(",")]
        p2 = [int(p) for p in lines[1][1:-1].split(",")]
        self.redStart = Position(p1[0],p1[1],p2[0],p2[1], "start")
        reds.append(self.redStart)
        p1 = [int(p) for p in lines[2][1:-1].split(",")]
        p2 = [int(p) for p in lines[3][1:-1].split(",")]
        newPos = Position(p1[0],p1[1],p2[0],p2[1], "start")
        reds.append(newPos)
        reds = reds + mainrun[39:] + mainrun[1:35]
        for linenum in range(4,len(lines),2):
            p1 = [int(p) for p in lines[linenum][1:-1].split(",")]
            p2 = [int(p) for p in lines[linenum+1][1:-1].split(",")]
            newPos = Position(p1[0],p1[1],p2[0],p2[1], "home")
            reds.append(newPos)

        #self.testrun(reds,"red")

        f = open("textfiles/green.txt","r")
        line = f.read()
        lines = line.split("-")
        greens = []
        p1 = [int(p) for p in lines[0][1:-1].split(",")]
        p2 = [int(p) for p in lines[1][1:-1].split(",")]
        self.greenStart = Position(p1[0],p1[1],p2[0],p2[1], "start")
        greens.append(self.greenStart)
        p1 = [int(p) for p in lines[2][1:-1].split(",")]
        p2 = [int(p) for p in lines[3][1:-1].split(",")]
        newPos = Position(p1[0],p1[1],p2[0],p2[1], "start")
        greens.append(newPos)
        greens = greens + mainrun[5:69]
        for linenum in range(4,len(lines),2):
            p1 = [int(p) for p in lines[linenum][1:-1].split(",")]
            p2 = [int(p) for p in lines[linenum+1][1:-1].split(",")]
            newPos = Position(p1[0],p1[1],p2[0],p2[1], "home")
            greens.append(newPos)

        #self.testrun(greens,"lightgreen")

        f = open("textfiles/blue.txt","r")
        line = f.read()
        lines = line.split("-")
        blues = []
        p1 = [int(p) for p in lines[0][1:-1].split(",")]
        p2 = [int(p) for p in lines[1][1:-1].split(",")]
        self.blueStart = Position(p1[0],p1[1],p2[0],p2[1], "start")
        blues.append(self.blueStart)
        p1 = [int(p) for p in lines[2][1:-1].split(",")]
        p2 = [int(p) for p in lines[3][1:-1].split(",")]
        newPos = Position(p1[0],p1[1],p2[0],p2[1], "start")
        blues.append(newPos)
        blues = blues + mainrun[22:69] + mainrun[1:18]
        for linenum in range(4,len(lines),2):
            p1 = [int(p) for p in lines[linenum][1:-1].split(",")]
            p2 = [int(p) for p in lines[linenum+1][1:-1].split(",")]
            newPos = Position(p1[0],p1[1],p2[0],p2[1], "home")
            blues.append(newPos)

        #self.testrun(blues,"lightblue")

        f = open("textfiles/yellow.txt","r")
        line = f.read()
        lines = line.split("-")
        yellows = []
        p1 = [int(p) for p in lines[0][1:-1].split(",")]
        p2 = [int(p) for p in lines[1][1:-1].split(",")]
        self.yellowStart = Position(p1[0],p1[1],p2[0],p2[1], "start")
        yellows.append(self.yellowStart)
        p1 = [int(p) for p in lines[2][1:-1].split(",")]
        p2 = [int(p) for p in lines[3][1:-1].split(",")]
        newPos = Position(p1[0],p1[1],p2[0],p2[1], "start")
        yellows.append(newPos)
        yellows = yellows + mainrun[56:69] + mainrun[1:52]
        for linenum in range(4,len(lines),2):
            p1 = [int(p) for p in lines[linenum][1:-1].split(",")]
            p2 = [int(p) for p in lines[linenum+1][1:-1].split(",")]
            newPos = Position(p1[0],p1[1],p2[0],p2[1], "home")
            yellows.append(newPos)

        #self.testrun(yellows,"yellow")
        return greens, yellows, blues, reds

    def startGame(self):
        # make the pieces and put them in the correct positions
        self.gamestate = Gamestate(self.makePosArrays(), self)
        self.sortlayers()
        self.turnCounterImage = tk.PhotoImage(file = "images/turnbutton.png")
        self.ghostImage = tk.PhotoImage(file="images/ghost.png")
        self.ghosts = set()
        self.ghoststate = True
        self.turnCounter = self.theCanvas.create_image(0,0,image = self.turnCounterImage)
        self.updateTurnCounter()
        self.flashjob = False
        # the game loop is run on the following events
        # turn status 0: Waiting for dice roll
        # turn status 1: Dice rolled, waiting for player piece choice
        # turn status 2: Piece chosen. Display target positions. Waiting for choice of destination
        # turn status 3: Destination chosen. Move piece. Deal with bounces.
        #                Deduct die value from choices and repeat status 1 if necessary
        # turn status 4: Turn complete. Detect if game won. Switch players, go to status 0

    def displayMessage(self, message):
        self.infoBox.config(text=message)


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
            self.theCanvas.tag_raise(p.pieceID)

    def updateTurnCounter(self):
        self.displayMessage(f"Player {self.gamestate.currentPlayer + 1}\n\nPlease roll the dice.")
        positions = [(200,200), (200,800),(800,200),(800,800)]
        self.theCanvas.coords(self.turnCounter, positions[self.gamestate.currentPlayer][0], positions[self.gamestate.currentPlayer][1])

    def addGhost(self,pos,side):
        self.ghosts.add(Ghost(pos,side,self))
        print("Add")
        print(len(self.ghosts))
        if not self.flashjob:
            self.flashGhosts()
            print("Start flash")

    def clearGhosts(self):
        for g in self.ghosts:
            self.theCanvas.delete(g.id)
        self.ghosts = set()
        if self.flashjob:
            self.after_cancel(self.flashjob)
            self.flashjob = None
        print("Stop flash")
        
    def flashGhosts(self):
        for g in self.ghosts:
            if self.ghoststate:
                self.theCanvas.itemconfig(g.id,state="hidden")
            else:
                self.theCanvas.itemconfig(g.id,state="normal")
        self.ghoststate = not self.ghoststate
        self.flashjob = self.after(500,self.flashGhosts)

game = App()