from misio.lost_wumpus.util import load_world_from_stdin
from numpy import empty, zeros
from numpy import min as np_min
from numpy import sum as np_sum
from numpy import percentile as np_percentile
from numpy.random import choice
from operator import itemgetter

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
                self.world[row, col] = self.translate_world(field)

        self.max_steps = self.world_rows * self.world_columns * 2

        self.find_exit()
        self.init_probability_array()
        self.build_distance_array()
        self.build_moves_array()

    def reset(self):
        self.init_probability_array()
        self.current_step = 0

    def translate_world(self, element):
        return SYMBOLS[element]

    def find_exit(self):
        for i, lst in enumerate(self.world):
            for j, v in enumerate(lst):
                if v == Field.EXIT:
                    self.exit = (i, j)
                    break

    def init_probability_array(self):
        # Initialize world
        # For Exit probability = 0.0
        start_probability = 1 / ((self.world_rows * self.world_columns) - 1)
        self.probability_array = zeros(shape=(self.world_rows, self.world_columns))
        self.probability_array.fill(start_probability)

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
        expected_value = np_percentile(self.probability_array, 75)

        for row in range(self.world_rows):
            for col in range(self.world_columns):
                if self.probability_array[row, col] >= expected_value:
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

def run_agent(agent_class):
    n_worlds = int(input())
    n_runs = int(input())
    for world_i in range(n_worlds):
        m, p, pj, pn = load_world_from_stdin()
        agent = agent_class(m, p, pj, pn)
        for run_i in range(n_runs):
            agent.reset()
            while True:
                state = agent.translate_world(input())
                if state == Field.EXIT or agent.current_step >= agent.max_steps:
                    break
                agent.sense(state)
                move = agent.move()
                print(move)

run_agent(SlepyPanZajebistosc)
