def countEnemisAround(board, team, case):
    enemisCount = 0
    for i in range(3):
        for j in range(3):
            y = i + case[0] -1
            x = j + case[1] -1
            if x >= 0 and x < len(board) and y >= 0 and y < len(board[i]):
                if board[y][x][0] != team:
                    enemisCount += 1
    return enemisCount

def selectUnitsSources(board, team):
    caseList = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j][0] == team:
                if countEnemisAround(board, team, (i, j)) != 0 and board[i][j][1] > 1:
                    caseList.append((i,j))
    return(caseList)

def selectTargetAround(board, team, source):
    caseList = []
    for i in range(3):
        for j in range(3):
            y = i + source[0] -1
            x = j + source[1] -1
            if x >= 0 and x < len(board) and y >= 0 and y < len(board[i]):
                if board[y][x][0] != team and board[source[0]][source[1]][1] != board[y][x][1]+1:
                    caseList.append((y,x))
    return(caseList)
