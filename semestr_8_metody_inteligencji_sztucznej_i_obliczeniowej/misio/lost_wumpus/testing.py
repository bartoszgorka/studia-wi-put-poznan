import tqdm
from numpy import empty, zeros
from numpy import min as np_min
from numpy import sum as np_sum
from numpy import percentile as np_percentile
from numpy.random import choice
from operator import itemgetter
import numpy as np
import traceback

DEFAULT_TEST_RUNS = 100


def generate_deterministic_seeds(seed, shape):
	r = np.random.RandomState(seed=seed)
	seeds = r.randint(0, np.iinfo(np.uint32).max, shape)
	return seeds

class Field:
	EXIT = 2
	CAVE = 1
	EMPTY = 0

class Action:
	UP = 'UP'
	DOWN = 'DOWN'
	LEFT = 'LEFT'
	RIGHT = 'RIGHT'

SYMBOLS = {
	'.': Field.EMPTY,
	'0': Field.EMPTY,
	0: Field.EMPTY,
	'J': Field.CAVE,
	'1': Field.CAVE,
	1: Field.CAVE,
	'W': Field.EXIT,
	'2': Field.EXIT,
	2: Field.EXIT
}

OPPOSITES = {
	Action.UP: Action.DOWN,
	Action.DOWN: Action.UP,
	Action.RIGHT: Action.LEFT,
	Action.LEFT: Action.RIGHT
}

class SlepyPanZajebistosc():
	# Probability
	move_probability = None
	probability_trap = None
	probability_mistake = None

	# World shape
	world_rows = None
	world_columns = None
	world = None
	exit = None
	max_steps = None
	current_step = 0

	# Probability
	probability_array = None
	distances = None
	moves = None
	last_move_opposite = None

	def __init__(self, m, p, pj, pn):
		self.move_probability = p
		self.probability_trap = pj
		self.probability_mistake = pn
		self.world_rows = len(m)
		self.world_columns = len(m[0])
		self.world = empty(shape=(self.world_rows, self.world_columns))
		for row, values in enumerate(m):
			for col, field in enumerate(values):
				type = self.translate_world(field)
				self.world[row, col] = type
				if type == Field.EXIT:
					self.exit = (row, col)

		self.max_steps = self.world_rows * self.world_columns * 2

		self.init_probability_array()
		self.build_distance_array()
		self.build_moves_array()

	def reset(self):
		self.init_probability_array()
		self.current_step = 0

	def translate_world(self, element):
		return SYMBOLS[element]

	def init_probability_array(self):
		# Initialize world
		# For Exit probability = 0.0
		start_probability = 1 / ((self.world_rows * self.world_columns) - 1)
		self.probability_array = zeros(shape=(self.world_rows, self.world_columns))
		self.probability_array.fill(start_probability)
		self.probability_array[self.exit] = 0.0

	def update_probability_array(self, action):
		new_array = zeros(shape=self.probability_array.shape)
		not_directly_moved_prob = (1 - self.move_probability) / 4

		# Based on move - set shift
		if action == Action.UP:
			m_col = 0
			m_row = -1
		elif action == Action.DOWN:
			m_col = 0
			m_row = 1
		elif action == Action.LEFT:
			m_col = -1
			m_row = 0
		else:
			m_col = 1
			m_row = 0

		# Iterate and create new array
		for row in range(self.world_rows):
			for column in range(self.world_columns):
				# Calculate row and column - common part - values calculated only once
				r = row + self.world_rows + m_row
				c = column + self.world_columns + m_col

				# Calculate probability of correct and incorrect moves
				basic_probability = self.move_probability * self.probability_array[row, column]
				move_in_another_direction_prob = not_directly_moved_prob * self.probability_array[row, column]

				# Update array
				new_array[(r + 1) % self.world_rows, c % self.world_columns] += move_in_another_direction_prob
				new_array[(r - 1) % self.world_rows, c % self.world_columns] += move_in_another_direction_prob
				new_array[r % self.world_rows, (c + 1) % self.world_columns] += move_in_another_direction_prob
				new_array[r % self.world_rows, (c - 1) % self.world_columns] += move_in_another_direction_prob
				new_array[r % self.world_rows, c % self.world_columns] += basic_probability

		# Set new array as probability array
		self.probability_array = new_array

		# Normalize
		self.normalize()

	def normalize(self):
		# Probability in exit field always 0.0
		self.probability_array[self.exit] = 0.0

		# Sum rest of indexes and normalize sum == 1.0
		sum_of_probability = np_sum(self.probability_array)
		self.probability_array /= sum_of_probability

	def sense(self, val):
		observation = self.translate_world(val)

		# Apply changes
		if observation == Field.EMPTY:
			self.probability_array[self.world == Field.EMPTY] *= (1 - self.probability_mistake)
			self.probability_array[self.world == Field.CAVE] *= (1 - self.probability_trap)
		elif observation == Field.CAVE:
			self.probability_array[self.world == Field.EMPTY] *= self.probability_mistake
			self.probability_array[self.world == Field.CAVE] *= self.probability_trap

		# Normalize probability array
		self.normalize()

	def move(self):
		# We don't know where we are but we can guess
		moves = {Action.UP: 0.0, Action.LEFT: 0.0, Action.DOWN: 0.0, Action.RIGHT: 0.0}
		val = np_percentile(self.probability_array, 95)

		for row in range(self.world_rows):
			for col in range(self.world_columns):
				if self.probability_array[row, col] >= val:
					available_moves = [move for move in self.moves[row, col] if move != self.last_move_opposite]
					if len(available_moves) > 0:
						moves[choice(available_moves)] += self.probability_array[row, col]

		# Select move with greatest value
		action = max(moves.items(), key=itemgetter(1))[0]

		self.last_move_opposite = OPPOSITES[action]
		self.update_probability_array(action)
		self.current_step += 1

		return action

	def find_min_val(self, row, col):
		min_val = np_min([
			self.distances[(row + 1) % self.world_rows, col],
			self.distances[(row + self.world_rows - 1) % self.world_rows, col],
			self.distances[row, (col + 1) % self.world_columns],
			self.distances[row, (col + self.world_columns - 1) % self.world_columns]])

		min_val += 1
		if min_val < self.distances[row, col]:
			return min_val
		else:
			return self.distances[row, col]

	def build_distance_array(self):
		self.distances = empty(shape=self.probability_array.shape)
		self.distances.fill(self.world_rows * self.world_columns)

		# For exit set 0
		self.distances[self.exit] = 0

		# In row where we can found exit
		exit_row, exit_col = self.exit
		for col in range(self.world_columns):
			self.distances[exit_row, col] = self.find_min_val(exit_row, col)
		for row in range(self.world_rows):
			self.distances[row, exit_col] = self.find_min_val(row, exit_col)

		changed = True
		while changed:
			changed = False
			for row in range(self.world_rows):
				for col in range(self.world_columns):
					previous = self.distances[row, col]
					self.distances[row, col] = self.find_min_val(row, col)
					if previous != self.distances[row, col]:
						changed = True

	def build_moves_array(self):
		self.moves = empty(shape=self.probability_array.shape, dtype=object)
		for row in range(self.world_rows):
			for col in range(self.world_columns):
				available_moves = []
				value = self.distances[row, col]
				if self.distances[(row + self.world_rows - 1) % self.world_rows, col] < value:
					available_moves.append(Action.UP)
				if self.distances[(row + 1) % self.world_rows, col] < value:
					available_moves.append(Action.DOWN)
				if self.distances[row, (col + self.world_columns - 1) % self.world_columns] < value:
					available_moves.append(Action.LEFT)
				if self.distances[row, (col + 1) % self.world_columns] < value:
					available_moves.append(Action.RIGHT)
				self.moves[row, col] = available_moves
		self.moves[self.exit] = [Action.UP, Action.DOWN, Action.RIGHT, Action.LEFT]



class LostWumpusGame(object):
	def __init__(self, map: np.ndarray, p: float, pj: float, pn: float, exit_loc: tuple = None, max_moves=None):
		assert isinstance(map, np.ndarray)
		self.map = map
		self.h, self.w = map.shape
		self.p = p
		self.pj = pj
		self.pn = pn
		if exit_loc is None:
			exit_loc = [int(x) for x in np.where(map == Field.EXIT)]
		self.exit_loc = list(exit_loc)
		self.position = list(exit_loc)
		self.moves = np.inf
		self.finished = True
		self.sensory_output = None
		if max_moves is None:
			max_moves = np.inf
		self.max_moves = max_moves

	def reset(self):
		self.moves = 0
		self.finished = False
		self.position = self.exit_loc
		while self.position == self.exit_loc:
			self.position = [np.random.randint(self.h), np.random.randint(self.w)]
		self._update_sensory_output()

	def apply_move(self, action):
		assert not self.finished
		motion = [0, 0]
		if action == 'LEFT':
			motion[1] -= 1
		elif action == 'RIGHT':
			motion[1] += 1
		elif action == 'UP':
			motion[0] -= 1
		elif action == 'DOWN':
			motion[0] += 1
		else:
			print(action)

		if np.random.random() > self.p:
			motion[np.random.randint(2)] += np.random.choice([-1, 1])
		self.position[0] += motion[0]
		self.position[1] += motion[1]
		self.position[0] %= self.h
		self.position[1] %= self.w

		self.moves += 1
		self._update_sensory_output()

		if self.position == self.exit_loc or self.moves >= self.max_moves:
			if self.moves >= self.max_moves:
				print('TOO MANY STEPS')
			self.finished = True
			self.sensory_output = None

	def _update_sensory_output(self):
		if self.map[self.position[0], self.position[1]] == Field.CAVE:
			self.sensory_output = np.random.binomial(1, self.pj)
		else:
			self.sensory_output = np.random.binomial(1, self.pn)

def generate_map(h: int, w: int, cave_density: float):
	assert cave_density > 0
	assert cave_density < 1
	map = np.zeros((h, w), dtype=np.uint8) + Field.EMPTY

	num_caves = int(h * w * cave_density)
	cave_x = np.random.choice(w, size=num_caves, replace=False)
	cave_y = np.random.choice(h, size=num_caves, replace=False)
	map[cave_y, cave_x] = Field.CAVE

	exit_x = np.random.randint(w)
	exit_y = np.random.randint(h)
	map[exit_y, exit_x] = Field.EXIT
	return map, (exit_y, exit_x)


def load_input_file(filename: str, new_format: bool = False):
	with open(filename, "r") as file:
		num_worlds = int(file.readline())
		worlds = []
		if new_format:
			mapping = {x: int(x) for x in range(2)}
		else:
			mapping = {"J": Field.CAVE, "W": Field.EXIT, ".": Field.EMPTY}
		for i in range(num_worlds):
			p = float(file.readline())
			pj, pn = [float(x) for x in file.readline().split()]
			h, w = [int(x) for x in file.readline().split()]

			world = np.zeros((h, w), dtype=np.uint8)
			for i in enumerate(range(h)):
				line = file.readline()
				world[i, :] = [mapping[x] for x in line.strip()]
			worlds.append((world, p, pj, pn))

	return worlds


def load_world_from_stdin(new_format: bool = False):
	import sys
	p = float(input())
	pj, pn = [float(x) for x in input().split()]
	h, w = [int(x) for x in input().split()]
	if new_format:
		mapping = {x: int(x) for x in range(2)}
	else:
		mapping = {"J": Field.CAVE, "W": Field.EXIT, ".": Field.EMPTY}

	world = np.zeros((h, w), dtype=np.uint8)
	for i in range(h):
		line = input()
		world[i, :] = [mapping[x] for x in line.strip()]

	return world, p, pj, pn


def save_world(
		filename: str, map: np.ndarray,
		p: float,
		pj: float, pn: float,
		new_format: bool = False):
	with open(filename, "w") as file:
		print(p, file=file)
		print(pj, pn, file=file)
		print(*map.shape, file=file)
		if new_format:
			mapping = {x: str(x) for x in range(2)}
		else:
			mapping = {Field.CAVE: "J", Field.EXIT: "W", Field.EMPTY: "."}
		for row in map:
			print("".join([mapping[x] for x in row]), file=file)


def default_steps_constraint(world):
	return world.shape[0] * world.shape[1] * 2


######
WORLD = {
	'.': Field.EMPTY,
	'0': Field.EMPTY,
	0: Field.EMPTY,
	'J': Field.CAVE,
	'1': Field.CAVE,
	1: Field.CAVE,
	'W': Field.EXIT,
	'2': Field.EXIT,
	2: Field.EXIT
}

class AgentKasia:
	def __init__(self, areaMap, p, pj, pn):
		self.areaMap = areaMap
		self.p=p
		self.pj=pj
		self.pn=pn
		self.areaY=len(areaMap)
		self.areaX=len(areaMap[0])
		self.direction="NONE"
		self.exitY = 0
		self.exitX = 0
		self.histogram = []
		self.lastMoveOpposite = "None"
		self.current_step = 0
		self.max_steps = self.areaY * self.areaY * 2


		#self.histogram = np.zeros_like(self.areaMap,  dtype=float)
		value = 1 / ((self.areaX*self.areaY) - 1)
		for y in range(0, self.areaY):
			self.histogram.append([])
			for x in range(0, self.areaX):
				self.histogram[y].append(value);
				if(self.areaMap[y][x]==2):
					self.exitY = y
					self.exitX = x


		self.distanceArray = np.zeros_like(self.areaMap)
		self.distanceArray.fill(self.exitY*self.exitX*10)
		self.moves =[]

		#calculate distance array
		for y in range(0, self.areaY):
			self.moves.append([])
			for x in range(0, self.areaY):
				self.moves[y].append([])
				shortestLEFT = (self.areaX - self.exitX + x) % self.areaX
				shortestRIGHT = (self.areaX + self.exitX - x) % self.areaX
				shortestUP = (self.areaY - self.exitY + y) % self.areaY
				shortestDOWN = (self.areaY + self.exitY - y) % self.areaY
				self.distanceArray[y][x] = min([shortestUP + shortestLEFT, shortestUP + shortestRIGHT, shortestDOWN + shortestLEFT, shortestDOWN + shortestRIGHT])

		self.histogram[self.exitY][self.exitX]=0.0


		#calculate best moves for every field
		for y in range(0, self.areaY):
			for x in range(0, self.areaX):
				bestMoves = []
				left = self.distanceArray[y][(x-1+self.areaX)%self.areaX]
				right = self.distanceArray[y][(x+1+self.areaX)%self.areaX]
				up = self.distanceArray[(y-1+self.areaY)%self.areaY][x]
				down = self.distanceArray[(y+1+self.areaY)%self.areaY][x]
				minn = min([left, right, up, down])
				if(left == minn):
					bestMoves.append(Action.LEFT)
				if(right == minn):
					bestMoves.append(Action.RIGHT)
				if(up == minn):
					bestMoves.append(Action.UP)
				if(down == minn):
					bestMoves.append(Action.DOWN)
				self.moves[y][x] = bestMoves

		return


	# TODO COPY IT!
	def sense(self, sensor1):
		sensor = self.translate_world(sensor1)

		self.histogram[self.exitY][self.exitX] = 0.0

		for y in range(self.areaY):
			for x in range(self.areaX):
				if(sensor==Field.CAVE and self.areaMap[y][x]==Field.CAVE):
					self.histogram[y][x] *= self.pj
				elif(sensor==Field.CAVE and self.areaMap[y][x]==Field.EMPTY):
					self.histogram[y][x] *= self.pn
				elif(sensor==Field.EMPTY and self.areaMap[y][x]==Field.CAVE):
					self.histogram[y][x] *= (1-self.pj)
				elif(sensor==Field.EMPTY and self.areaMap[y][x]==Field.EMPTY):
					self.histogram[y][x] *= (1-self.pn)


		#normalize
		sumTmp = 0.0
		for y in range(self.areaY):
			for x in range(self.areaX):
				sumTmp += self.histogram[y][x]

		if(sumTmp!=0.0):
			for y in range (self.areaY):
				for x in range(self.areaX):
					self.histogram[y][x] /= sumTmp


	def move(self):
		dictt = {Action.UP: 0.0, Action.DOWN:0.0, Action.LEFT: 0.0, Action.RIGHT:0.0}
		self.current_step+=1

		#finding direction
		for y in range(self.exitY):
			for x in range(self.exitX):
				possibleMoves = []
				for move in self.moves[y][x]:
					if(move != self.lastMoveOpposite):
						possibleMoves.append(move)
				if len(possibleMoves) > 0:
					dictt[choice(possibleMoves)] += self.histogram[y][x]

		self.direction = max(dictt.items(), key=itemgetter(1))[0]

		#setting self.lastMoveOpposite
		if(self.direction == Action.LEFT):
			self.lastMoveOpposite = Action.RIGHT
		elif(self.direction == Action.RIGHT):
			self.lastMoveOpposite = Action.LEFT
		elif(self.direction == Action.UP):
			self.lastMoveOpposite = Action.DOWN
		elif(self.direction == Action.DOWN):
			self.lastMoveOpposite = Action.UP

		newHistogram = np.zeros_like(self.areaMap,  dtype=float)
		for y in range(self.areaY):
			for x in range(self.areaX):
				centre = self.p * self.histogram[y][x]
				neighboors = ((1 - self.p) / 4) * self.histogram[y][x]

				if(self.direction == Action.LEFT):
					newHistogram[y][(x + 1) % self.areaX] += centre
					newHistogram[y][x] += neighboors
					newHistogram[y][(x + 2) % self.areaX] += neighboors
					newHistogram[(y - 1 + self.areaY) % self.areaY][(x + 1) % self.areaX] += neighboors
					newHistogram[(y + 1) % self.areaY][(x + 1) % self.areaX] += neighboors

				elif(self.direction==Action.RIGHT):
					newHistogram[y][(x - 1 + self.areaX) % self.areaX] += centre
					newHistogram[y][x] += neighboors
					newHistogram[(y - 1 + self.areaY) % self.areaY][(x - 1 + self.areaX) % self.areaX] += neighboors
					newHistogram[(y + 1) % self.areaY][(x - 1 + self.areaX) % self.areaX] += neighboors
					newHistogram[y][(x - 2 + self.areaX) % self.areaX] += neighboors

				elif(self.direction==Action.UP):
					newHistogram[(y - 1 + self.areaY) % self.areaY][x]  +=  centre
					newHistogram[y][x]  +=  neighboors
					newHistogram[(y + 2) % self.areaY][x]   +=  neighboors
					newHistogram[(y + 1) % self.areaY][(x - 1 + self.areaX) % self.areaX]   +=  neighboors
					newHistogram[(y + 1) % self.areaY][(x + 1) % self.areaX]  +=  neighboors

				elif(self.direction==Action.DOWN):
					newHistogram[(y - 1 + self.areaY) % self.areaY][x] += centre
					newHistogram[y][x] += neighboors
					newHistogram[(y - 1 + self.areaY) % self.areaY][(x - 1) % self.areaX] += neighboors
					newHistogram[(y - 2 + self.areaY) % self.areaY][x] += neighboors
					newHistogram[(y - 1 + self.areaY) % self.areaY][(x + 1) % self.areaX] += neighboors

		#normalize
		sumTmp = 0.0
		newHistogram[self.exitY][self.exitX] = 0.0
		for y in range(self.areaY):
			for x in range(self.areaX):
				sumTmp += newHistogram[y][x]

		self.histogram = newHistogram

		if sumTmp != 0.0:
			for y in range (self.areaY):
				for x in range(self.areaX):
					self.histogram[y][x] /= sumTmp

		return self.direction


	def histogram(self):
		return self.histogram

	def translate_world(self, element):
		return WORLD[element]

	def reset(self):
		pass


from numpy import ndarray, float64, zeros, ones_like, random, argwhere
from scipy.signal import convolve2d
from random import shuffle
class HistogramAgent:
    def __init__(self, map: ndarray, p: float, pj: float, pn: float):

        self.oppositeAction = {Action.LEFT: Action.RIGHT,
                               Action.RIGHT: Action.LEFT,
                               Action.UP: Action.DOWN,
                               Action.DOWN: Action.UP,
                               None: None}
        self.moveMap = {0: Action.UP, 1: Action.DOWN, 2: Action.LEFT, 3: Action.RIGHT}

        self.correctMoveProb = p
        self.badMoveProb = (1 - p) / 4

        self.mUp = zeros((5, 5))
        self.mUp[1, 2] = self.correctMoveProb
        self.mUp[0, 2] = self.badMoveProb
        self.mUp[1, 1] = self.badMoveProb
        self.mUp[2, 2] = self.badMoveProb
        self.mUp[1, 3] = self.badMoveProb
        self.mDown = zeros((5, 5))
        self.mDown[3, 2] = self.correctMoveProb
        self.mDown[3, 1] = self.badMoveProb
        self.mDown[2, 2] = self.badMoveProb
        self.mDown[4, 2] = self.badMoveProb
        self.mDown[3, 3] = self.badMoveProb
        self.mLeft = zeros((5, 5))
        self.mLeft[2, 1] = self.correctMoveProb
        self.mLeft[1, 1] = self.badMoveProb
        self.mLeft[2, 0] = self.badMoveProb
        self.mLeft[3, 1] = self.badMoveProb
        self.mLeft[2, 2] = self.badMoveProb
        self.mRight = zeros((5, 5))
        self.mRight[2, 3] = self.correctMoveProb
        self.mRight[1, 3] = self.badMoveProb
        self.mRight[2, 2] = self.badMoveProb
        self.mRight[3, 3] = self.badMoveProb
        self.mRight[2, 4] = self.badMoveProb
        # print()
        # print(self.mUp)
        # print(self.mDown)
        # print(self.mLeft)
        # print(self.mRight)

        self.correctSensorProb = pj
        self.badSensorProb = 1 - pj

        self.badWumpusDec = pn
        self.correctWumpusDec = 1 - pn

        self.h, self.w = map.shape
        self.map = map.astype(float64)

        # print(self.histogram)
        # print(self.map)
        # print(self.correctMoveProb, self.correctSensorProb, self.pn, self.w, self.h)
        self.holes = []
        self.normals = []
        self.end = None
        for x in range(self.w):
            for y in range(self.h):
                if self.map[x, y] == 1.0:
                    self.holes.append([x, y])
                elif self.map[x, y] == 2.0:
                    self.end = [x, y]
                else:
                    self.normals.append([x, y])
        self.distanceMatrix = zeros(map.shape)
        self.shape = map.shape
        self.createDistanceMatrix(self.distanceMatrix, self.end)
        self.moveMatrix = self.createPossibleMoveMatrix(self.distanceMatrix)
        # print(self.holes)
        # print(self.end)
        self.maxMove = self.w * self.h * 2
        self.histogram = None
        self.moved = 0
        self.lastMove = None
        self.prepare()

    def prepare(self):
        self.histogram = ones_like(self.map) / (self.h * self.w - 1)
        self.histogram[self.end[0], self.end[1]] = 0
        self.moved = 0
        self.lastMove = None

    def sense(self, sensory_input: bool):
        if sensory_input:
            forNormalFields = self.badWumpusDec
            forHoles = self.correctSensorProb
        else:
            forNormalFields = self.correctWumpusDec
            forHoles = self.badSensorProb

        for normal in self.normals:
            self.histogram[normal[0], normal[1]] *= forNormalFields
        for hole in self.holes:
            self.histogram[hole[0], hole[1]] *= forHoles

        self.normalize(self.histogram)

    def move(self):
        actions = {Action.LEFT: 0, Action.RIGHT: 0, Action.UP: 0, Action.DOWN: 0}

        lastOpposite = self.oppositeAction[self.lastMove]
        for y in range(self.h):
            for x in range(self.w):
                # print("Last", self.lastMove)
                # print(self.moveMatrix[x][y])
                # if x != self.end[0] and y != self.end[1]:
                posMove = self.moveMatrix[x][y] if lastOpposite is None \
                    else [move for move in self.moveMatrix[x][y] if move != lastOpposite]
                if len(posMove) > 0:
                    for m in posMove:
                        actions[m] += (self.histogram[x, y] / self.distanceMatrix[x, y])
                # for m in posMove:
                #     actions[m] += self.histogram[x, y]
                # print("Posmove", posMove)
        action = None
        maxVal = 0
        for key, value in actions.items():
            if value > maxVal:
                action = key
                maxVal = value

        self.lastMove = action
        self.moved += 1
        if self.moved < self.maxMove:
            # tmpHistogram = zeros(self.shape)

            # for y in range(self.h):
            #     for x in range(self.w):
            #         bad = self.histogram[x, y] * self.badMoveProb
            #         good = self.histogram[x, y] * self.correctMoveProb
            #         if action == Action.UP:
            #             tmpHistogram[x, y] += bad
            #             tmpHistogram[(x - 1 + self.w) % self.w, y] += good
            #             tmpHistogram[(x - 2 + self.w) % self.w, y] += bad
            #             tmpHistogram[(x - 1 + self.w) % self.w, (y - 1 + self.h) % self.h] += bad
            #             tmpHistogram[(x - 1 + self.w) % self.w, (y + 1 + self.h) % self.h] += bad
            #         elif action == Action.DOWN:
            #             tmpHistogram[x, y] += bad
            #             tmpHistogram[(x + 1 + self.w) % self.w, y] += good
            #             tmpHistogram[(x + 2 + self.w) % self.w, y] += bad
            #             tmpHistogram[(x + 1 + self.w) % self.w, (y - 1 + self.h) % self.h] += bad
            #             tmpHistogram[(x + 1 + self.w) % self.w, (y + 1 + self.h) % self.h] += bad
            #         elif action == Action.LEFT:
            #             tmpHistogram[x, y] += bad
            #             tmpHistogram[x, (y - 1 + self.h) % self.h] += good
            #             tmpHistogram[x, (y - 2 + self.h) % self.h] += bad
            #             tmpHistogram[(x - 1 + self.w) % self.w, (y - 1 + self.h) % self.h] += bad
            #             tmpHistogram[(x + 1 + self.w) % self.w, (y - 1 + self.h) % self.h] += bad
            #         elif action == Action.RIGHT:
            #             tmpHistogram[x, y] += bad
            #             tmpHistogram[x, (y + 1 + self.h) % self.h] += good
            #             tmpHistogram[x, (y + 2 + self.h) % self.h] += bad
            #             tmpHistogram[(x - 1 + self.w) % self.w, (y + 1 + self.h) % self.h] += bad
            #             tmpHistogram[(x + 1 + self.w) % self.w, (y + 1 + self.h) % self.h] += bad
            #
            # self.histogram = tmpHistogram
            # self.normalize(self.histogram)

            mask = None
            if action == Action.DOWN:
                mask = self.mDown
            elif action == Action.UP:
                mask = self.mUp
            elif action == Action.LEFT:
                mask = self.mLeft
            elif action == Action.RIGHT:
                mask = self.mRight

            self.histogram = convolve2d(self.histogram, mask, mode='same', boundary='wrap')
            self.normalize(self.histogram)
        else:
            self.prepare()
        # print(action)
        # print(self.histogram)
        return action

    def normalize(self, hist):
        hist[self.end[0], self.end[1]] = 0
        sumProb = sum(hist)
        hist /= sumProb

    def createDistanceMatrix(self, matrix, end):
        for x in range(self.w):
            for y in range(self.h):
                inLeft = x - end[0] if end[0] < x else (x + 1) + (self.w - 1 - end[0])
                inRight = (self.w - 1 - x) + (end[0] + 1) if end[0] < x else end[0] - x
                lessX = inRight if inLeft > inRight else inLeft

                inUp = y - end[1] if end[1] < y else (y + 1) + (self.h - 1 - end[1])
                inDown = (self.h - 1 - y) + (end[1] + 1) if end[1] < y else end[1] - y
                lessY = inDown if inUp > inDown else inUp
                # print(x, y, lessX, lessY)
                matrix[x, y] = lessX + lessY
        # print(matrix)
        # print(self.end)

    def createPossibleMoveMatrix(self, distanceMatrix):
        moveMatrix = []
        for x in range(self.w):
            row = []
            for y in range(self.h):
                minNeighbourhood = 1000000
                neighbourhood = [[(x - 1 + self.w) % self.w, y], [(x + 1 + self.w) % self.w, y],
                                 [x, (y - 1 + self.h) % self.h], [x, (y + 1 + self.h) % self.h]]#up, down, left, right
                for n in neighbourhood:
                    if minNeighbourhood > distanceMatrix[n[0], n[1]]:
                        minNeighbourhood = distanceMatrix[n[0], n[1]]
                moveList = []
                for i, n in enumerate(neighbourhood):
                    if minNeighbourhood == distanceMatrix[n[0], n[1]]:
                        moveList.append(self.moveMap[i])
                row.append(moveList)
                # print(x,y, moveList)
            moveMatrix.append(row)
        moveMatrix[self.end[0]][self.end[1]] = []
        # print()
        # print()
        # print()
        # print(moveMatrix[0][2])
        # print(moveMatrix[self.end[0]][self.end[1]])
        # print(moveMatrix[6])
        # print(self.distanceMatrix)
        # print(self.map)
        return moveMatrix

    def reset(self):
        pass

    def get_histogram(self):
        return self.histogram

def test_locally(filename, n: int = 100, seed: int = None, verbose: bool = False):
	mean_scores = []
	stds = []

	if seed is not None:
		np.random.seed(seed)

	worlds = load_input_file(filename)
	run_seeds = generate_deterministic_seeds(seed, [len(worlds), n])
	actions = [Action.RIGHT, Action.LEFT, Action.UP, Action.DOWN]

	for world_i, (m, p, pj, pn) in enumerate(worlds):
		max_moves = default_steps_constraint(m)
		game = LostWumpusGame(m, p, pj, pn, max_moves=max_moves)
		agent = HistogramAgent(m, p, pj, pn)

		run_scores = []
		for run_i in tqdm.trange(n, leave=False, desc="map{}/{}".format(world_i, len(worlds))):
			np.random.seed(run_seeds[world_i, run_i])
			agent.reset()
			game.reset()
			while not game.finished:
				move = None
				try:
					agent.sense(game.sensory_output)
					move = agent.move()
				except:
					print("Stop Wumpus. You're drunk. ABORTING.")
					traceback.print_exc()
					exit(-1)
				try:
					if move not in actions:
						exit(-2)
					game.apply_move(move)
				except:
					print("Environment failed. Please report it. ABORTING.")
					traceback.print_exc()
					exit(-3)
			run_scores.append(game.moves)
		mean_score = np.mean(run_scores)
		std = np.std(run_scores)
		mean_scores.append(mean_score)
		stds.append(std)
		if verbose:
			print("map{}: avg score: {:0.2f} ±{:0.2f}".format(world_i, mean_score, std))

	mean_total_score = np.sum(mean_scores)
	print(np.min(mean_scores))
	print(np.max(mean_scores))
	total_std = (np.array(stds) ** 2).sum() ** 0.5
	if verbose:
		print()
	print("Total score: {:0.2f} ± {:0.2f}".format(mean_total_score, total_std))

test_locally("/Users/bgorka/Downloads/Studia/Semestr_8/misio_labs/lab3/tests/2015.in", n=10)
