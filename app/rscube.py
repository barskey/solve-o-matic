from kociemba import solve
from PIL import Image, ImageStat
import time
from app.lookups import *

class MyCube(object):

	def __init__(self):
		self._raw_colors = [[None for i in range(9)] for j in range(6)] # [r,g,b,a] for each raw color found on cube
		self._face_colors = [None for i in range(6)] # matched color of the center site on each face e.g. red, blue, etc.
		self._match_colors = [[None for i in range(9)] for j in self._face_colors] # matched color for each site e.g. red, blue, etc.
		self._cube_colors = [[None for i in range(9)] for j in self._face_colors] # letter for corresponding face_color for each site on cube
		self.solve_to = 'Solid Cube' # string representing cube solve to pattern
		self._solve_string = None # instructions to solve cube

		self._grip_state = {'A': None, 'B': None}
		self.orientation = 'UFD' # current orientation of the cube, Upface, gripper A Face, gripper B Face

	@property
	def orientation(self):
		return self._orientation

	@orientation.setter
	def orientation(self, val):
		self._orientation = val

	@property
	def solve_to(self):
		return self._solve_to

	@solve_to.setter
	def solve_to(self, pattern):
		self._solve_to = PATTERNS[pattern][1]

	def get_abs_site(self, site_r):
		"""
		Transposes site numbers given up_face rotation. Returns unrotated site number given rotated site.
		"""
		return ROT_TABLE[UP_FACE_ROT[self._orientation]][site_r - 1]

	def set_face_colors(self):
		"""
		Sets face color for all faces.
		Should be run after check_all_sites returns True
		"""
		for face, colors in enumerate(self._match_colors):
			self._face_colors[face] = colors[4]
		#print self._face_colors # debug

	def check_face_colors(self):
		"""
		Checks that each face has a color assigned and that they are unique
		"""
		if None in self._face_colors:
			return False
		elif len(self._face_colors) > len(set(self._face_colors)):
			return False
		else:
			return True

	def check_face_matched(self, f):
		"""
		Checks that each site on a face has a matched color
		"""
		face = str(f)
		if not face.isdigit():
			face = FACES[face]
		if None in self._match_colors[face]:
			return False
		else:
			return True

	def clear_matched(self):
		"""
		Clears all matched sites on all faces for a re-scan_face
		"""
		self._match_colors = [[None for i in range(9)] for j in self._face_colors]
		return

	def check_all_sites(self):
		"""
		Checks that there are exactly 9 of each match_color.
		"""
		colors = []
		for face in self._match_colors:
			for color in face:
				if color not in colors:
					colors.append(color)
		for color in colors:
			if sum(f.count(color) for f in self._match_colors) != 9:
				return False
		return True

	def get_solve_string(self):
		"""
		Gets the solve string
		"""
		return self._solve_string

	def set_solve_string(self):
		"""
		Sets the solve string from kociemba
		"""
		cube_def = self.get_cube_def()
		print (cube_def) # debug
		print (self._solve_to) # debug
		cube_def = 'FLRLURDBLUUBBRLFRDRLFBFDBURLFUDDFBDRDUBBLRLFDUDLFBUFRU' # debug because pics are not in the correct order - hence unsolvable
		self._solve_string = solve(cube_def, self._solve_to)
		#self._solve_string = "R' D2 R' U2 R F2 D B2 U' R F' U R2 D L2 D' B2 R2 B2 U' B2" # debug
		print (self._solve_string) # debug
		return self._solve_string

	def set_cube_colors(self):
		"""
		Sets each site to letter representing face color
		"""
		for f in range(6):
			for s in range(9):
				self._cube_colors[f][s] = FACES_STR[self._face_colors.index(self._match_colors[f][s])]
		#print self._cube_colors # debug

	def get_cube_def(self):
		"""
		Returns cube_def in the form UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
		"""
		return ''.join(str(site) for sitelist in self._cube_colors for site in sitelist)

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

	def get_up_raw_color(self, site_r):
		"""
		Returns the raw color for site site_r on upface. Transposes if necessary for rotated face
		"""
		sitenum = int(site_r)
		upface = FACES[self.get_up_face()]
		s = self.get_abs_site(sitenum)
		return self._raw_colors[upface][s - 1]

	def set_raw_color(self, face, site, rawcolor):
		"""
		Sets the raw color for site site on given face.
		"""
		self._raw_colors[FACES[face]][site] = rawcolor

	def set_up_match_color(self, site_r, color):
		"""
		Sets matched color on up_face for given (possibly) rotated site_r
		"""
		upface = FACES[self.get_up_face()]
		s = self.get_abs_site(site_r)
		self._match_colors[upface][s - 1] = color

	def set_orientation(self, gripper, dir):
		"""
		Updates cube orientation given a gripper and direction it twisted
		"""
		if gripper == 'A':
			self.orientation = NEW_ORIENTATION_TWISTA[self.orientation][dir]
		elif gripper == 'B':
			self.orientation = NEW_ORIENTATION_TWISTB[self.orientation][dir]

	def move_face_for_twist(self, face_to_move, to_gripper = None):
		"""
		Will position face_to_move to gripper A or B depending on fewest moves.
		Moves face to chosen gripper, and updates cube orientation.
		If gripper passed as arg face_to_move will be positioned to input gripper.
		Returns chosen gripper
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
		if len(moves) > 0:
			print ('Moving face %i to gripper %s') % (face, to_gripper)

		# perform the moves (if any)
		for move in moves:
			gripper_to_move = move[0]
			cmd = move[1]
			#if cmd == '+' or cmd == '-': # if it's a twist command
			#	self.twist(gripper_to_move, cmd)
			#else: # it must be a grip command
			#	self.grip(gripper_to_move, cmd)

		return to_gripper
