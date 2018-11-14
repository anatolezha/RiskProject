import random
import battle

#team est un int du numéro du joueur
#sources est un tableau de tuples qui contiennent les coordonnées x et y de chaque case source possible
def play(board, team, sources):
    # sélectionne par défaut la première source (un tuple des coordonnées x et y)
    selectedSource = sources[0]

    #Code de séléction de la source (A Modifié)
    if len(sources) > 1:
        selectedSource = sources[random.randint(0,len(sources)-1)]

    #Sélectionne toutes les cibles (tableau de tuples qui contiennent les coordonnées x et y)
    #en fonction d'une source
    targets = battle.selectTargetAround(board, team, selectedSource)

    #Code de séléction de la source (A Modifié)
    if len(targets) > 1:
        selectedTarget = targets[random.randint(0,len(targets)-1)]

    #Sécurité à garder pour que le programme fonctionne
    elif len(targets) > 0:
        selectedTarget = targets[0]
    else:
        selectedTarget = selectedSource
    return([selectedSource, selectedTarget])
    
