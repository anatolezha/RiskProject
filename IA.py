import random
import battle

def play(board, team, sources):
    selectedSource = sources[0]
    if len(sources) > 1:
        selectedSource = sources[random.randint(0,len(sources)-1)]
    targets = battle.selectTargetAround(board, team, selectedSource)
    if len(targets) > 1:
        selectedTarget = targets[random.randint(0,len(targets)-1)]
    elif len(targets) > 0:
        selectedTarget = targets[0]
    else:
        selectedTarget = selectedSource
    return([selectedSource, selectedTarget])
    
