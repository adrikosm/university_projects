# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()  # Get current game score

        food_list = newFood.asList()  # Make it a list so we can iterate it
        for food in food_list:
            food_distance = util.manhattanDistance(food, newPos)  # Get minimum distnace to food
            if food_distance != 0:
                score += add_score(food_distance)

        ghost_list = newGhostStates.asList()  # Make it a list so we can iterate it
        for ghost in ghost_list:
            ghost_position = ghost.getPosition()
            ghost_distance = util.manhattanDistance(ghost_position, newPos)
            check_position = abs(newPos[0] - ghost_position[0]) + abs(newPos[1] - ghost_position[1])
            # ^ if the position is positive it means the ghost has not caught pacman

            if check_position > 1:
                score += add_score(ghost_distance)

        def add_score(distance):
            return 1.0 / distance


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def MiniMax_func(self, depth, agentIndex, gameState):
        # Check game state
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState)

        node_store = []  # Used to store value for node action
        node_action = gameState.getLegalActions(agentIndex)  # Used to store actions

        for action in node_action:
            successor = gameState.generateSuccessor(agentIndex, action)
            if agentIndex + 1 >= gameState.getNumAgents():
                node_store += [self.MiniMax_func(depth + 1, 0, successor)]  # Recursion needs to be saved into list
            else:
                node_store += [self.MiniMax_func(depth, agentIndex + 1, successor)]
                # Check the position of the agent index
        if agentIndex == 0:
            if depth == 1:  # If position is root return the action
                max_score = max(node_store)
                for i in range(len(node_store)):
                    if node_store[i] == max_score:
                        return node_action[i]
            else:  # Else return the max node value
                node_val = max(node_store)
        # Ghosts
        elif agentIndex > 0:
            node_val = min(node_store)

        return node_val

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        return self.MiniMax_func(1, 0, gameState) # Depth , pacmanindex,gamestate


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def AlphaBeta_func(self,depth,agentIndex,gameState,a,b):
        alpha = a
        beta = b

        # Check game state
        if gameState.isWin() or gameState.isLose() or depth > self.depth:
            return self.evaluationFunction(gameState)


        node_store = [] # Used to store node actions
        node_action = gameState.getLegalActions(agentIndex) # Used to store the actions

        for action in node_action:
            successor = gameState.generateSuccessor(agentIndex,action)

            if agentIndex + 1 >= gameState.getNumAgents():
                # Use temp_store to compare with alpha,beta
                temp_store = self.AlphaBeta_func(depth + 1, 0,successor,alpha,beta)
            else:
                temp_store = self.AlphaBeta_func(depth,agentIndex + 1,successor,alpha,beta)

            if agentIndex == 0 and temp_store > beta:
                return temp_store
            if agentIndex > 0 and temp_store < alpha:
                return temp_store
            
            if agentIndex == 0 and temp_store > alpha:
                alpha = temp_store
            if agentIndex > 0 and temp_store < beta:
                beta = temp_store

            node_store += [temp_store] # Make temp_store a list

        if agentIndex == 0:
            if depth == 1: # If position is root return the action
                max_score = max(node_store)
                for i in range(len(node_store)):
                    if node_store[i] == max_score:
                        return node_action[i]
            else:  # Else return the node value
                    node_val = max(node_store)
                    # Ghost
        elif agentIndex > 0:
                node_val = min(node_store)

        return node_val


        

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.AlphaBeta_func(1,0,gameState,-10000,100000)# Depth , pacmanindex,gamestate,alpha,beta


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def Expectimax_func(self,depth,agentIndex):
        pass



    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
