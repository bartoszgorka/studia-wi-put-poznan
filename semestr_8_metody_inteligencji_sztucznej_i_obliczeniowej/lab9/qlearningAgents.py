from misio.pacman.game import *
from misio.pacman.learningAgents import ReinforcementAgent
from featureExtractors import *
from misio.pacman.util import CustomCounter, lookup
import random, math
import numpy as np
from operator import itemgetter


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
        # return max([(action, self.getQValue(state, action)) for action in self.getLegalActions(state)], key=lambda k: k[1])[0]
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

    def __init__(self, epsilon=0.05, gamma=0.8, alpha=0.2, numTraining=4500, **args):
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
        self.simpleExtractor = SimpleExtractor()
        PacmanQAgent.__init__(self, **args)
        self.weights = CustomCounter()
        self.weights['bias'] = np.random.random()
        self.weights['#-of-ghosts-1-step-away'] = np.random.random()
        self.weights['closest-food'] = np.random.random()
        self.weights['eats-food'] = np.random.random()
        self.weights['can-enter'] = np.random.random()
        # self.weights['bias'] = 13855.576578152864
        # self.weights['#-of-ghosts-1-step-away'] = -28133.285682255213
        # self.weights['closest-food'] = -2.2083299825216907
        # self.weights['eats-food'] = 4157.414783996123
        self.featureVector = CustomCounter()

    def getWeights(self):
        return self.weights

    def getQValue(self, state, action):
        """
          Should return Q(state,action) = w * featureVector
          where * is the dotProduct operator
        """
        # Return Q(state, action) value
        self.featureVector = self.simpleExtractor.getFeatures(state, action)
        return self.getWeights().__mul__(self.featureVector)

    def update(self, state, action, nextState, reward):
        """
           Should update your weights based on transition
        """
        # return
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
        if self.episodesSoFar % 100 == 0:
            print(self.epsilon, self.weights)

        # did we finish training?
        if self.episodesSoFar == self.numTraining:
            print(self.getWeights())
            pass
