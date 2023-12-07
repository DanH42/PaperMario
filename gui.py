from solver import paperMarioSolver
import math
import pygame


class TestColorScheme:
	color_array = ['#f7f7f7', '#ff0000', '#00ff00', '#0000ff', '#ffff00', '#00ffff', '#ff00ff', '#000000', '#808080']
	TEXT_FG = pygame.Color(color_array[0])
	TEXT_BG = pygame.Color(color_array[1])
	GRASS   = pygame.Color(color_array[2])
	SOLVE   = pygame.Color(color_array[3])
	RING_A  = pygame.Color(color_array[4])
	RING_B  = pygame.Color(color_array[5])
	SELECT  = pygame.Color(color_array[6])
	OVERLAY = pygame.Color(color_array[7])
	INVALID = pygame.Color(color_array[8])


class DefaultColorScheme:
	TEXT_FG = pygame.Color("#000000")
	TEXT_BG = pygame.Color("#ffffff")
	GRASS   = pygame.Color("#33dd11")
	SOLVE   = pygame.Color("#ffaa66")
	RING_A  = pygame.Color("#ffee66")
	RING_B  = pygame.Color("#ffffcc")
	SELECT  = pygame.Color("#99eeff")
	OVERLAY = pygame.Color("#888888")
	INVALID = pygame.Color("#cc2200")


class GUI:
	def __init__(self, board=None, window_size=800, font_size=36, colors=DefaultColorScheme):
		pygame.init()
		pygame.display.set_allow_screensaver(True)
		pygame.display.set_caption("Pay per Mario? In this economy?")

		self.board = board if board is not None else [
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
			[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		]
		self.window_size = window_size
		self.num_sections = 12
		self.move_limit = 2

		self.screen = pygame.display.set_mode((self.window_size, self.window_size))
		self.clock = pygame.time.Clock()
		self.empty_board = None

		self.center_pos = pygame.Vector2(self.window_size / 2, self.window_size / 2)
		self.font_size = font_size
		self.font = pygame.font.Font(None, font_size)

		self.colors = colors


	def run(self):
		while True:
			mouse_pos = pygame.mouse.get_pos()

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					return

				if event.type == pygame.MOUSEBUTTONDOWN:
					clicked = self.get_slice(mouse_pos)
					# Solve button clicked
					if clicked == "center":
						if event.button == 1:
							# Don't run if board is unsolvable
							enemies = self.count_enemies()
							if enemies == 0 or enemies % 4 != 0:
								continue

							# Show an overlay while the solver is running
							overlay = pygame.Surface((self.window_size, self.window_size))
							overlay.set_alpha(192)
							overlay.fill(self.colors.OVERLAY)
							self.screen.blit(overlay, (0,0))
							pygame.display.flip()

							print("Solving...")
							solver = paperMarioSolver(self.board, self.move_limit)
							found = solver.findSolution()
							if found:
								print("Done!")
							else:
								print("No solution found")
					# Ring slice clicked
					elif clicked is not None:
						# Left click
						if event.button == 1:
							self.board[clicked[0]][clicked[1]] += 1
						# Right click
						elif event.button == 3:
							self.board[clicked[0]][clicked[1]] = 0
					# Move count +/- clicked
					elif mouse_pos[0] > self.window_size * .96 and mouse_pos[1] < self.window_size * .075:
						if event.button == 1:
							if mouse_pos[1] < self.window_size * .0375:
								if self.move_limit < 9:
									self.move_limit += 1
							else:
								if self.move_limit > 1:
									self.move_limit -= 1

			self.render(mouse_pos)

			self.clock.tick(60)


	def init_board(self):
		self.screen.fill(self.colors.GRASS)

		# Draw a checkerboard pattern for the rings
		for i in range(1, 5):
			radius = int(self.window_size * (0.5 - (0.075 * i)))
			angle_increment = 2 * math.pi / self.num_sections

			for j in range(self.num_sections):
				start_angle = j * angle_increment
				end_angle = (j + 1) * angle_increment

				# Alternate colors
				color = self.colors.RING_A if (i + j) % 2 == 0 else self.colors.RING_B

				# Draw multiple arcs with different offsets to fill in gaps
				for x in range(2):
					for y in range(2):
						pygame.draw.arc(
							self.screen, color, (
								self.center_pos[0] - radius + x,
								self.center_pos[1] - radius + y,
								radius * 2, radius * 2
							), start_angle, end_angle,
						   int(self.window_size * 0.075) + 1
						)

		# Draw the move counter
		text_surface = self.font.render("Moves:", True, self.colors.TEXT_FG)
		text_rect = text_surface.get_rect(center=((self.window_size * .9) - (self.font_size * 1.6), self.window_size * .0375))
		self.screen.blit(text_surface, text_rect)

		pygame.draw.rect(self.screen, self.colors.TEXT_BG, (self.window_size * .9, 0, self.window_size * .1, self.window_size * .075), 0)
		pygame.draw.rect(self.screen, self.colors.TEXT_FG, (self.window_size * .9, 0, self.window_size * .1, self.window_size * .075), 1)

		pygame.draw.rect(self.screen, self.colors.TEXT_FG, (self.window_size * .96, 0, self.window_size * .04, self.window_size * .0375), 1)
		text_surface = self.font.render("+", True, self.colors.TEXT_FG)
		text_rect = text_surface.get_rect(center=(self.window_size * .98, self.window_size * .01875))
		self.screen.blit(text_surface, text_rect)

		pygame.draw.rect(self.screen, self.colors.TEXT_FG, (self.window_size * .96, self.window_size * .0375, self.window_size * .04, self.window_size * .0375), 1)
		text_surface = self.font.render("-", True, self.colors.TEXT_FG)
		text_rect = text_surface.get_rect(center=(self.window_size * .98, self.window_size * (.0375 + .01875)))
		self.screen.blit(text_surface, text_rect)

		# Draw help text
		text_surface = self.font.render("Left click: place/change enemy        Right click: clear", True, self.colors.TEXT_FG)
		text_rect = text_surface.get_rect(center=(self.window_size / 2, self.window_size * .97))
		self.screen.blit(text_surface, text_rect)

		# Store a copy of the current screen for later use
		self.empty_board = self.screen.copy()


	def render(self, mouse_pos):
		# Render complex geometry once, then re-use it as a static background later
		if self.empty_board is None:
			self.init_board()
		else:
			self.screen.blit(self.empty_board, (0, 0))

		hovered_slice = self.get_slice(mouse_pos)
		labels = []

		# Draw a checkerboard pattern for the rings
		for i in range(1, 5):
			radius = int(self.window_size * (0.5 - (0.075 * i)))
			middle_radius = int(self.window_size * (0.5 - (0.075 * (i + 0.5))))
			angle_increment = 2 * math.pi / self.num_sections

			for j in range(self.num_sections):
				start_angle = j * angle_increment
				end_angle = (j + 1) * angle_increment
				column = (12 - j) + 2
				column = column - 12 if column >= 12 else column
				slice_center = (self.center_pos[0] + middle_radius * math.cos((start_angle + end_angle) / 2),
								self.center_pos[1] - middle_radius * math.sin((start_angle + end_angle) / 2))

				# Highlight the slice the mouse is hovering over
				if hovered_slice is not None and hovered_slice != "center":
					if hovered_slice[0] == i - 1 and hovered_slice[1] == column:
						pygame.draw.circle(self.screen, self.colors.SELECT, slice_center, self.window_size * 0.03)

				# Display the value from the board array in the center of each slice
				value = self.board[i - 1][column]
				if value > 0:
					text_surface = self.font.render(str(value), True, self.colors.TEXT_FG)
					text_rect = text_surface.get_rect(center=slice_center)
					labels.append((text_surface, text_rect))

		# Add labels last so they don't get covered by slice backgrounds
		for label in labels:
			self.screen.blit(label[0], label[1])

		# Draw the center circle
		color = self.colors.SELECT if hovered_slice == "center" else self.colors.SOLVE
		enemies = self.count_enemies()
		color = color if enemies > 0 and enemies % 4 == 0 else self.colors.INVALID
		pygame.draw.circle(self.screen, color, self.center_pos, int(self.window_size * (0.5 - (0.075 * 5))))

		# Render a button label if there's a multiple of 4 enemies
		if enemies > 0 and enemies % 4 == 0:
			text_surface = self.font.render("Solve", True, self.colors.TEXT_FG)
			text_rect = text_surface.get_rect(center=self.center_pos)
			self.screen.blit(text_surface, text_rect)

		# Render hover effects for buttons
		if hovered_slice is None and mouse_pos[0] > self.window_size * .96 and mouse_pos[1] < self.window_size * .075:
			if mouse_pos[1] < self.window_size * .0375:
				pygame.draw.rect(self.screen, self.colors.SELECT,  ((self.window_size * .96) + 1, 1, (self.window_size * .04) - 2, (self.window_size * .0375) - 2), 0)
				text_surface = self.font.render("+", True, self.colors.TEXT_FG)
				text_rect = text_surface.get_rect(center=(self.window_size * .98, self.window_size * .01875))
				self.screen.blit(text_surface, text_rect)
			else:
				pygame.draw.rect(self.screen, self.colors.SELECT,  ((self.window_size * .96) + 1, (self.window_size * .0375) + 1, (self.window_size * .04) - 2, (self.window_size * .0375) - 2), 0)
				text_surface = self.font.render("-", True, self.colors.TEXT_FG)
				text_rect = text_surface.get_rect(center=(self.window_size * .98, self.window_size * (.0375 + .01875)))
				self.screen.blit(text_surface, text_rect)

		# Display move limit
		text_surface = self.font.render(str(self.move_limit), True, self.colors.TEXT_FG)
		text_rect = text_surface.get_rect(center=(self.window_size * .93, self.window_size * .0375))
		self.screen.blit(text_surface, text_rect)

		# Render to the screen
		pygame.display.flip()


	def get_slice(self, mouse_pos):
		# Calculate polar coordinates relative to the center of the board
		relative_x = mouse_pos[0] - self.center_pos[0]
		relative_y = mouse_pos[1] - self.center_pos[1]
		angle = math.atan2(relative_y, relative_x)
		distance = math.hypot(relative_x, relative_y) / (self.window_size * (1 - (0.075 * 2)))

		# Check if the center circle was clicked
		if distance <= 0.5 - (0.0875 * 4):
			return "center"

		# Determine the ring and slice based on the polar coordinates
		for i in range(4):
			if 0.5 - (0.0875 * (i + 1)) <= distance < 0.5 - (0.0875 * i):
				slice_index = (int((angle + math.pi) / (2 * math.pi / self.num_sections)) % self.num_sections) - 3
				slice_index = 12 + slice_index if slice_index < 0 else slice_index
				return i, slice_index

		return None


	def count_enemies(self):
		count = 0
		for i in range(len(self.board)):
			for j in range(len(self.board[i])):
				if self.board[i][j] > 0:
					count += 1
		return count