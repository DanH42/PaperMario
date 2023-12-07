from copy import deepcopy

class move:
	def __init__(self, index, amount, moveType=0):
		# type 0 = ring, type 1 = line
		self.index = index
		self.amount = amount
		self.type = moveType

	def __str__(self):
		ringDict = {0: "outermost", 1:"second outer", 2: "second inner", 3: "innermost"}
		if self.type==0:
			direction = ("counterclockwise" if self.amount <=6 else "clockwise")
			amount = (self.amount if self.amount <= 6 else (12-self.amount))
			return ("Rotate " + ringDict[self.index] + " ring " + direction +" by " + str(amount))
		else:
			direction = ("outward" if self.amount <= 4 else "inward")
			amount = (self.amount if self.amount <= 4 else (8 - self.amount))
			return ("Shift the " + str(self.index+1) + " o'clock line " + direction + " by " + str(amount))

	def getAllRingMoves():
		ringMoves = []
		for index in range(4):
			for amount in range(1,12):
				tempMove = move(index, amount, moveType=0)
				ringMoves.append(tempMove)
		return ringMoves

	def getAllLineMoves():
		lineMoves = []
		for index in range(6):
			for amount in range(1,8):
				tempMove = move(index, amount, moveType=1)
				lineMoves.append(tempMove)
		return lineMoves

	def getAllMoves():
		return move.getAllRingMoves() + move.getAllLineMoves()


class paperMarioBoard:
	def __init__(self, initialBoard):
		if isinstance(initialBoard, list):
			self.boardState = deepcopy(initialBoard)	
			self.initialBoardState = deepcopy(initialBoard)
		elif isinstance(initialBoard, paperMarioBoard):
			self.boardState = deepcopy(initialBoard.boardState)
			self.initialBoardState = deepcopy(initialBoard.boardState)		

	def resetState(self):
		self.boardState = deepcopy(self.initialBoardState)

	def makeMove(self, moveToMake):
		if moveToMake.type == 0:
			self.ringMove(moveToMake.index, moveToMake.amount)
		else:
			self.lineMove(moveToMake.index, moveToMake.amount)

	def ringMove(self, index, amount):
		# index 0-3, out to in, amount 1-11, counterclockwise
		self.boardState[index] = self.boardState[index][amount:]+self.boardState[index][:amount]

	def lineMove(self, index, amount):
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
		arr = deepcopy(self.boardState)
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

	def isSolution(self):
		arr = deepcopy(self.boardState)

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
		tempArr = deepcopy(mergeArr)
		for j in range(len(tempArr)-1):
			if (tempArr[j] == 1 and tempArr[j+1] == 1):
				tempArr[j] = 0
				tempArr[j+1] = 0
		if tempArr.count(0) == 12:
			arr[2] = tempArr
			arr[3] = tempArr
		tempArr = deepcopy(mergeArr)
		tempArr = tempArr[1:] + tempArr[:1]
		for j in range(len(tempArr)-1):
			if (tempArr[j] == 1 and tempArr[j+1] == 1):
				tempArr[j] = 0
				tempArr[j+1] = 0
		if tempArr.count(0) == 12:
			arr[2] = tempArr
			arr[3] = tempArr
		return sum([sum(x) for x in arr]) == 0


# class bossBoard:
	# TODO: add boss board logic. Tile types:
	# - Can't pass (infinite penalty)
	# - Prefer not to pass, penalty
	# - Arrows (preserve direction)
	# - On switch + Magic circles (on can be marked as preferred and magic as end or can't pass,
	# 		depending on the preferred move of a round)
	# - Prefer to pass (bonus, e.g. hearts or coins or chests)
	# - Determined end states (large bonus, must be the last tile)
	# - positioning of end state (this may be tricky)
