import tkinter as tk
import tkinter.font as tkFont


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
        self.drawGrid()
        self.showFrame(0)
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

    def drawGrid(self,):
        for i in range(0,1000,43):
            self.theCanvas.create_line(0,self.boardBuffer + i,1000, self.boardBuffer + i,fill="black")
game = App()
