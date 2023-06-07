#Currently not covering if a coef is 0 everywhere in a column, unexpected behaviour might occur
def solve(equations):
    numberOfRows, numberOfColumns = equations.shape
    numberOfColumns -= 1

    #Eliminate variables
    for r in range(min(numberOfRows, numberOfColumns)):
        if equations[r,r] == 1:
            for i in range(r + 1, numberOfRows):
                if equations[i, r] == 1:
                    equations[i] = (equations[i] - equations[r]) % 2
        else:
            newRowIndex = r
            for i in range(r + 1, numberOfRows):
                if equations[i, r] == 1:
                    newRowIndex = i
                    break
            #Forcing to not pass by reference with dummy operation
            temp = equations[r] + 0
            equations[r] = equations[newRowIndex]
            equations[newRowIndex] = temp
            for i in range(r + 1, numberOfRows):
                if equations[i, r] == 1:
                    equations[i] = (equations[i] - equations[r]) % 2
    #Back-substitution
    for i in reversed(range(numberOfColumns)):
        if(equations[i, i] == 1):
            j = i - 1
            while j >= 0:
                if equations[j, i] == 1:
                    equations[j] = (equations[j] - equations[i]) % 2
                j -= 1

    return list(equations[:, -1])