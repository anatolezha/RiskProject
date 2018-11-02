from tkinter import *
import start as Back

class GUI():
    
    def initFrame(self):
        
        root = Tk()
        return(root)

    def createGrid(self, root):
        buttons = [None for i in range(self.ROW_COUNT * self.COLUMN_COUNT)]
        for i in range(len(buttons)):
            buttons[i] = Button(root, height="5", width="10")
        return(buttons)

    def displayGrid(self, buttons):
        i = 0
        j = 0
        for button in buttons:
            if(i%self.COLUMN_COUNT == 0):
                j += 1
                i = 0
            i += 1
            button.grid(row=j, column=i, padx=0, ipadx=0, pady=0, ipady=0)

    def refreshGrid(self, buttons, board):
        index = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j][0] == 1:
                    color = "#0000FF"
                elif board[i][j][0] == 2:
                    color = "#FF0000"
                buttons[index].configure(text=board[i][j][1], background=color,
                                         font=('arial', 16, 'bold'), foreground="white")
                index += 1

    def setGridSize(self, root, scale):
        self.TABLE_SIZE = scale.get()
        root.destroy()

    def askForGridSize(self, text, minVal, maxVal):
        root = self.initFrame()
        s = Scale(root, orient='horizontal', from_=minVal, to=maxVal,
                  resolution=1, tickinterval=1, sliderlength=20,
                  troughcolor="#BCF5A9", activebackground="green",
                  label=text, length=350)
        s.grid(padx=0, pady=1)
        b = Button(root, text="Valider", command=lambda : self.setGridSize(root, s))
        b.grid(padx=0, pady=2)
        root.mainloop()

    def setNumberOfUnits(self, root, scale):
        self.UNITS = scale.get()
        root.destroy()

    def askForNumberOfUnits(self, text, minVal, maxVal):
        root = self.initFrame()
        s = Scale(root, orient='horizontal', from_=minVal, to=maxVal,
                  resolution=1, tickinterval=5, sliderlength=20,
                  troughcolor="#BCF5A9", activebackground="green",
                  label=text, length=350)
        s.grid(padx=0, pady=1)
        b = Button(root, text="Valider", command=lambda : self.setNumberOfUnits(root, s))
        b.grid(padx=0, pady=2)
        root.mainloop()

    def __init__(self):

        self.ROW_COUNT = 3
        self.COLUMN_COUNT = 3
        self.TABLE_SIZE = 3
        self.UNITS = 3
        
        self.askForGridSize("Donnez la taille du plateau", 2, 10)
        
        self.ROW_COUNT = self.TABLE_SIZE
        self.COLUMN_COUNT = self.TABLE_SIZE

        print(str(self.ROW_COUNT) + " | " + str(self.COLUMN_COUNT))
        
        self.askForNumberOfUnits("Donnez le nombre de pion par joueur", self.TABLE_SIZE*self.TABLE_SIZE/2, 60)
        #size = self.TABLE_SIZE
        #nbPawn = self.UNITS
        repartCase = Back.createBoard(self.TABLE_SIZE)
        casePerPlayer = Back.countCase(repartCase)
        print(str(self.UNITS) + " " + str(casePerPlayer[0]) + " - " + str(self.UNITS) + " " + str(casePerPlayer[1]))
        repartPawn = Back.distribute(self.UNITS, casePerPlayer[0]) + Back.distribute(self.UNITS, casePerPlayer[1])
        board = list(zip(repartCase, repartPawn))
        Back.shuffle(board)
        print(Back.countPawn(board))
        board = list(Back.chunks(board, int(self.TABLE_SIZE)))
        for i in range(len(board)):
            print(board[i])

        
        root = self.initFrame()
        buttons = self.createGrid(root)
        self.displayGrid(buttons)
        self.refreshGrid(buttons, board)
        root.mainloop()

GUI()
