# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    node = problem.getStartState()  # Get inital node
    # If the problem goal state = node state then return the solution
    if problem.isGoalState(node):
        return []

    stack_queue = util.Stack()
    seen_nodes = []
    stack_queue.push((node, []))  # Starting node and action

    while not stack_queue.isEmpty():
        current_node, actions = stack_queue.pop()

        if current_node not in seen_nodes:
            seen_nodes.append(current_node)

            if problem.isGoalState(current_node):
                return actions

            for next_node, move, cost in problem.getSuccessors(current_node):
                new_action = actions + [move]
                stack_queue.push((next_node, new_action))

    util.raiseNotDefined()


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    node = problem.getStartState()  # initial node
    # if the problem goal state  = node state then return the solution
    if problem.isGoalState(node):
        return []

    # Get a FIFO queue
    fifo_queue = util.Queue()
    # Add an empty list
    seen_nodes = []

    # Node and action
    fifo_queue.push((node, []))

    while not fifo_queue.isEmpty():
        current_node, actions = fifo_queue.pop()  # removes shallowest

        if current_node not in seen_nodes:
            seen_nodes.append(current_node)

            if problem.isGoalState(current_node):
                return actions
            for next_node, move, cost in problem.getSuccessors(current_node):
                new_actions = actions + [move]
                fifo_queue.push((next_node, new_actions))

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    node = problem.getStartState()
    # if the problem goal state  = node state then return the solution
    if problem.isGoalState(node):
        return []
    # Add an empty list
    seen_nodes = []
    priority_queue = util.PriorityQueue()
    # Node ,action to current node ,cost to current node and priority
    priority_queue.push((node, [], 0), 0)

    while not priority_queue.isEmpty():
        current_node, actions, previous_cost = priority_queue.pop()
        if current_node not in seen_nodes:
            seen_nodes.append(current_node)

            if problem.isGoalState(current_node):
                return actions

            for next_node, move, cost in problem.getSuccessors(current_node):
                new_action = actions + [move]
                priority = previous_cost + cost
                priority_queue.push((next_node, new_action, priority), priority)
    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    node = problem.getStartState()
    # if the problem goal state  = node state then return the solution
    if problem.isGoalState(node):
        return []

    priority_queue = util.PriorityQueue()
    seen_nodes = []
    # node, action to current node, cost to current node,priority
    priority_queue.push((node, [], 0), 0)

    while not priority_queue.isEmpty():
        current_node, actions, previous_cost = priority_queue.pop()

        if current_node not in seen_nodes:
            seen_nodes.append(current_node)

            if problem.isGoalState(current_node):
                return actions

            for next_node, move, cost in problem.getSuccessors(current_node):
                new_action = actions + [move]
                priority = previous_cost + cost
                total_cost = priority + heuristic(next_node, problem)
                priority_queue.push((next_node, new_action, priority), total_cost)

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
