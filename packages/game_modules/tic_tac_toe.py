from packages.utils import Value


class TicTacToe(object):
    """
    Game logic for TicTacToe
    """

    PLAYER_PIECES = ['x', 'o']

    def __init__(self):
        """
        Initialize the play board
        """
        self.board = [
            [None, None, None],
            [None, None, None],
            [None, None, None]
        ]
        self.players_turn = 0

    def unhash(self, position):
        """
        Turn a position into a board
        """
        player_turn, board = position.split(':')
        player_turn = int(player_turn)
        board = list(board)
        return (player_turn, board)

    def hash(self, player_turn, board):
        """
        Turn a board into a position
        """
        return ':'.join([str(player_turn), ''.join(board)])

    def get_moves(self):
        """
        Get supported moves
        """
        moves = []
        for row, columns in enumerate(self.board):
            for column, space in enumerate(columns):
                if not space:
                    moves.append((row + 1, column + 1))
        return moves

    def do_move(self, move):
        """
        Apply the move to the current board
        """
        #move = literal_eval(move)
        self.board[move[0] - 1][move[1] - 1] = self.PLAYER_PIECES[self.players_turn]
        self.players_turn = (self.players_turn + 1) % 2

    def get_value(self):
        """
        Return if this is an ending position
        """
        other_player = (self.players_turn + 1) % 2
        piece = self.PLAYER_PIECES[other_player]
        # rows
        for row in range(0, 3):
            if self.board[row][0] == self.board[row][1] == self.board[row][2] == piece:
                return Value.LOSS
        # columns
        for column in range(0, 3):
            if self.board[0][column] == self.board[1][column] == self.board[2][column] == piece:
                return Value.LOSS

        # diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] == piece:
            return Value.LOSS
        if self.board[0][2] == self.board[1][1] == self.board[2][0] == piece:
            return Value.LOSS

        for row in self.board:
            for space in row:
                if space is None:
                    return Value.UNKNOWN
        return Value.TIE

    def print_position(self):
        """
        Print the specified position
        """
        print
        print '======================='
        print 'Current game board:'
        for row_i, row in enumerate(self.board):
            for column_i, space in enumerate(row):
                if space:
                    print space,
                else:
                    print ' ',
                if column_i < 2:
                    print ' | ',
                else:
                    print
            if row_i < 2:
                print '-------------'
        print 'Player %s\'s turn (%s)!' % (str(self.players_turn + 1), self.PLAYER_PIECES[self.players_turn])
        print '======================='
        print

    @staticmethod
    def _index_to_coords(index):
        """
        Converts a linear index to a row x column

        >>> TicTacToe._index_to_coords(0)
        (1, 1)
        >>> TicTacToe._index_to_coords(1)
        (1, 2)
        >>> TicTacToe._index_to_coords(3)
        (2, 1)
        >>> TicTacToe._index_to_coords(4)
        (2, 2)
        >>> TicTacToe._index_to_coords(8)
        (3, 3)
        """
        return (index / 3 + 1, index % 3 + 1)

    @staticmethod
    def _coords_to_index(row, column):
        """
        Converts a row x clumn to a linear index

        >>> TicTacToe._coords_to_index(1, 1)
        0
        >>> TicTacToe._coords_to_index(1, 2)
        1
        >>> TicTacToe._coords_to_index(2, 1)
        3
        >>> TicTacToe._coords_to_index(2, 2)
        4
        >>> TicTacToe._coords_to_index(3, 3)
        8
        """
        return (row - 1) * 3 + column - 1
