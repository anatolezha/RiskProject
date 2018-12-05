from tkinter import *
import start as Back
import IA
import battle
import random
import time

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

    def setIACount(self, root, scale):
        self.IA_count = scale.get()
        root.destroy()
        
    def setGridSize(self, root, scale):
        self.TABLE_SIZE = scale.get()
        root.destroy()
        
    def startGame(self, button):
        button.destroy()
        self.displayGrid()
        self.newTurn()

    def countGameStats(self, team):
        units = 0
        territory = 0
        for i in range(len(self.board)):
            for case in self.board[i]:
                if case[0] == team:
                    units += case[1]
                    territory += 1
        ratio = units/territory
        return([ratio, territory, units])

    def selectWinner(self):
        winner = [0, 0, 0, 0]#team, ratio, case, pions
        for i in range(self.teamCount):
            stats = self.countGameStats(i+1)
            if stats[1] > winner[2]:
                winner[0] = i+1
                winner[1] = stats[0]
                winner[2] = stats[1]
                winner[3] = stats[2]
        return(winner)

    def displayGameEnd(self):
        self.root.destroy()
        root = self.initFrame()
        Label(root, text="\n***\t\tPartie terminée !\t\t***\n").grid(padx=0, pady=1)
        Label(root, text="Durée : " + str(self.turnCount)).grid(padx=0, pady=2)
        winner = self.selectWinner()
        Label(root, text="Winner : " + str(winner[0]) + " -> " + str(winner[1]) + "\t(cases : " + str(winner[2]) + " | pions : " + str(winner[3]) + ")").grid(padx=0, pady=3)
        b = Button(root, text="Valider", command=lambda : root.destroy())
        b.grid(padx=0, pady=4)
        root.mainloop()
    
    def displayGameStart(self):
        b = Button(self.root, text="Commencer !")
        b.configure(command=lambda : self.startGame(b))
        b.grid(padx=0, pady=1)

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

    def askIACount(self, text, minVal, maxVal):
        root = self.initFrame()
        s = Scale(root, orient='horizontal', from_=minVal, to=maxVal,
                  resolution=1, tickinterval=1, sliderlength=20,
                  troughcolor="#BCF5A9", activebackground="green",
                  label=text, length=350)
        s.grid(padx=0, pady=1)
        b = Button(root, text="Valider", command=lambda : self.setIACount(root, s))
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

    def IATurn(self):
        sources = battle.selectUnitsSources(self.board, self.team)
        if self.isTurnPossible(len(sources),1):
            attackInformations = IA.play(self.board, self.team, sources)
            self.source = attackInformations[0]
            self.target = attackInformations[1]
            print("source : " + str(self.source) + "\target : " + str(self.target))
            self.root.update()
            time.sleep(self.timeToSleep*2)
            self.changeBgColorOfOneButton(self.source, "#FFFF00")
            self.root.update()
            time.sleep(self.timeToSleep)
            self.changeBgColorOfOneButton(self.target, "#FFFF00")
            self.root.update()
            time.sleep(self.timeToSleep)
            if self.source == self.target:
                self.isTurnPossible(0,2)
                if not self.isItFinish:
                    self.newTurn()
                else:
                    self.displayGameEnd()
            else:
                self.isTurnPossible(1,2)
                self.attack()
        else:
            if not self.isItFinish:
                self.newTurn()
            else:
                self.displayGameEnd()

    def newTurn(self):
        self.turnCount += 1
        if self.team == self.teamCount:
            self.team = 1
        else:
            self.team += 1
        print("Team n°" + str(self.team) + " play.") 
        self.refreshGrid()
        if self.team not in self.IA_teams:
            self.enableUnitsSources()
        else:
            self.giveButtonsNoneAction()
            self.IATurn()

    def attack(self):
        print("Attack : source (" + str(self.source) + ") target (" + str(self.target))
        self.board = Back.oneAttack(self.board, self.source, self.target)
        print(self.board)
        self.newTurn()
        

    def launchAttack(self, case):
        self.changeAllButtonsState("disabled")
        self.giveButtonsSelectSourceAction()
        x = case//len(self.board)
        y = case - x*len(self.board)
        self.target = (x, y)
        self.attack()

    def noneCommand(self):
        pass

    def giveButtonsNoneAction(self):
        for i in range(len(self.buttons)):
            self.buttons[i].configure(command=self.noneCommand)
            
    def giveButtonsSelectTargetAction(self):
        for i in range(len(self.buttons)):
            self.buttons[i].configure(command=lambda val=i: self.launchAttack(val))

    def changeAllButtonsState(self, state):
        for i in range(len(self.buttons)):
            self.buttons[i].configure(state=state)

    def changeStateOfOneButton(self, case, state):
        self.buttons[(case[0]*len(self.board[case[0]]))+case[1]].configure(state=state)

    def changeBgColorOfOneButton(self, case, bgColor):
        self.buttons[(case[0]*len(self.board[case[0]]))+case[1]].configure(background=bgColor, foreground="black")

    def isTurnPossible(self, possible, step):
        print(possible)
        if possible != 0:
            if step != 1:
                self.skipTurnCount = 0
            return True
        else:
            self.skipTurnCount += 1
            self.turnCount -= 1
            print("Pas de choix nb : " + str(self.skipTurnCount))
            if self.skipTurnCount == self.teamCount:
                self.isItFinish = True
                input()
                print("Partie Finie")
            return False

##    def countEnemisAround(self, board, team, case):
##        enemisCount = 0
##        for i in range(3):
##            for j in range(3):
##                y = i + case[0] -1
##                x = j + case[1] -1
##                if x >= 0 and x < len(board) and y >= 0 and y < len(board[i]):
##                    if board[y][x][0] != team:
##                        enemisCount += 1
##        return enemisCount
##
##    def selectUnitsSources(self, board, team):
##        caseList = []
##        for i in range(len(board)):
##            for j in range(len(board[i])):
##                if board[i][j][0] == team:
##                    if countEnemisAround(board, team, (i, j)) != 0 and board[i][j][1] > 1:
##                        caseList.append((i,j))
##        return(caseList)

##    def selectTargetAround(self, board, team, source):
##        caseList = []
##        for i in range(3):
##            for j in range(3):
##                y = i + source[0] -1
##                x = j + source[1] -1
##                if x >= 0 and x < len(board) and y >= 0 and y < len(board[i]):
##                    if board[y][x][0] != team and board[source[0]][source[1]][1] != board[y][x][1]+1:
##                        caseList.append((y,x))
##        return(caseList)

    def enableUnitsSources(self):
        self.changeAllButtonsState("disabled")
        self.giveButtonsSelectSourceAction()
        choices = battle.selectUnitsSources(self.board, self.team)
        if self.isTurnPossible(len(choices),1):
            for i in range(len(choices)):
                self.changeStateOfOneButton(choices[i], "normal")
        else:
            if not self.isItFinish:
                self.newTurn()
            else:
                self.displayGameEnd()

    
    def enableTargetAround(self):
        choices = battle.selectTargetAround(self.board, self.team, self.source)
        if self.isTurnPossible(len(choices),2):
            for i in range(len(choices)):
                self.changeStateOfOneButton(choices[i], "normal")
        else:
            if not self.isItFinish:
                self.newTurn()
            else:
                self.displayGameEnd()

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
        self.IA_count = 0
        self.team = 0
        self.skipTurnCount = 0
        self.isItFinish = False
        self.turnCount = 0
        self.IA_teams = []
        self.timeToSleep = 0.5
        
        self.askPlayerCount("Donnez le nombre de joueurs", 2, 3)
        self.askIACount("Parmis ces joueurs, donnez le nombre d'IA", 0, self.teamCount)
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
        for i in range(self.IA_count):
            self.IA_teams.append(self.teamCount-i)

        print(self.IA_teams)
            
        if self.teamCount == 3:
           self.board[-1][-1] = (3, self.UNITS)#(3, self.board[-1][-1][1])
        #
        
##        self.board = [[(2,1),(2,1),(2,1),(1,1),(1,1),(2,1)],
##                      [(1,1),(3,1),(3,1),(2,1),(1,1),(1,1)],
##                      [(3,1),(3,2),(3,1),(2,1),(2,1),(2,1)],
##                      [(3,1),(3,1),(3,1),(3,1),(2,1),(2,1)],
##                      [(1,1),(3,1),(1,1),(3,1),(2,1),(1,2)],
##                      [(1,1),(2,1),(3,1),(3,1),(3,1),(3,1)]]
        for i in range(len(self.board)):
            print(self.board[i])

        
        self.root = self.initFrame()
        self.buttons = self.createGrid(self.root)
        assert(len(self.buttons) == self.ROW_COUNT*self.COLUMN_COUNT)
        self.team = random.randint(1,self.teamCount)
        print(str(self.teamCount) + " Players")
        
        self.displayGameStart()
        self.root.mainloop()

GUI()
