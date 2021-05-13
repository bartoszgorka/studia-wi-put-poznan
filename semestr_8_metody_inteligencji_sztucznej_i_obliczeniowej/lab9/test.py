from misio.pacman.game import *
from misio.pacman.learningAgents import ReinforcementAgent
from featureExtractors import *
from misio.pacman.util import CustomCounter, lookup
import random, math
import numpy as np
from operator import itemgetter


class Node:
	def __init__(self, pos, distance=-1):
		self.position = pos
		self.x = pos[0]
		self.y = pos[1]
		self.distance = distance
		self.neighbors = []


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

    # def getQValue(self, state, action):
    #     """
    #       Returns Q(state,action)
    #       Should return 0.0 if we have never seen a state
    #       or the Q node value otherwise
    #     """
    #     if (state, action) in self.q_values:
    #         return self.q_values[(state, action)]
    #     else:
    #         self.q_values[(state, action)] = 0.0
    #         return 0.0

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

            # Select best value
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
        if np.random.rand() > self.epsilon:
            return self.getPolicy(state)
        else:
            # Get list of possibled action in current state
            legal_actions = self.getLegalActions(state)

            if len(legal_actions) > 0:
                return np.random.choice(legal_actions)
            else:
                return None

    def update(self, state, action, nextState, reward):
        """
          The parent class calls this to observe a
          state = action => nextState and reward transition.
          You should do your Q-Value update here

          NOTE: You should never call this function,
          it will be called on your behalf
        """
        # Calculate values
        modification_value = reward + self.discount * self.computeValueFromQValues(nextState)
        q_value = self.getQValue(state, action)

        # Update stored Q-values
        self.q_values[(state, action)] = q_value + self.alpha * (self.alpha * modification_value - q_value)

    def getPolicy(self, state):
        return self.computeActionFromQValues(state)

    def getValue(self, state):
        return self.computeValueFromQValues(state)


class ApproximateQAgent(QLearningAgent):
    """
       ApproximateQLearningAgent

       You should only have to overwrite getQValue
       and update.  All other QLearningAgent functions
       should work as is.

       These default parameters can be changed from the pacman.py command line.
       For example, to change the exploration rate, try:
           python pacman.py -p PacmanQLearningAgent -a epsilon=0.1

       alpha    - learning rate
       epsilon  - exploration rate
       gamma    - discount factor
       numTraining - number of training episodes, i.e. no learning after these many episodes
    """

    def construct_graph(self, state):
        width = state.getFood().width
        height = state.getFood().height
        nodes = []
        for x in range(width):
        	nodes.append([])
        	for y in range(height):
        		nodes[x].append(Node((x,y)))

        for x in range(width):
        	for y in range(height):
        		d = [666, 1, 0, -1, 0]
        		for k in range(1, 4 + 1):
        			cx = x + d[k]
        			cy = y + d[-k]
        			if cx >= 0 and cx < width:
        				if cy >= 0 and cy < height:
        					if not state.hasWall(cx, cy):
        						nodes[x][y].neighbors.append(nodes[cx][cy])
        return nodes

    def __init__(self, extractor='SimpleExtractor', epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=1000, **args):
        args['epsilon'] = epsilon
        args['gamma'] = gamma
        args['alpha'] = alpha
        args['numTraining'] = numTraining
        self.original_epsilon = float(epsilon)
        self.index = 0
        self.nodes = []
        self.totalFoodCount = 100
        self.builtNodes = False
        self.featExtractor = lookup(extractor, globals())()
        QLearningAgent.__init__(self, **args)
        self.weights = CustomCounter()
        # self.weights['bias'] = -503.53462799655483
        # self.weights['#-of-ghosts-1-step-away'] = -3381.0858534955764
        # self.weights['closest-food'] = -34.11760067073395
        # self.weights['eats-food'] = 715.8383534418471
        # self.weights['remains-food'] = -81.75959477367374
        # self.weights['nearest-ghost'] = 130.04860762210964
        # self.weights['capsules-still-on-map'] = -11.092029839725715

    def getAction(self, state):
        """
        Simply calls the getAction method of QLearningAgent and then
        informs parent of action for Pacman.  Do not change or remove this
        method.
        """
        action = QLearningAgent.getAction(self,state)
        self.doAction(state,action)
        return action

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        # Return Q(state, action) value
        if not self.builtNodes:
            self.nodes = self.construct_graph(state)
            self.totalFoodCount = state.getNumFood()
            self.builtNodes = True
            self.featExtractor.setData(self.nodes, self.totalFoodCount)

        return self.getWeights().__mul__(self.featExtractor.getFeatures(state, action))

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        if not self.builtNodes:
            self.nodes = self.construct_graph(nextState)
            self.totalFoodCount = nextState.getNumFood()
            self.builtNodes = True
            self.featExtractor.setData(self.nodes, self.totalFoodCount)

        # Calculate value
        q_value = reward + self.discount * self.getValue(nextState) - self.getQValue(state, action)

        # Get all features
        features = self.featExtractor.getFeatures(state, action)

        # Update weights
        for (feature_name, feature_value) in features.items():
            self.getWeights()[feature_name] += self.alpha * q_value * feature_value

    def final(self, state):
        "Called at the end of each game."
        # call the super-class final method
        QLearningAgent.final(self, state)
        self.epsilon = max(0.0, self.epsilon - self.original_epsilon / (self.numTraining + 1))

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            print(self.getWeights())
            pass
