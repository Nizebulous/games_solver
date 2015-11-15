from base import BasePlayer

from packages import solvers
from packages.utils import Value
from packages import solution_stores


class Computer(BasePlayer):

    def __init__(self, *args, **kwargs):
        """
        Initialize the computer
        """
        super(Computer, self).__init__(*args, **kwargs)
        solution_store = getattr(solution_stores, self.player_config.get('solution', 'engine'))
        self.game_solution = solution_store(self.game_logic.id())
        if not self.game_solution.get_value(self.game_logic()):
            solver = getattr(
                solvers, self.player_config.get('solver', 'engine')
            )(self.game_logic, solution_store)
            solver.solve()
            self.game_solution.load()

    def get_input(self, board, menu_commands):
        """
        Get the computer's input
        """
        moves = board.get_moves()
        moves_by_value = {}
        for index, move in enumerate(moves):
            board.do_move(move)
            value = self.game_solution.get_value(board)
            moves_by_value.setdefault(value, []).append((index, move))
            board.undo_move(move)

        print 'Possible moves: '
        if moves:
            for index, move in enumerate(moves, start=1):
                print '%s. %s' % (index, move)

        if Value.LOSS in moves_by_value:
            chosen_index, chosen_move = moves_by_value[Value.LOSS][0]
        elif Value.TIE in moves_by_value:
            chosen_index, chosen_move = moves_by_value[Value.TIE][0]
        elif Value.DRAW in moves_by_value:
            chosen_index, chosen_move = moves_by_value[Value.DRAW][0]
        elif Value.WIN in moves_by_value:
            chosen_index, chosen_move = moves_by_value[Value.WIN][0]

        print
        print 'Computer chooses: %s. %s' % (chosen_index + 1, chosen_move)
        return chosen_move
