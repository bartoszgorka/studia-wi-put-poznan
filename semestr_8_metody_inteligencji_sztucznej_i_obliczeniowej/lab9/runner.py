from misio.optilio.pacman import StdIOPacmanRunner
from misio.pacman.game import *
from misio.pacman.util import CustomCounter, lookup, manhattan_distance
from misio.pacman.learningAgents import ReinforcementAgent
import random, math
import numpy as np
from operator import itemgetter


def closestFood(pos, food, capsules, walls):
    """
    closestFood -- this is similar to the function that we have
    worked on in the search project; here its all in one place
    """
    fringe = [(pos[0], pos[1], 0)]
    expanded = set()
    while fringe:
        pos_x, pos_y, dist = fringe.pop(0)
        if (pos_x, pos_y) in expanded:
            continue
        expanded.add((pos_x, pos_y))
        # if we find a food at this location then exit
        if food[pos_x][pos_y] or (pos_x, pos_y) in capsules:
            return dist
        # otherwise spread out from the location to its neighbours
        nbrs = Actions.getLegalNeighbors((pos_x, pos_y), walls)
        for nbr_x, nbr_y in nbrs:
            fringe.append((nbr_x, nbr_y, dist + 1))
    # no food found
    return None


class SimpleExtractor2():
    """
    Returns simple features for a basic reflex Pacman:
    - whether food will be eaten
    - how far away the next food is
    - whether a ghost collision is imminent
    - whether a ghost is one step away
    """

    def getFeatures(self, state, action):
        # extract the grid of food and wall locations and get the ghost locations
        food = state.getFood()
        capsules = state.getCapsules()
        walls = state.getWalls()
        ghosts = state.getGhostStates()
        map_size = walls.width * walls.height

        features = CustomCounter()

        features["bias"] = 1.0

        # compute the location of pacman after he takes the action
        x, y = state.getPacmanPosition()
        dx, dy = Actions.directionToVector(action)
        next_x, next_y = int(x + dx), int(y + dy)

        # count the number of ghosts 1-step away
        features["#-of-ghosts-1-step-away"] = sum(
            (next_x, next_y) in Actions.getLegalNeighbors(g.getPosition(), walls) and g.scaredTimer < 2 for g in ghosts)

        # if there is no danger of ghosts then add the food feature
        if not features["#-of-ghosts-1-step-away"] and (food[next_x][next_y] or (next_x, next_y) in capsules):
            features["eats-food"] = 1.0

        dist = closestFood((next_x, next_y), food, capsules, walls)
        if dist is not None:
            features["closest-food"] = float(dist) / map_size

        features.divideAll(10.0)
        return features


class QLearningAgent(ReinforcementAgent):
    """
      Q-Learning Agent

      Functions you should fill in:
        - computeValueFromQValues
        - computeActionFromQValues
        - getQValue
        - getAction
        - update

      Instance variables you have access to
        - self.epsilon (exploration prob)
        - self.alpha (learning rate)
        - self.discount (discount rate)

      Functions you should use
        - self.getLegalActions(state)
          which returns legal actions for a state
    """
    def __init__(self, **args):
        "You can initialize Q-values here..."
        ReinforcementAgent.__init__(self, **args)
        self.q_values = CustomCounter()

    def getQValue(self, state, action):
        """
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
        """
        if (state, action) in self.q_values:
            return self.q_values[(state, action)]
        else:
            self.q_values[(state, action)] = 0.0
            return 0.0

    def computeValueFromQValues(self, state):
        """
          Returns max_action Q(state,action)
          where the max is over legal actions.  Note that if
          there are no legal actions, which is the case at the
          terminal state, you should return a value of 0.0.
        """
        # Get list of actions in current state
        legal_actions = self.getLegalActions(state)
        if len(legal_actions) > 0:
            # Dict with action: value
            actions_list = CustomCounter()

            # Loop over possible actions
            for action in legal_actions:
                actions_list[action] = self.getQValue(state, action)

            # Select best action
            return max(actions_list.items(), key=itemgetter(1))[1]
        else:
            return 0.0

    def computeActionFromQValues(self, state):
        """
          Compute the best action to take in a state.  Note that if there
          are no legal actions, which is the case at the terminal state,
          you should return None.
        """
        # Get list of actions in current state
        legal_actions = self.getLegalActions(state)
        if len(legal_actions) > 0:
            # Dict with action: value
            actions_list = CustomCounter()

            # Loop over possible actions
            for action in legal_actions:
                actions_list[action] = self.getQValue(state, action)

            # Select best action
            return max(actions_list.items(), key=itemgetter(1))[0]
        else:
            return None

    def getAction(self, state):
        """
          Compute the action to take in the current state.  With
          probability self.epsilon, we should take a random action and
          take the best policy action otherwise.  Note that if there are
          no legal actions, which is the case at the terminal state, you
          should choose None as the action.

          HINT: To pick randomly from a list, use random.choice(list)
        """
        return max([(action, self.getQValue(state, action)) for action in self.getLegalActions(state)], key=lambda k: k[1])[0]
        # Get list of possibled action in current state
        legal_actions = self.getLegalActions(state)

        if np.random.rand() > self.epsilon:
            # Dict with action: value
            actions_list = CustomCounter()

            # Loop over possible actions
            for action in legal_actions:
                actions_list[action] = self.getQValue(state, action)

            # Select best action
            return max(actions_list.items(), key=itemgetter(1))[0]
        else:
            return np.random.choice(legal_actions)

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        raise NotImplementedError()

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class PacmanQAgent(QLearningAgent):
    "Exactly the same as QLearningAgent, but with different default parameters"

    def __init__(self, epsilon=0.0, gamma=0.8, alpha=0.2, numTraining=0, **args):
        """
        These default parameters can be changed from the pacman.py command line.
        For example, to change the exploration rate, try:
            python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

        alpha    - learning rate
        epsilon  - exploration rate
        gamma    - discount factor
        numTraining - number of training episodes, i.e. no learning after these many episodes
        """
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.index = 0
        QLearningAgent.__init__(self, **args)

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action


class ApproximateQAgent(PacmanQAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.
    """
    def __init__(self, **args):
        self.simpleExtractor = SimpleExtractor2()
        PacmanQAgent.__init__(self, **args)
        self.featureVector = CustomCounter()
        self.weights = []
        for i in range(0, 11):
            self.weights.append(CustomCounter())
        # capsuleClassic.lay
        self.weights[0]['bias'] = 2965.8273862563638
        self.weights[0]['#-of-ghosts-1-step-away'] = -13144.00462307635
        self.weights[0]['closest-food'] = -13.532189169359691
        self.weights[0]['eats-food'] = 1760.1826379221086

        # contestClassic.lay
        self.weights[1]['bias'] = 11835.299555444328
        self.weights[1]['#-of-ghosts-1-step-away'] = -14415.276999987025
        self.weights[1]['closest-food'] = -3.2642073911054923
        self.weights[1]['eats-food'] = 3746.837725582929

        # mediumClassic.lay
        self.weights[2]['bias'] = 11446.691928879674
        self.weights[2]['#-of-ghosts-1-step-away'] = -11362.12660081642
        self.weights[2]['closest-food'] = -37.31267241835425
        self.weights[2]['eats-food'] = 6203.8448314200095

        # mediumGrid.lay
        self.weights[3]['bias'] = 7586.292003514671
        self.weights[3]['#-of-ghosts-1-step-away'] = -1283.829372124739
        self.weights[3]['closest-food'] = -0.6931457680468394
        self.weights[3]['eats-food'] = 858.4194562414963

        # minimax
        self.weights[4]['bias'] = -12820.66382724905
        self.weights[4]['#-of-ghosts-1-step-away'] = -12431.42492890723
        self.weights[4]['closest-food'] = -936.0154539824068
        self.weights[4]['eats-food'] = 10.233155190839577

        # openClassic.lay
        self.weights[5]['bias'] = 17568.132065859296
        self.weights[5]['#-of-ghosts-1-step-away'] = -1486.632230130045
        self.weights[5]['closest-food'] = -0.04935921821387102
        self.weights[5]['eats-food'] = 7945.028663626653

        # originalClassic.lay
        self.weights[6]['bias'] = 21125.99892724873
        self.weights[6]['#-of-ghosts-1-step-away'] = -18867.370123322642
        self.weights[6]['closest-food'] = -54.81950905746498
        self.weights[6]['eats-food'] = 12406.9607171604

        # smallClassic.lay
        self.weights[7]['bias'] = 3177.4623378198767
        self.weights[7]['#-of-ghosts-1-step-away'] = -12899.421028313125
        self.weights[7]['closest-food'] = -167.05127486905636
        self.weights[7]['eats-food'] = 5043.480439750393

        # smallGrid.lay
        self.weights[8]['bias'] = -13464.576647629403
        self.weights[8]['#-of-ghosts-1-step-away'] = -15920.654974059871
        self.weights[8]['closest-food'] = -2318.298128051994
        self.weights[8]['eats-food'] = 3025.2494185179703

        # testClassic.lay
        self.weights[9]['bias'] = -8801.90634322086
        self.weights[9]['#-of-ghosts-1-step-away'] = 1.2678729978934449
        self.weights[9]['closest-food'] = -626.6423962761033
        self.weights[9]['eats-food'] = 2135.9073570100763

        # trickyClassic.lay
        self.weights[10]['bias'] = 10929.527052190506
        self.weights[10]['#-of-ghosts-1-step-away'] = -17739.41517532303
        self.weights[10]['closest-food'] = -124.34792753366628
        self.weights[10]['eats-food'] = 8534.452244789083

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        # Return Q(state, action) value
        self.featureVector = self.simpleExtractor.getFeatures(state, action)
        w = 0.0
        for i in range(0, 11):
            w += self.getWeights()[i].__mul__(self.featureVector)
        return w

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        return
        # We need calculate Q value by own
        next_q_value = 0.0
        next_move = (nextState, self.getPolicy(nextState))
        if next_move in self.q_values:
            next_q_value = self.q_values[next_move]

        expected_value_in_next_state = reward + self.discount * next_q_value
        value_in_current_state = self.q_values[(state, action)]

        # If values changed - update it
        if value_in_current_state != expected_value_in_next_state:
            # Update weights
            for (key, value) in self.weights.items():
                self.weights[key] = value + self.alpha * (expected_value_in_next_state - value_in_current_state) * self.featureVector[key]

        # Update QTable
        value_in_current_state = value_in_current_state + self.alpha * (expected_value_in_next_state - value_in_current_state)

        # Update epsilon in learning state
        eps = 0.05
        self.epsilon = max(0.0, -eps / 4500 * self.episodesSoFar + eps)

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        PacmanQAgent.final(self, state)
        if self.episodesSoFar == self.numTraining:
            print(self.getWeights())
            pass

if __name__ =="__main__":
    runner = StdIOPacmanRunner()
    games_num = int(input())

    agent = ApproximateQAgent()
    for _ in range(games_num):
        runner.run_game(agent)
