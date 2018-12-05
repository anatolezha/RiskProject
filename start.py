from random import *
from math import *
from pprint import *

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def distribute(items, cells):
     """ Distribute items over a given number of cells
         Cells must be greater or equals to items !
     """

     distribution = []

     if items < cells:
         raise 'Cells must be greater or equals to items !'

     while cells > 0:
         count = 1 + int(randint(0, items - cells) / 3)
         cells -= 1
         items -= count
         distribution.append(count)

     if items > 0:
         distribution[-1] += items

     shuffle(distribution)
     return distribution

def oneAttack(board, coordCaseAttack, coordCaseDefend):
    caseAttack = board[coordCaseAttack[0]][coordCaseAttack[1]]
    caseDefend = board[coordCaseDefend[0]][coordCaseDefend[1]]
    pawnAttack = caseAttack[1]
    pawnDefend = caseDefend[1]
    defend = [caseDefend[0],caseDefend[1]]
    if pawnAttack > pawnDefend:
        defend[0] = caseAttack[0]#abs(caseDefend[0]-1)
        pawnDefend = pawnAttack-1-pawnDefend
        pawnAttack = 1
    elif pawnDefend > pawnAttack:
        pawnDefend -= (pawnAttack-1)
        pawnAttack = 1
    elif pawnAttack == pawnDefend:
        pawnAttack = 1
        pawnDefend = 1
    defend[1] = pawnDefend
    board[coordCaseAttack[0]][coordCaseAttack[1]] = (caseAttack[0],pawnAttack)
    board[coordCaseDefend[0]][coordCaseDefend[1]] = (defend[0],defend[1])
    return board

def countCase(board):
    caseA = 0
    caseB = 0
    for i in board:
        if i == 1:
            caseA += 1
        elif i == 2:
            caseB += 1
    return (caseA, caseB)

def countPawn(board):
    pawnA = 0
    pawnB = 0
    for i in board:
        if i[0] == 1:
            pawnA += i[1]
        elif i[0] == 2:
            pawnB += i[1]
    return (pawnA, pawnB)

def countCaseTeam(board, team):
    case = 0
    for i in board:
        if i == team:
            case+= 1
    return case

def countPawnTeam(board, team):
    pawn = 0
    for i in board:
        if i[0] == team:
            pawn += i[1]
    return pawn

def createBoard(size):
    square = size * size
    if size % 2 != 0 :
        if randint(1,10)%2 == 0 :
            B = [(1)] * int(square/2 +1)
            B += [(2)] * int(square/2)
        else : 
            B = [(1)] * int(square/2)
            B += [(2)] * int(square/2 +1)
    else :
        B = [(1)] * int(square/2)
        B += [(2)] * int(square/2)
    return list(B)

if __name__ == "__main__":
    size = int(input("Veuillez enregistrer une taille\n"))
    nbPawn = int(input("Nombre de pion par joueur, doit être supérieur au nombre de case ("+str(size*size)+")\n"))
    repartCase = createBoard(size)
    casePerPlayer = countCase(repartCase)
    repartPawn = distribute(nbPawn, casePerPlayer[0]) + distribute(nbPawn, casePerPlayer[1])
    board = list(zip(repartCase, repartPawn))
    shuffle(board)
    print(countPawn(board))
    board = list(chunks(board, int(size)))
    for i in range(len(board)):
        print(board[i])


