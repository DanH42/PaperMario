from pprint import pprint 
import copy

class paperMarioSolver:
    def __init__(self, starting, moves):
        self.initialBoardState = copy.deepcopy(starting)
        self.boardState = copy.deepcopy(starting)
        self.initialMoves = moves
        self.moves = moves


    def resetState(self):
        self.boardState = copy.deepcopy(self.initialBoardState)
        self.moves = copy.deepcopy(self.initialMoves)

    def ringMove(self, index, amount):
        # index 0-3, amount 1-11
        self.moves -= 1
        self.boardState[index] = self.boardState[index][amount:]+self.boardState[index][:amount]

    def lineMove(self, index, amount): 
        self.moves -= 1
        def reindex(x):
            return abs(3 - ((x-4)%7))
        # index 0-5, amount 1-7
        opposite = index+6
        tempCol = [x[index] for x in self.boardState] + list(reversed([x[opposite] for x in self.boardState]))
        tempCol = tempCol[amount:] + tempCol[:amount]
        for tempIndex,item in enumerate(tempCol):
            if (tempIndex < 4):
                self.boardState[reindex(tempIndex)][index] = item
            else:
                self.boardState[reindex(tempIndex)][opposite] = item

    def showState(self):
        self.showStateAsRows()
        self.showStateAsColumns()

    def showStateAsRows(self):
        print("RowView")
        arr = copy.deepcopy(self.boardState)
        for i in range(len(arr)):
            for j in range(len(arr[i])):
                arr[i][j] = str(arr[i][j])
                if len(arr[i][j])== 1:
                    arr[i][j] = " " + arr[i][j]
            print(" ".join(arr[i]))
        print()

    def showStateAsColumns(self):
        print("ColumnView")
        for i in range(6):
            tempCol = [x[i] for x in self.boardState] + list(reversed([x[i+6] for x in self.boardState]))
            for j in range(len(tempCol)):
                tempCol[j] = str(tempCol[j])
                if len(tempCol[j])== 1:
                    tempCol[j] = " " + tempCol[j]
            print(" ".join(tempCol))
        print()

    def checkSolution(self):
        arr = copy.deepcopy(self.boardState)

        for j in range(len(arr[0])):
            # i,j belongs to a column or a group of 4, residing in the 3rd and 4th rows only 
            # column check:
            tempCol = [x[j] for x in arr]
            if (tempCol.count(1) == 4):
                for k in range(len(arr)):
                    arr[k][j]  = 0
                    continue

        for j in range(len(arr[2])):
            if arr[2][j] != arr[3][j]:
                return False

        mergeArr = [0]*len(arr[3])
        for j in range(len(arr[3])):
            mergeArr[j] = int(arr[2][j] and arr[3][j])
        tempArr = copy.deepcopy(mergeArr)
        for j in range(len(tempArr)-1):
            if (tempArr[j] == 1 and tempArr[j+1] == 1):
                tempArr[j] = 0
                tempArr[j+1] = 0
        if tempArr.count(0) == 12:
            arr[2] = tempArr
            arr[3] = tempArr
        tempArr = copy.deepcopy(mergeArr)
        tempArr = tempArr[1:] + tempArr[:1]
        for j in range(len(tempArr)-1):
            if (tempArr[j] == 1 and tempArr[j+1] == 1):
                tempArr[j] = 0
                tempArr[j+1] = 0
        if tempArr.count(0) == 12:
            arr[2] = tempArr
            arr[3] = tempArr
        return sum([sum(x) for x in arr]) == 0

    def findSolution(self):
        # ring move -> index 0-3, amount 1-11
        # column move -> index 0-5, amount 1-7
        for moveIndex in range(86):
            if moveIndex < 4*11:
                index = moveIndex//11
                amount = moveIndex%11+1
                self.ringMove(index, amount)
                if self.checkSolution():
                    print("checkSolution evaluated to true for")
                    print("ring",index,amount)
                    print()
                    self.showState()
                    return True
                elif self.moves > 0:
                    nextMoveSolver = paperMarioSolver(self.boardState, self.moves)
                    if nextMoveSolver.findSolution():
                        print("checkSolution evaluated to true for")
                        print("ring", index, amount)
                        print("with a subsequent move\n")
                        self.showState()
                        return True
                    else:
                        self.resetState()
                else:
                    self.resetState()
            else:
                index = (moveIndex-4*11)//7
                amount = (moveIndex-4*11)%7+1
                self.lineMove(index, amount)
                if self.checkSolution():
                    print("checkSolution evaluated to true for")
                    print("line",index,amount)
                    print()
                    self.showState()
                    return True
                elif self.moves > 0:
                    nextMoveSolver = paperMarioSolver(self.boardState, self.moves)
                    if nextMoveSolver.findSolution():
                        print("checkSolution evaluated to true for")
                        print("line", index, amount)
                        print("with a subsequent move\n")
                        self.showState()
                        return True
                    else:
                        self.resetState()
                else:
                    self.resetState()
        return False
                    


board =[
[0, 1, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0],
[0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0],
[0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]


solver = paperMarioSolver(board, 3)
solver.findSolution()

for i in range(4*11+6*7):
    print(i)