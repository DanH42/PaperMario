from ..src.solver import paperMarioSolver
from copy import deepcopy
import random
import timeit

def generate_random_matrix(rows, columns, num_ones_per_row):
	# Initialize a matrix with zeros
	matrix = [[0] * columns for _ in range(rows)]

	# Set random positions to 1 in each row
	for row in matrix:
		ones_positions = random.sample(range(columns), num_ones_per_row)
		for pos in ones_positions:
			row[pos] = 1

	return matrix

def testSearchPerformance():
	performanceDFS = []
	performanceBFS = []

	randomBoards = []
	for i in range(1000):
		# Generate test boards. The way we generate this guarantees a valid solution in 3.
		testBoard = generate_random_matrix(4,12,1)
		randomBoards.append(deepcopy(testBoard))

	# test findSolutionBFS and findSolutionDFS here
	for randomBoard in randomBoards:
		solver = paperMarioSolver(randomBoard, 3)

		# Time findSolutionBFS
		bfs_time = timeit.timeit(lambda: solver.findSolutionBFS(), number=1)
		performanceBFS.append(bfs_time)

		# Time findSolutionDFS
		dfs_time = timeit.timeit(lambda: solver.findSolutionDFS(), number=1)
		performanceDFS.append(dfs_time)

	# Calculate and print average times
	avg_bfs_time = sum(performanceBFS) / len(performanceBFS)
	avg_dfs_time = sum(performanceDFS) / len(performanceDFS)

	print(f"Avg. time for BFS: {avg_bfs_time} seconds")
	print(f"Avg. time for DFS: {avg_dfs_time} seconds")
