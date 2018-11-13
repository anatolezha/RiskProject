from tkinter import *
import start as Back
import random

class GUI():
    
    def initFrame(self):
        
        root = Tk()
        return(root)

    def createGrid(self, root):
        buttons = [None for i in range(self.ROW_COUNT * self.COLUMN_COUNT)]
        for i in range(len(buttons)):
            buttons[i] = Button(root, height="5", width="10")
        return(buttons)

    def displayGrid(self):
        i = 0
        j = 0
        for button in self.buttons:
            if(i%self.COLUMN_COUNT == 0):
                j += 1
                i = 0
            i += 1
            button.grid(row=j, column=i, padx=0, ipadx=0, pady=0, ipady=0)

    def refreshGrid(self):
        index = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j][0] == 1:
                    color = "#0000FF"
                elif self.board[i][j][0] == 2:
                    color = "#FF0000"
                elif self.board[i][j][0] == 3:
                    color = "#00FFFF"
                self.buttons[index].configure(text=self.board[i][j][1], background=color,
                                         font=('arial', 16, 'bold'), foreground="white")
                index += 1

    def setPlayerCount(self, root, scale):
        self.teamCount = scale.get()
        root.destroy()
        
    def setGridSize(self, root, scale):
        self.TABLE_SIZE = scale.get()
        root.destroy()

    def askPlayerCount(self, text, minVal, maxVal):
        root = self.initFrame()
        s = Scale(root, orient='horizontal', from_=minVal, to=maxVal,
                  resolution=1, tickinterval=1, sliderlength=20,
                  troughcolor="#BCF5A9", activebackground="green",
                  label=text, length=350)
        s.grid(padx=0, pady=1)
        b = Button(root, text="Valider", command=lambda : self.setPlayerCount(root, s))
        b.grid(padx=0, pady=2)
        root.mainloop()

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

    def giveButtonsSelectSourceAction(self):
        for i in range(len(self.buttons)):
            self.buttons[i].configure(command=lambda val=i: self.enableUnitsTargets(val))

    def launchAttack(self, case):
        self.changeAllButtonsState("disabled")
        self.giveButtonsSelectSourceAction()
        x = case//len(self.board)
        y = case - x*len(self.board)
        self.target = (x, y)
        print("Attack : source (" + str(self.source) + ") target (" + str(self.target))
        #####
        self.board = Back.oneAttack(self.board, self.source, self.target)
        if self.team == self.teamCount:
            self.team = 1
        else:
            self.team += 1
        self.refreshGrid()
        self.enableUnitsSources()

    def giveButtonsSelectTargetAction(self):
        for i in range(len(self.buttons)):
            self.buttons[i].configure(command=lambda val=i: self.launchAttack(val))

    def changeAllButtonsState(self, state):
        for i in range(len(self.buttons)):
            self.buttons[i].configure(state=state)

    def changeStateOfOneButton(self, case, state):
        self.buttons[(case[0]*len(self.board[case[0]]))+case[1]].configure(state=state)

    def countEnemisAround(self, case):
        enemisCount = 0
        for i in range(3):
            for j in range(3):
                y = i + case[0] -1
                x = j + case[1] -1
                if x >= 0 and x < len(self.board) and y >= 0 and y < len(self.board[i]):
                    if self.board[y][x][0] != self.team:
                        enemisCount += 1
        return enemisCount

    def selectUnitsSources(self):
        caseList = []
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j][0] != self.team:
                    caseList.append((i,j))
                else:
                    if self.countEnemisAround((i, j)) == 0 or self.board[i][j][1] <= 1:
                        caseList.append((i,j))
        return(caseList)

    def selectTargetAround(self):
        caseList = []
        for i in range(3):
            for j in range(3):
                y = i + self.source[0] -1
                x = j + self.source[1] -1
                if x >= 0 and x < len(self.board) and y >= 0 and y < len(self.board[i]):
                    if self.board[y][x][0] != self.team:
                        caseList.append((y,x))
        return(caseList)

    def enableUnitsSources(self):
        self.changeAllButtonsState("normal")
        self.giveButtonsSelectSourceAction()
        choices = self.selectUnitsSources()
        for i in range(len(choices)):
            self.changeStateOfOneButton(choices[i], "disabled")        

    
    def enableTargetAround(self):
        choices = self.selectTargetAround()
        for i in range(len(choices)):
            self.changeStateOfOneButton(choices[i], "normal") 

    def enableUnitsTargets(self, case):
        self.changeAllButtonsState("disabled")
        self.giveButtonsSelectTargetAction()
        x = case//len(self.board)
        y = case - x*len(self.board)
        self.source = (x, y)
        self.enableTargetAround()

    def __init__(self):

        self.ROW_COUNT = 3
        self.COLUMN_COUNT = 3
        self.TABLE_SIZE = 3
        self.UNITS = 3
        self.source = (0, 0)
        self.target = (0, 0)
        self.teamCount = 0
        self.team = 0
        
        self.askPlayerCount("Donnez le nombre de joueurs", 2, 3)
        self.askForGridSize("Donnez la taille du plateau", self.teamCount+1, 6)
        
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
        self.board = list(zip(repartCase, repartPawn))
        Back.shuffle(self.board)
        print(Back.countPawn(self.board))
        self.board = list(Back.chunks(self.board, int(self.TABLE_SIZE)))
        #
        if self.teamCount == 3:
           self.board[-1][-1] = (3, self.board[-1][-1][1])
        #
        
        for i in range(len(self.board)):
            print(self.board[i])

        
        root = self.initFrame()
        self.buttons = self.createGrid(root)
        assert(len(self.buttons) == self.ROW_COUNT*self.COLUMN_COUNT)
        self.displayGrid()
        self.team = random.randint(1,self.teamCount)
        print("Team n°" + str(self.team) + " starts. " + str(self.teamCount) + " Players")
        self.refreshGrid()
        self.enableUnitsSources()
        root.mainloop()

GUI()
