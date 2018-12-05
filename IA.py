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
    if(testTarget(board, team, sources)):
        targets = battle.selectTargetAround(board, team, sources[0])
        for target in targets : 
            actualBoard = Back.oneAttack(deepcopy(board), sources[0], target)
            selectedSource = sources[0]
            selectedTarget = target
            break

        for source in sources : 
            targets = battle.selectTargetAround(board, team, source)
            for target in targets : 
                newBoard = Back.oneAttack(deepcopy(board), source, target)    
                if evaluate(newBoard, team) > evaluate(actualBoard, team):
                    actualBoard = newBoard
                    selectedSource = source
                    selectedTarget = target
    else:
        selectedTarget = source[0]
        selectedTarget = selectedSource

    return([selectedSource, selectedTarget])
    
