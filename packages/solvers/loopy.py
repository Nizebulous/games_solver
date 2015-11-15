from packages.utils import Value


class Loopy(object):
    """
    Loopy-style solver
    """

    def __init__(self, game_logic, solution_store):
        """
        Setup the game for solving
        """
        self.game_logic = game_logic
        self.board = game_logic()
        self.game_solution = solution_store(game_logic.id())
        self.seen = set()
        self.value_changed = True

    def _solve(self):
        """
        Solve the game provided
        """
        position = self.board.hash()
        if position in self.seen:
            return self.game_solution.get_value(self.board)
        self.seen.add(position)
        if not self.game_solution.get_value(self.board):
            values_seen = set()
            for move in self.board.get_moves():
                self.board.do_move(move)
                values_seen.add(self._solve())
                self.board.undo_move(move)
            if Value.LOSS in values_seen:
                determined_value = Value.WIN
            elif Value.TIE in values_seen:
                determined_value = Value.TIE
            elif Value.UNKNOWN in values_seen:
                determined_value = Value.UNKNOWN
            else:
                determined_value = Value.LOSS
            self.game_solution.set_value(self.board, determined_value)
        return self.game_solution.get_value(self.board)

    def _resolve_unknown(self):
        """
        Resolve fields marked as unkown
        """
        position = self.board.hash()
        if position in self.seen:
            return self.game_solution.get_value(self.board)
        self.seen.add(position)
        values_seen = set()
        for move in self.board.get_moves():
            self.board.do_move(move)
            values_seen.add(self._resolve_unknown())
            self.board.undo_move(move)
        old_value = self.game_solution.get_value(self.board)
        if not old_value:
            if Value.LOSS in values_seen:
                determined_value = Value.WIN
            elif Value.TIE in values_seen:
                determined_value = Value.TIE
            elif Value.UNKNOWN in values_seen:
                determined_value = Value.UNKNOWN
            elif Value.WIN in values_seen:
                determined_value = Value.LOSS
            if old_value != determined_value:
                self.value_changed = True
            self.game_solution.set_value(self.board, determined_value)
        return self.game_solution.get_value(self.board)

    def solve(self):
        value = self._solve()
        while self.value_changed:
            self.seen = set()
            self.value_changed = False
            value = self._resolve_unknown()
        print 'Solution is a:', value
        self.game_solution.store()
