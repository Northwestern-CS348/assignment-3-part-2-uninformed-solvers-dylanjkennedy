
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        """
        SOLVER
        self.gm = gameMaster
        self.visited = dict()
        self.currentState = GameState(self.gm.getGameState(), 0, None)
        self.visited[self.currentState] = True
        self.victoryCondition = victoryCondition
        
        GAMESTATE
        self.children = []
        self.nextChildToVisit = GameState.FIRST_CHILD_INDEX
        self.parent = None
        self.requiredMovable = movableToReachThisState
        self.state = state
        self.depth = depth

        """
        if self.gm.getGameState() == self.victoryCondition:
            return True

        options = self.gm.getMovables()
        current = self.currentState
        # if the state has no children yet,
        if not current.children:
            for move in options:
                self.gm.makeMove(move)
                child = GameState(self.gm.getGameState(), current.depth+1, move)
                child.parent = current
                current.children.append(child)
                self.gm.reverseMove(move)

        self.visited[current] = True

        found_unexplored_child = False
        for child in self.currentState.children:
            visited_states = [x.state for x in self.visited.keys()]
            if child.state not in visited_states:
                self.gm.makeMove(child.requiredMovable)
                self.currentState = child
                debug = child.state
                print(debug)
                found_unexplored_child = True
                break
        if not found_unexplored_child:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            self.solveOneStep()
        return False


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        """
        SOLVER
        self.gm = gameMaster
        self.visited = dict()
        self.currentState = GameState(self.gm.getGameState(), 0, None)
        self.visited[self.currentState] = True
        self.victoryCondition = victoryCondition

        GAMESTATE
        self.children = []
        self.nextChildToVisit = GameState.FIRST_CHILD_INDEX
        self.parent = None
        self.requiredMovable = movableToReachThisState
        self.state = state
        self.depth = depth

        """
        if self.gm.getGameState() == self.victoryCondition:
            return True

        options = self.gm.getMovables()
        current = self.currentState
        # if the state has no children yet,
        if not current.children:
            for move in options:
                self.gm.makeMove(move)
                child = GameState(self.gm.getGameState(), current.depth + 1, move)
                child.parent = current
                current.children.append(child)
                self.gm.reverseMove(move)

        self.visited[current] = True

        found_unexplored_child = False
        for child in self.currentState.children:
            visited_states = [x.state for x in self.visited.keys()]
            if child.state not in visited_states:
                self.gm.makeMove(child.requiredMovable)
                self.currentState = child
                debug = child.state
                print(debug)
                found_unexplored_child = True
                break
        if not found_unexplored_child:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent
            self.solveOneStep()
        return False
