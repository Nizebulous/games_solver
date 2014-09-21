#! /usr/bin/python

import argparse
from types import FunctionType
from ConfigParser import ConfigParser

from packages import modules
from packages import solvers
from packages import player_engines
from packages import solution_stores
from packages.utils import Value


games_config = ConfigParser()
games_config.read('games.conf')


def list():
    """
    List the supported games
    """
    print "Supported games:"
    games = filter(lambda x: not x.startswith('__'), dir(modules))
    print
    for game in games:
        game_class = getattr(modules, game)
        print game, ' - ', game_class.__doc__
    print


def play(game):
    """
    Play a specified game
    """
    print "Loading ", game, "..."
    game_logic = getattr(modules, game)
    board = game_logic()
    players = [
        getattr(player_engines, games_config.get('player_one', 'engine'))(games_config, game_logic),
        getattr(player_engines, games_config.get('player_two', 'engine'))(games_config, game_logic)
    ]
    player_turn = 0
    while True:
        board.print_position()
        command = players[player_turn].get_input(board, ['q'])
        if command == 'q':
            break
        else:
            try:
                board.do_move(command)
            except Exception:
                print 'Invalid move!'
            else:
                value = board.get_value()
                if value:
                    if value == Value.LOSS:
                        board.print_position()
                        print 'Player %s wins!' % str(player_turn + 1)
                    else:
                        board.print_position()
                        print 'Cat\'s game!'
                    break
                player_turn = (player_turn + 1) % 2


def solve(game):
    """
    Solve and store a specified game
    """
    print "Solving", game, "..."
    game_logic = getattr(modules, game)
    solution_store = getattr(solution_stores, games_config.get('solution', 'engine'))
    game_solver = getattr(solvers, games_config.get('solver', 'engine'))(game_logic, solution_store)
    game_solver.solve()
    print "Done."


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2-person perfect information game solver')
    current_scope = globals()
    parser.add_argument('command', choices=filter(lambda x: isinstance(current_scope[x], FunctionType), current_scope))
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    current_scope[args.command](*args.args)
