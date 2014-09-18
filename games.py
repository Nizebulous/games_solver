#! /usr/bin/python

import argparse
from types import FunctionType
from ConfigParser import ConfigParser

from packages import game_modules
from packages import player_engines
from packages.utils import Value


games_config = ConfigParser()
games_config.read('games.conf')


def list():
    """
    List the supported games
    """
    print "Supported games:"
    games = filter(lambda x: not x.startswith('__'), dir(game_modules))
    print
    for game in games:
        game_class = getattr(game_modules, game)
        print game, ' - ', game_class.__doc__
    print


def play(game):
    """
    Play a specified game
    1. Solve if it hasn't been solved
    2. Start game-loop
    """
    print "Loading ", game, "..."
    game_logic = getattr(game_modules, game)()
    players = [
        getattr(player_engines, games_config.get('player_one', 'engine'))(),
        getattr(player_engines, games_config.get('player_two', 'engine'))()
    ]
    player_turn = 0
    while True:
        moves = game_logic.get_moves()
        game_logic.print_position()
        command = players[player_turn].get_input(['q'], moves)
        if command == 'q':
            break
        else:
            try:
                game_logic.do_move(command)
            except Exception:
                print 'Invalid move!'
            else:
                value = game_logic.get_value()
                if value:
                    if value == Value.LOSS:
                        game_logic.print_position()
                        print 'Player %s wins!' % str(player_turn + 1)
                    else:
                        game_logic.print_position()
                        print 'Cat\'s game!'
                    break
                player_turn = (player_turn + 1) % 2


def solve(game):
    """
    Solve and store a specified game
    """
    print 'Not currently supported!'
    #print "Solving ", game, "..."


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='2-person perfect information game solver')
    current_scope = globals()
    parser.add_argument('command', choices=filter(lambda x: isinstance(current_scope[x], FunctionType), current_scope))
    parser.add_argument('args', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    current_scope[args.command](*args.args)
