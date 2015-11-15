from base import BaseGame

from packages.utils import Value


class Chopsticks(BaseGame):
    """
    The finger game of Chopsticks
    """

    DEAD_HAND = 6

    def __init__(self):
        """
        Initialize the play board
        """
        self.board = [1, 1, 1, 1]
        self.players_turn = 0
        self.hands = ['left', 'right']
        self.hands_map = {
            'left': 0,
            'right': 1
        }

    def hash(self):
        """
        Turn a board into a position
        """
        pos_hash = 0
        for hand in self.board:
            pos_hash += hand - 1
            pos_hash *= 6
        pos_hash /= 6
        pos_hash <<= 1
        pos_hash += self.players_turn
        return pos_hash

    @classmethod
    def unhash(cls, pos_hash):
        """
        Turn a position (value) into a board
        """
        board = cls()
        board.players_turn = pos_hash % 2
        pos_hash >>= 1
        for index in range(3, -1, -1):
            board.board[index] = (pos_hash % 6) + 1
            pos_hash = int(pos_hash / 6)
        return board

    def get_moves(self):
        """
        Get supported moves
        """
        moves = []
        source_first_hand_index = self.players_turn * 2
        dest_first_hand_index = (source_first_hand_index + 2) % 4
        for index in range(source_first_hand_index, source_first_hand_index + 2):
            if self.board[index] != self.DEAD_HAND:
                for second_index in range(dest_first_hand_index, dest_first_hand_index + 2):
                    if self.board[second_index] == self.DEAD_HAND:
                        continue
                    moves.append((self.hands[index % 2], self.hands[second_index % 2]))
        return moves

    def do_move(self, move):
        """
        Apply the move to the current board
        """
        source_first_hand_index = self.players_turn * 2
        dest_first_hand_index = (source_first_hand_index + 2) % 4
        source = source_first_hand_index + self.hands_map[move[0]]
        dest = dest_first_hand_index + self.hands_map[move[1]]
        self.board[dest] = (self.board[dest] + self.board[source]) % 5 or self.DEAD_HAND
        self.players_turn = (self.players_turn + 1) % 2

    def undo_move(self, move):
        """
        Unapply the move that resulted in the current board
        """
        dest_first_hand_index = self.players_turn * 2
        source_first_hand_index = (dest_first_hand_index + 2) % 4
        source = source_first_hand_index + self.hands_map[move[0]]
        dest = dest_first_hand_index + self.hands_map[move[1]]
        old_value = 0 if self.board[dest] == self.DEAD_HAND else self.board[dest]
        self.board[dest] = (old_value - self.board[source]) % 5
        self.players_turn = (self.players_turn + 1) % 2

    def get_value(self):
        """
        Return if this is an ending position
        """
        first_hand_index = self.players_turn * 2
        if self.board[first_hand_index] == self.DEAD_HAND and \
                self.board[first_hand_index + 1] == self.DEAD_HAND:
            return Value.LOSS
        return Value.UNKNOWN

    def print_position(self):
        """
        Print the specified position
        """
        board = [hand if hand != self.DEAD_HAND else 'X' for hand in self.board]
        print '    Player 1:               Player 2:'
        print 'left: {}  right: {}      left: {}  right: {}'.format(*board)
        print
        print 'Player {}\'s turn!'.format(str(self.players_turn + 1))
        print '======================='
        print
