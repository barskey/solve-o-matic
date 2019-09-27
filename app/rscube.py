from kociemba import solve
import time
from app.lookups import *

class MyCube(object):

	def __init__(self):
		self.reset_cube()

	@property
	def orientation(self):
		return self._orientation

	@orientation.setter
	def orientation(self, val):
		self._orientation = val

	def reset_cube(self):
		self._cube_colors = [[None for i in range(9)] for j in range(6)] # letter for corresponding face_color for each site on cube
		self._face_color = {} # dict for looking up face assigned to hex color on each face (center site). key:#ffffff val:0
		self.solve_to = 'Solid Cube' # string representing cube solve to pattern
		self._solve_string = None # instructions to solve cube
		self.orientation = 'UFD' # current orientation of the cube, Upface, gripper A Face, gripper B Face

	def get_solve_string(self):
		"""
		Gets the solve string
		"""
		return self._solve_string if self._solve_string is not None else 0

	def set_solve_string(self):
		"""
		Sets the solve string from kociemba
		"""
		cube_def = self.get_cube_def()
		print (cube_def) # debug
		print (self.solve_to) # debug
		cube_def = 'FLRLURDBLUUBBRLFRDRLFBFDBURLFUDDFBDRDUBBLRLFDUDLFBUFRU' # debug because pics are not in the correct order - hence unsolvable
		solve_pattern = PATTERNS[self.solve_to][1]
		#self._solve_string = solve(cube_def, solve_pattern)
		self._solve_string = "R' D2 R' U2 R F2 D B2 U' R F' U R2 D L2 D' B2 R2 B2 U' B2" # debug
		#print (self._solve_string) # debug
		return self.get_solve_string()
	
	def update_solve_to(self, solveto):
		"""
		Updates the solve_to pattern. Returns the number of moves to the new pattern, 0 if not possible.
		"""
		self.solve_to = solveto
		moves = self.set_solve_string()
		return len(moves.split())

	def get_cube_def(self):
		"""
		Returns cube_def in the form UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
		"""
		cube_def = ''
		for face in self._cube_colors:
			for site in face:
				cube_def = cube_def + FACES_STR[self._face_color[site]]
		return cube_def

	def get_up_face(self):
		"""
		Returns string representing current up face
		"""
		return FACES_STR[FACE_POSITION[self._orientation][U]]

	def get_up_rot(self):
		"""
		Returns current rotation of up_face
		"""
		return UP_FACE_ROT[self._orientation]

	def set_orientation(self, gripper, dir):
		"""
		Updates cube orientation given a gripper and direction it twisted
		"""
		if gripper == 'A':
			self.orientation = NEW_ORIENTATION_TWISTA[self.orientation][dir]
		elif gripper == 'B':
			self.orientation = NEW_ORIENTATION_TWISTB[self.orientation][dir]
	
	def set_face_colors(self, colors):
		"""
		Takes list of colors with respect to camera (0 in UL, 8 in LR),
		rotates as necessary and saves in self cube colors.
		Returns face colors in un-rotated list.
		"""
		site_r = 0
		upface = FACES[self._orientation[0]]
		for i in ROT_TABLE[self.get_up_rot()]:
			self._cube_colors[upface][i] = colors[site_r]
			site_r += 1
		self._face_color[colors[4]] = upface # set face color with center site
		return self._cube_colors[upface]

	def get_moves_for_twist(self, face_to_move, to_gripper = None):
		"""
		Returns list of moves to position face_to_move to gripper A or B
		depending on fewest moves.
		If gripper passed as arg face_to_move will be positioned to input gripper.
		"""
		moves = None
		o = self._orientation
		print (o)

		# get current position of face to move
		face = FACE_POSITION[o].index(FACES[face_to_move])

		# get the moves to both gripper A and B so they can be compared
		moves_a = MOVES_TO_A[face].split(',')
		if moves_a[0] == '':
			moves_a = []
		moves_b = MOVES_TO_B[face].split(',')
		if moves_b[0] == '':
			moves_b = []

		# if a gripper was passed in as argument, move to that gripper
		if to_gripper == 'A':
			moves = moves_a
		elif to_gripper == 'B':
			moves = moves_b
		else: # else pick the least number of moves
			if len(moves_a) <= len(moves_b):
				moves = moves_a # moves to gripper A
				to_gripper = 'A'
			else:
				moves = moves_b # moves to gripper B
				to_gripper = 'B'

		return moves
