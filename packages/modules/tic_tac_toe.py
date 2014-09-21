from base import BaseGame

from packages.utils import Value


class TicTacToe(BaseGame):
    """
    The classic game of Tic Tac Toe
    """

    PLAYER_PIECES = ['x', 'o', ' ']
    X = 0
    O = 1
    EMPTY = 2

    def __init__(self):
        """
        Initialize the play board
        """
        self.board = [
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY],
            [self.EMPTY, self.EMPTY, self.EMPTY]
        ]
        self.players_turn = 0

    def hash(self):
        """
        Turn a board into a position
        """
        hash = 0
        for index in range(9):
            row, col = self._index_to_coords(index)
            hash += self.board[row][col]
            if index != 8:
                hash <<= 2
        return hash

    @classmethod
    def unhash(cls, hash):
        """
        Turn a position (value) into a board
        """
        board = cls()
        x_count = 0
        o_count = 0
        for index in range(9).reverse():
            row, col = cls._index_to_coords(index)
            piece_value = hash % 4
            board[row][col] = piece_value
            if cls.PLAYER_PIECES[piece_value] == 'x':
                x_count += 1
            elif cls.PLAYER_PIECES[piece_value] == 'o':
                o_count += 1
            hash >>= 2
        if x_count == o_count + 1:
            board.players_turn = 1
        else:
            assert(x_count == o_count)
        return board

    def get_moves(self):
        """
        Get supported moves
        """
        moves = []
        for row, columns in enumerate(self.board):
            for column, space in enumerate(columns):
                if space == self.EMPTY:
                    moves.append((row + 1, column + 1))
        return moves

    def do_move(self, move):
        """
        Apply the move to the current board
        """
        self.board[move[0] - 1][move[1] - 1] = self.players_turn
        self.players_turn = (self.players_turn + 1) % 2

    def undo_move(self, move):
        """
        Unapply the move that resulted in the current board
        """
        self.board[move[0] - 1][move[1] - 1] = self.EMPTY
        self.players_turn = (self.players_turn + 1) % 2

    def get_value(self):
        """
        Return if this is an ending position
        """
        other_player = (self.players_turn + 1) % 2
        # rows
        for row in range(0, 3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == other_player:
                return Value.LOSS
        # columns
        for column in range(0, 3):
            if self.board[0][column] == self.board[1][column] == self.board[2][column] == other_player:
                return Value.LOSS

        # diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == other_player:
            return Value.LOSS
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == other_player:
            return Value.LOSS

        for row in self.board:
            for space in row:
                if space == self.EMPTY:
                    return Value.UNKNOWN
        return Value.TIE

    def print_position(self):
        """
        Print the specified position
        """
        print
        print '======================='
        print 'Current game board:'
        print
        print '                columns'
        print '             1  |  2  |  3'
        print '         --------------------'
        print '        |'
        for row_i, row in enumerate(self.board):
            if row_i == 1:
                print 'rows ', row_i + 1, '|   ',
            else:
                print '     ', row_i + 1, '|   ',
            for column_i, space in enumerate(row):
                print self.PLAYER_PIECES[space],
                if column_i < 2:
                    print ' | ',
                else:
                    print
            if row_i < 2:
                print '     -- |   ---------------'
        print '        |'
        print
        print 'Player %s\'s turn (%s)!' % (str(self.players_turn + 1), self.PLAYER_PIECES[self.players_turn])
        print '======================='
        print

    @staticmethod
    def _index_to_coords(index):
        """
        Converts a linear index to a row x column

        >>> TicTacToe._index_to_coords(0)
        (0, 0)
        >>> TicTacToe._index_to_coords(1)
        (0, 1)
        >>> TicTacToe._index_to_coords(3)
        (1, 0)
        >>> TicTacToe._index_to_coords(4)
        (1, 1)
        >>> TicTacToe._index_to_coords(8)
        (2, 2)
        """
        return (index / 3, index % 3)

    @staticmethod
    def _coords_to_index(row, column):
        """
        Converts a row x clumn to a linear index

        >>> TicTacToe._coords_to_index(0, 0)
        0
        >>> TicTacToe._coords_to_index(0, 1)
        1
        >>> TicTacToe._coords_to_index(1, 0)
        3
        >>> TicTacToe._coords_to_index(1, 1)
        4
        >>> TicTacToe._coords_to_index(2, 2)
        8
        """
        return (row) * 3 + column
