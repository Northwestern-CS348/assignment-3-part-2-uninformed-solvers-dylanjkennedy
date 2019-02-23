from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        state = []
        for i in range (1,4):
            first_ask = parse_input('fact: (top ?X peg'+str(i)+')')
            first_answer = self.kb.kb_ask(first_ask)
            try:
                first_answer[0]
            except:
                pass
            first_disk = str(first_answer[0]).split()[-1]
            if first_disk == 'base':
                peg_list = []
            else:
                peg_list = [int(first_disk[-1])]
                next_ask = parse_input('fact: (ontop disk'+str(peg_list[-1])+' ?X)')
                next_answer = self.kb.kb_ask(next_ask)
                next_disk = str(next_answer[0]).split()[-1]
                while next_disk != 'base':
                    peg_list.append(int(next_disk[-1]))
                    next_ask = parse_input('fact: (ontop disk'+str(peg_list[-1])+' ?X)')
                    next_answer = self.kb.kb_ask(next_ask)
                    next_disk = str(next_answer[0]).split()[-1]
            state.append(peg_list)
        tuple_state = tuple([tuple(x) for x in state])
        return tuple_state

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        string_statement = str(movable_statement)
        disk_a = string_statement.split()[1]
        peg_a = string_statement.split()[2]
        #drop the ')'
        peg_b = string_statement.split()[3][:-1]

        #disk1 is no longer top of peg1
        removal = parse_input('fact: (top '+disk_a+' '+peg_a+')')
        self.kb.kb_retract(removal)
        
        #whatever disk1 was ontop of is now top of peg1
        ask = parse_input('fact: (ontop '+disk_a+' ?x)')
        answer = self.kb.kb_ask(ask)
        new_top = str(answer[0]).split()[-1]
        addition = parse_input('fact: (top '+new_top+' '+peg_a+')')
        self.kb.kb_assert(addition)
        
        #disk1 is not ontop of whatever it was ontop of
        removal = parse_input('fact: (ontop '+disk_a+' '+new_top+')')
        self.kb.kb_retract(removal)
        
        #disk1 is now ontop of whatever was top of peg3
        ask = parse_input('fact: (top ?x '+peg_b+')')
        answer = self.kb.kb_ask(ask)
        old_top = str(answer[0]).split()[-1]
        addition = parse_input('fact: (ontop '+disk_a+' '+old_top+')')
        self.kb.kb_assert(addition)
        
        #disk1 is now top of peg3
        addition = parse_input('fact: (top '+disk_a+' '+peg_b+')')
        self.kb.kb_assert(addition)
        
        #whatever disk1 is ontop of is not top of peg3
        removal = parse_input('fact: (top '+old_top+' '+peg_b+')')
        self.kb.kb_retract(removal)
        
    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here
        state = []
        for y in range(1, 4):
            row = []
            for x in range(1, 4):
                ask = parse_input('fact: (pos ?X pos' + str(x) + ' pos' + str(y)+')')
                answer = self.kb.kb_ask(ask)
                # -1 because we only want the tile part of the binding, and then only the number
                tile = str(answer[0]).split()[-1][-1]
                #y is the last letter in empty
                if tile == 'y':
                    tile = -1
                else:
                    tile = int(tile)
                row.append(tile)
            state.append(row)
        tuple_state = tuple([tuple(x) for x in state])
        return tuple_state

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        stated_array = str(movable_statement).split()
        tile = stated_array[1]
        old_pos_x = stated_array[2]
        old_pos_y = stated_array[3]
        new_pos_x = stated_array[4]
        new_pos_y = stated_array[5][:-1]

        if (old_pos_x == new_pos_x) and (old_pos_y == new_pos_y):
            return

        # fix the move tile
        removal = parse_input('fact: (pos ' + tile + ' ' + old_pos_x + ' ' + old_pos_y + ')')
        self.kb.kb_retract(removal)
        addition = parse_input('fact: (pos ' + tile + ' ' + new_pos_x + ' ' + new_pos_y + ')')
        self.kb.kb_assert(addition)

        # fix the empty space
        addition = parse_input('fact: (pos empty ' + old_pos_x + ' ' + old_pos_y + ')')
        self.kb.kb_assert(addition)
        removal = parse_input('fact: (pos empty ' + new_pos_x + ' ' + new_pos_y + ')')
        self.kb.kb_retract(removal)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
