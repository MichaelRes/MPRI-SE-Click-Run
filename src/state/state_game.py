class StateGame(GameState):
    """
    Main state for the game
    """
    def _init__(self):
        GameState.__init__(self)
        
    def startup(self,persistent):
        GameState.startup(self,persistent)

    def get_event(self,event):
        GameState.get_event(self,event)

    def draw(self,surface):
        GameState.draw(self,surface)
