import random
import battle
import start as Back
from copy import *


def evaluate(board, team):
    nbCase = Back.countCaseTeam(board, team)
    nbPawn = Back.countPawnTeam(board, team)
    return nbPawn/nbCase

def testTarget(board, team, sources):
    for source in sources :
        targets = battle.selectTargetAround(board, team, source)
        if(len(targets)>0):
            return True
    return False

def play(board, team, sources):
    #Test si des targets existent pour chaque source
    if(testTarget(board, team, sources)):
        #bloc pour faire premiere attaque
        for source in sources :
            targets = battle.selectTargetAround(board, team, source)
            if(len(targets)>0):
                for target in targets : 
                    actualBoard = Back.oneAttack(deepcopy(board), source, target)
                    selectedSource = source
                    selectedTarget = target
                    break
                break
        #Determine la meilleur attaque
        for source in sources : 
            targets = battle.selectTargetAround(board, team, source)
            for target in targets : 
                newBoard = Back.oneAttack(deepcopy(board), source, target)    
                if evaluate(newBoard, team) > evaluate(actualBoard, team):
                    actualBoard = newBoard
                    selectedSource = source
                    selectedTarget = target
    else:
        selectedSource = sources[0]
        selectedTarget = selectedSource

    return([selectedSource, selectedTarget])
    
