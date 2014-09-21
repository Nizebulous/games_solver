from packages.utils import Value


class SimpleTree(object):
    """
    Simple tree-style solver
    """

    def __init__(self, game_logic, solution_store):
        """
        Setup the game for solving
        """
        self.game_logic = game_logic
        self.board = game_logic()
        self.game_solution = solution_store(game_logic.id())

    def _solve(self):
        """
        Solve the game provided
        """
        if not self.game_solution.get_value(self.board):
            children_values = []
            for move in self.board.get_moves():
                self.board.do_move(move)
                children_values.append(self._solve())
                self.board.undo_move(move)
            determined_value = Value.LOSS
            for value in children_values:
                if value == Value.LOSS:
                    determined_value = Value.WIN
                    break
                elif value == Value.TIE:
                    determined_value = Value.TIE
            self.game_solution.set_value(self.board, determined_value)
        return self.game_solution.get_value(self.board)

    def solve(self):
        self._solve()
        self.game_solution.store()
