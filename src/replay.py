from enum import Enum
import pickle

class ReplayMode(Enum):
    WRITE = 1
    READ = 2


class Replay:
    """
    A class for replay.
    """
    def __init__(self, path= None):
        """
        If path isn't None, the replay should load the corresponding file.
        Otherwise, the instance goes write mode on a new file
        """
        if self.path != None:
            self.mode = ReplayMode.READ
            self.load(path)
            self.position = 0
        else:
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
        f=open(path, "rb")
        a=pickle.load(f, pickle.HIGHEST_PROTOCOL)
        self.options = a[0]
        self.history = a[1]

    
    def save(self,path):
        """
        write the replay in order to load it later
        """
        assert self.mode == ReplayMode.WRITE, "Wrong Mode for Replay class"
        with open(path, "wb") as f:
            pickle.dump([self.options,self.history], f, pickle.HIGHEST_PROTOCOL)
        
        

            
    def is_empty(self):
        """
        return if this instance has been initialised
        """
        return self.history == []

    def read(self,frame):
        """
        Return what happens at a given frame
        Should happen only in read mode and in sequential order
        """
        assert self.mode == ReplayMode.READ, "Wrong Mode for Replay class"
        while 1:
            if self.position >= 1 + len(self.history) or self.history[self.position][0] > frame:
                return []
            if self.history[self.position][0] == frame:
                return self.history[self.position][1]
            if self.history[self.position][0] < frame:
                i+=1
        
    
    def write(self, events, frame):
        """
        Write to the end of the file what's happening.
        Should happen only in write mode
        """
        assert self.mode == ReplayMode.WRITE, "Wrong Mode for Replay class"
        if self.history != [] and self.history[-1][0] == frame:
            self.history[-1][1] += events
        else:
            self.history.append([frame, events])
