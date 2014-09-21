import os


class FileStore(object):
    """
    Solutions to games are persistently stored to file
    """
    _DEFAULT_STORAGE_PATH = 'game_data/'

    def __init__(self, game_id):
        """
        Load the Solution
        """
        self.storage_path = self._DEFAULT_STORAGE_PATH
        self.file_path = self.storage_path + str(game_id) + '.db'
        if os.path.exists(self.file_path):
            self.load()
        else:
            self.values = {}

    def get_value(self, game_logic):
        """
        Get the value of the current position in the game logic
        """
        hash = game_logic.hash()
        if hash in self.values:
            return self.values[hash]
        else:
            value = game_logic.get_value()
            if value:
                self.values[hash] = value
            return value

    def set_value(self, game_logic, value):
        """
        Set the value of the current position in the game logic
        """
        self.values[game_logic.hash()] = value

    def store(self):
        """
        Store the solved data
        """
        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)
        if not os.path.exists(self.file_path):
            with open(self.file_path, 'w') as f:
                for key, value in self.values.items():
                    f.write('%s:%s\n' % (key, value))

    def load(self):
        self.values = {}
        with open(self.file_path, 'r') as f:
            for line in f:
                key, value = line.strip().split(':')
                self.values[int(key)] = int(value)
