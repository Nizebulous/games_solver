class Human(object):

    def get_input(self, menu_commands, moves):
        while True:
            print 'Possible moves: '
            if moves:
                for index, move in enumerate(moves, start=1):
                    print '%s. %s' % (index, move)
                options_string = '1 - %i, ' % len(moves)
            else:
                options_string = ''
                print 'None'
            print
            print 'Enter move (%s\'q\' to quit) >>' % options_string,
            selection = raw_input()
            if selection in menu_commands:
                return selection
            try:
                return moves[int(selection) - 1]
            except Exception:
                print
                print 'INVALID INPUT'
                print
