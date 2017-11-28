from enum import Enum

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
            self.load(path)
            self.mode = ReplayMode.READ
        else:
            self.history = []
            self.mode = ReplayMode.WRITE
            
    def set_opts(self, options):
        """
        This should set the variable : difficulty and number of players in order to save them to the replay
        """
        pass
    
    def get_opts(self):
        """
        Give option in read mode
        """
        pass
        
    def load(self,path):
        """
        Should load from some file
        """
        pass
    
    def save(self,path):
        """
        write the replay in order to load it later
        """
        pass
    
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
        pass
    
    def write(self, event, frame):
        """
        Write to the end of the file what's happening.
        Should happen only in write mode
        """
        pass
    
