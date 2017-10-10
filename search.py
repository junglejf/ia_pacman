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
    return  [s, s, w, s, w, w, s, w]

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
    def dfs(graph, start): ( Algoritmo retirado do livro abaixo ele adaptado para o problema)
        visited, stack = set(), [start]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                stack.extend(graph[vertex] - visited)
        return visited
    """
    marcado = set()
    pilha = util.Stack()
    pilha.push((problem.getStartState(), []))
    while not pilha.isEmpty():
        pos, movimento = pilha.pop()
        if problem.isGoalState(pos):
            return movimento
        if pos in marcado:
            continue
        marcado.add(pos)
        candidatos = problem.getSuccessors(pos)
        for candidato, acao, custo in candidatos:
            pilha.push((candidato, movimento + [acao]))
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    marcado = set()
    fila = util.Queue()
    fila.push((problem.getStartState(), []))
    while not fila.isEmpty():
        pos, movimento = fila.pop()
        if problem.isGoalState(pos):
            return movimento
        if pos in marcado:
            continue
        marcado.add(pos)
        candidatos = problem.getSuccessors(pos)
        for candidato, acao, custo in candidatos:
            fila.push((candidato, movimento + [acao]))

    return []

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    #Teremos uma fila só que cada elemento da fila recebe uma prioridade como uma fila de banco
    "*** YOUR CODE HERE ***"
    marcado = set()
    fila = util.PriorityQueue()
    fila.push((problem.getStartState(), []),0)
    while not fila.isEmpty():
        pos, movimento = fila.pop()
        if problem.isGoalState(pos):
            return movimento
        if pos in marcado:
            continue
        marcado.add(pos)
        candidatos = problem.getSuccessors(pos)
        for candidato, acao, custo in candidatos: #agora adicionaremos a prioridade no push
            prioridade_do_candidato = problem.getCostOfActions(movimento+[acao])
            fila.push((candidato, movimento + [acao]), prioridade_do_candidato)

    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first.
    "*** YOUR CODE HERE ***"
    marcado = set()
    fila = util.PriorityQueue()
    hx = heuristic(problem.getStartState(),problem)
    fila.push((problem.getStartState(), []),hx)
    while not fila.isEmpty():
        pos, movimento = fila.pop()
        if problem.isGoalState(pos):
            return movimento
        if pos in marcado:
            continue
        marcado.add(pos)
        candidatos = problem.getSuccessors(pos)
        for candidato, acao, custo in candidatos: #agora adicionaremos a prioridade no push
            prioridade_do_candidato = problem.getCostOfActions(movimento+[acao]) + heuristic(candidato,problem)
            fila.push((candidato, movimento + [acao]), prioridade_do_candidato)

    return []"""
def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    cost = lambda aPath: problem.getCostOfActions([x[1] for x in aPath]) + heuristic(aPath[len(aPath)-1][0], problem)
    frontier = util.PriorityQueueWithFunction(cost)
    return graphSearch(problem, frontier)


"""def aStarSearch(problem, heuristic=nullHeuristic):
    closedset = []
    aStarPacman = util.PriorityQueue()
    start = problem.getStartState()
    aStarPacman.push((start, []), heuristic(start, problem))

    while not aStarPacman.isEmpty():
        node, actions = aStarPacman.pop()
        if (problem.isGoalState(node)):
            return actions
        closedset.append(node)
        for coord, direction, cost in problem.getSuccessors(node):
            if (not coord in closedset):
                new_actions = actions + [direction]
                score = problem.getCostOfActions(new_actions) + heuristic(coord, problem)
                aStarPacman.push((coord, new_actions), score)
    return []"""

def graphSearch(problem, frontier):
    print
    "Start:", problem.getStartState()
    print
    "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print
    "Start's successors:", problem.getSuccessors(problem.getStartState())

    explored = []
    frontier.push([(problem.getStartState(), "Stop", 0)])

    while not frontier.isEmpty():
        # print "frontier: ", frontier.heap
        path = frontier.pop()
        # print "path len: ", len(path)
        # print "path: ", path

        s = path[len(path) - 1]
        s = s[0]
        # print "s: ", s
        if problem.isGoalState(s):
            # print "FOUND SOLUTION: ", [x[1] for x in path]
            return [x[1] for x in path][1:]

        if s not in explored:
            explored.append(s)
            # print "EXPLORING: ", s

            for successor in problem.getSuccessors(s):
                # print "SUCCESSOR: ", successor
                if successor[0] not in explored:
                    successorPath = path[:]
                    successorPath.append(successor)
                    # print "successorPath: ", successorPath
                    frontier.push(successorPath)
                    # else:
                    # print successor[0], " IS ALREADY EXPLORED!!"

    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
