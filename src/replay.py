from enum import Enum
import pickle


class ReplayMode(Enum):
    WRITE = 1
    READ = 2


class Replay:
    """
    A class for the record used for the replay.
    """
    def __init__(self, seed=None, path=None):
        """
        If path isn't None, the replay should load the corresponding file.
        Otherwise, the instance goes write mode and can be later written on the discs.
        """
        if path is not None:
            self.mode = ReplayMode.READ
            self.load(path)
            self.position = 0
        else:
            self.seed = seed
            self.mode = ReplayMode.WRITE
            self.history = []
            
    def set_opts(self, options):
        """
        This should set the variable : difficulty and number of players in order to save them to the replay
        """
        assert self.mode == ReplayMode.WRITE, "Wrong Mode for Replay class"
        self.options = options
    
    def get_opts(self):
        """
        Give option in read mode
        """
        assert self.mode == ReplayMode.READ, "Wrong Mode for Replay class"
        return self.options
        
    def load(self,path):
        """
        Should load from some file
        """
        assert self.mode == ReplayMode.READ, "Wrong Mode for Replay class"
        with open(path, "rb") as f:
            self.options, self.seed, self.history = pickle.load(f)
    
    def save(self, path):
        """
        write the replay in order to load it later
        """
        assert self.mode == ReplayMode.WRITE, "Wrong Mode for Replay class"
        with open(path, "wb") as f:
            pickle.dump((self.options, self.seed, self.history), f, pickle.HIGHEST_PROTOCOL)

    def is_empty(self):
        """
        return if this instance has been initialised
        """
        return self.history == []

    def read(self, frame):
        """
        Return what happens at a given frame
        Should happen only in read mode and in sequential order
        """
        assert self.mode == ReplayMode.READ, "Wrong Mode for Replay class"
        while True:
            if self.position >= len(self.history) or self.history[self.position][0] > frame:
                return None
            if self.history[self.position][0] == frame:
                return self.history[self.position][1]
            if self.history[self.position][0] < frame:
                self.position += 1

    def write(self, frame, key):
        self.history.append([frame, key])
        
    """def write(self, event, frame):
        
        Write to the end of the file what's happening
        Should happen only in write mode
        
        assert self.mode == ReplayMode.WRITE, "Wrong Mode for Replay class"
        assert self.history == [] or self.history[-1][0] <= frame, "Write should happen in increasing frame number"
        if self.history != [] and self.history[-1][0] == frame:
            self.history[-1][1] += [event]
        else:
            self.history.append([frame, [event]])"""
