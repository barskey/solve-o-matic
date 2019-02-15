U = 0
R = 1
F = 2
D = 3
L = 4
B = 5

FACES = {
	'U': U,
	'R': R,
	'F': F,
	'D': D,
	'L': L,
	'B': B
}

FACES_STR = ['U', 'R', 'F', 'D', 'L', 'B']

# ----------------------------------------------------------------------
# Lookup table to store moves to put given face to gripper A or B.
# Relative to cube in default position ordered URFDLB
# e.g. MOVES_TO_A[D] would be the moves to get face currently in position D to gripper A
#
# String is comma separated moves, with the following commands:
# Note: using lower case o and c so it doesn't look like 0
# A : gripper A (front gripper)
# B : gripper B (back gripper)
# o : Open
# c : Close
# + : Clockwise turn
# - : Counter-clockwise turn
MOVES_TO_A = [
	'Bo,A-,Bc,Ao,B+,A+,Ac,Bo,B-,Bc',
	'Ao,B-,Ac,Bo,B+,Bc',
	'',
	'Bo,A+,Bc,Ao,B+,A-,Ac,Bo,B-,Bc',
	'Ao,B+,Ac,Bo,B-,Bc',
	'Ao,B+,B+,Ac'
]

MOVES_TO_B = [
	'Bo,A+,A+,Bc',
	'Bo,A+,Bc,Ao,A-,Ac',
	'Ao,B+,Ac,Bo,B-,A+,Bc,Ao,A-,Ac',
	'',
	'Bo,A-,Bc,Ao,A+,Ac',
	'Ao,B+,Ac,Bo,B-,A-,Bc,Ao,A+,Ac'
]

# Lookup table for new orientation after twisting gripper A or B with the cube in the given position
# e.g. NEW_ORIENTATION_TWISTA['UFD']['+'] gives 'LDR', which the cube will be in after twisting gripper A CW
NEW_ORIENTATION_TWISTA = {
	'UFD': {'+': 'LFR', '-': 'RFL'},
	'URD': {'+': 'FRB', '-': 'BRF'},
	'UBD': {'+': 'RBL', '-': 'LBR'},
	'ULD': {'+': 'BLF', '-': 'FLB'},
	'RDL': {'+': 'FDB', '-': 'BDF'},
	'RBL': {'+': 'DBU', '-': 'UBD'},
	'RUL': {'+': 'BUF', '-': 'FUB'},
	'RFL': {'+': 'UFD', '-': 'DFU'},
	'FDB': {'+': 'LDR', '-': 'RDL'},
	'FRB': {'+': 'DRU', '-': 'URD'},
	'FUB': {'+': 'RUL', '-': 'LUR'},
	'FLB': {'+': 'ULD', '-': 'DLU'},
	'DBU': {'+': 'LBR', '-': 'RBL'},
	'DRU': {'+': 'BRF', '-': 'FRB'},
	'DFU': {'+': 'RFL', '-': 'LFR'},
	'DLU': {'+': 'FLB', '-': 'BLF'},
	'LDR': {'+': 'BDF', '-': 'FDB'},
	'LFR': {'+': 'DFU', '-': 'UFD'},
	'LUR': {'+': 'FUB', '-': 'BUF'},
	'LBR': {'+': 'UBD', '-': 'DBU'},
	'BDF': {'+': 'RDL', '-': 'LDR'},
	'BLF': {'+': 'DLU', '-': 'ULD'},
	'BUF': {'+': 'LUR', '-': 'RUL'},
	'BRF': {'+': 'URD', '-': 'DRU'}
}

NEW_ORIENTATION_TWISTB = {
	'UFD': {'+': 'ULD', '-': 'URD'},
	'URD': {'+': 'UFD', '-': 'UBD'},
	'UBD': {'+': 'URD', '-': 'ULD'},
	'ULD': {'+': 'UBD', '-': 'UFD'},
	'RDL': {'+': 'RFL', '-': 'RBL'},
	'RBL': {'+': 'RDL', '-': 'RUL'},
	'RUL': {'+': 'RBL', '-': 'RFL'},
	'RFL': {'+': 'RUL', '-': 'RDL'},
	'FDB': {'+': 'FLB', '-': 'FRB'},
	'FRB': {'+': 'FDB', '-': 'FUB'},
	'FUB': {'+': 'FRB', '-': 'FLB'},
	'FLB': {'+': 'FUB', '-': 'FDB'},
	'DBU': {'+': 'DLU', '-': 'DRU'},
	'DRU': {'+': 'DBU', '-': 'DFU'},
	'DFU': {'+': 'DRU', '-': 'DLU'},
	'DLU': {'+': 'DFU', '-': 'DBU'},
	'LDR': {'+': 'LBR', '-': 'LFR'},
	'LFR': {'+': 'LDR', '-': 'LUR'},
	'LUR': {'+': 'LFR', '-': 'LBR'},
	'LBR': {'+': 'LUR', '-': 'LDR'},
	'BDF': {'+': 'BRF', '-': 'BLF'},
	'BLF': {'+': 'BDF', '-': 'BUF'},
	'BUF': {'+': 'BLF', '-': 'BRF'},
	'BRF': {'+': 'BUF', '-': 'BDF'}
}
# Translate table to get from current orientation to representation as if in default position
# Order of faces is URFDLB - e.g. for face_position['RUL'], R is in default U, F is in default R, U is in default F, etc.
# so face_position['RUL'][L] gives face B in the default L position
FACE_POSITION = {
	'UFD': [U, R, F, D, L, B],
	'URD': [U, B, R, D, F, L],
	'UBD': [U, L, B, D, R, F],
	'ULD': [U, F, L, D, B, R],
	'RDL': [R, B, D, L, F, U],
	'RBL': [R, U, B, L, D, F],
	'RUL': [R, F, U, L, B, D],
	'RFL': [R, D, F, L, U, B],
	'FDB': [F, R, D, B, L, U],
	'FRB': [F, U, R, B, D, L],
	'FUB': [F, L, U, B, R, D],
	'FLB': [F, D, L, B, U, R],
	'DBU': [D, R, B, U, L, F],
	'DRU': [D, F, R, U, B, L],
	'DFU': [D, L, F, U, R, B],
	'DLU': [D, B, L, U, F, R],
	'LDR': [L, F, D, R, B, U],
	'LFR': [L, U, F, R, D, B],
	'LUR': [L, B, U, R, F, D],
	'LBR': [L, D, B, R, U, F],
	'BDF': [B, L, D, F, R, U],
	'BLF': [B, U, L, F, D, R],
	'BUF': [B, R, U, F, L, D],
	'BRF': [B, D, R, F, U, L]
}

# Lookup table for current rotation of up face when cube is in designated orientation
# degrees up face is rotated (CW) wrt looking at up face
UP_FACE_ROT = {
	'UFD': 0,
	'URD': 90,
	'UBD': 180,
	'ULD': 270,
	'RDL': 0,
	'RBL': 90,
	'RUL': 180,
	'RFL': 270,
	'FDB': 0,
	'FRB': 90,
	'FUB': 180,
	'FLB': 270,
	'DBU': 0,
	'DRU': 90,
	'DFU': 180,
	'DLU': 270,
	'LDR': 0,
	'LFR': 90,
	'LUR': 180,
	'LBR': 270,
	'BDF': 0,
	'BLF': 90,
	'BUF': 180,
	'BRF': 270
}

# Lookup table to reorder list corresponding to given orientation
# need to subtract 1 from this number to get index
ROT_TABLE = {
	0: [1, 2, 3, 4, 5, 6, 7, 8, 9],
	90: [7, 4, 1, 8, 5, 2, 9, 6, 3],
	180: [9, 8, 7, 6, 5, 4, 3, 2, 1],
	270: [3, 6, 9, 2, 5, 8, 1, 4, 7]
}

testimages = [
	'testimg/uface.jpg',
	'testimg/rface.jpg',
	'testimg/fface.jpg',
	'testimg/dface.jpg',
	'testimg/lface.jpg',
	'testimg/bface.jpg'
]

PATTERNS = {
	'Solid Cube':           ['_solid.jpg',                   'UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'],
	'Checkerboard':         ['checkerboard.jpg',             'UFUFUFUFURURURURURFRFRFRFRFDBDBDBDBDLDLDLDLDLBLBLBLBLB'],
	'Easy Checkerboard':    ['easy-checkerboard.jpg',        'UDUDUDUDURLRLRLRLRFBFBFBFBFDUDUDUDUDLRLRLRLRLBFBFBFBFB'],
	'Wire':                 ['wire.jpg',                     'UUUUUUUUURLLRRRLLRBBFFFFFBBDDDDDDDDDLRRLLLRRLFFBBBBBFF'],
	'Tablecloth':           ['tablecloth.jpg',               'BFBRURBFBRURURURURURUBFBURUFBFLDLFBFLDLDLDLDLDLDFBFDLD'],
	'Spiral':               ['spiral.jpg',                   'FFFFUFFUURRUURUUUURRFRFFRRRBBBBDBDDBDDDDLDLLDLLLLBBLLB'],
	'Vertical Stripes':     ['vertical-stripes.jpg',         'UUUUUUUUUBRFBRFBRFLFRLFRLFRDDDDDDDDDFLBFLBFLBRBLRBLRBL'],
	'Opposite Corners':     ['opposite-corners.jpg',         'DDDDUDDDDLRRRRRRRLBFFFFFFFBUUUUDUUUURLLLLLLLRFBBBBBBBF'],
	'Cross':                ['cross.jpg',                    'DUDUUUDUDFRFRRRFRFRFRFFFRFRUDUDDDUDUBLBLLLBLBLBLBBBLBL'],
	'Cross 2':              ['cross2.jpg',                   'RURUUURURFRFRRRFRFUFUFFFUFULDLDDDLDLBLBLLLBLBDBDBBBDBD'],
	'Cube in cube':         ['cube-in-cube.jpg',             'FFFFUUFUURRURRUUUURFFRFFRRRBBBDDBDDBDDDLLDLLDLLLLBBLBB'],
	'Cube in cube in cube': ['cube-in-a-cube-in-a-cube.jpg', 'RRRRUURUFURFRRFFFFUFRUFFUUULLLDDLBDLBBBLLBDLBDDDDBBDBL'],
	'Anaconda':             ['anaconda.jpg',                 'FUFUUFFFFUUUURRURURRRFFRRFRBDBBDDBBBDLDDLLDDDLBLBBLLLL'],
	'Python':               ['python.jpg',                   'DUDDUDDUDFFFFRRFRFRFRFFRRRRUUUDDDUUUBBBBLLBLBLBLBBLLLL'],
	'Black Mamba':          ['black-mamba.jpg',              'RURUURRRRBBBRRRBBBDDDFFFDDDLLLDDLLDLFLFFLLFFFUBUUBUUBU'],
	'Green Mamba':          ['green-mamba.jpg',              'RRRUUURRRBBBRRRBBBDDDFFFDDDLLLDDLLDLFLFFLLFFFUUUBBUUBU'],
	'Four Spots':           ['four-spots.jpg',               'UUUUUUUUULLLLRLLLLBBBBFBBBBDDDDDDDDDRRRRLRRRRFFFFBFFFF'],
	'Six Spots':            ['six-spots.jpg',                'FFFFUFFFFUUUURUUUURRRRFRRRRBBBBDBBBBDDDDLDDDDLLLLBLLLL'],
	'Twister':              ['twister.jpg',                  'RURRUURUURRFRRFFRFUFFFFFUUULLLDDDDDLBBBLLLLLBDBDDBBDBB'],
	'Center Edge Corner':   ['center-edge-corner.jpg',       'RFRFUFRFRFUFURUFUFURURFRURULBLBDBLBLBDBDLDBDBDLDLBLDLD'],
	'Tetris':               ['tetris.jpg',                   'FFBFUBFBBUDDURDUUDRLLRFLRRLBBFBDFBFFUDDULDUUDLRRLBRLLR'],
	'Facing Checkerboards': ['facing-checkerboards.jpg',     'UUUUUUUUURLRLRLRLRFFFFFFFFFDDDDDDDDDLRLRLRLRLBBBBBBBBB']
}
