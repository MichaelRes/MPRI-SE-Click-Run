class MainMenu(GameState):
    def __init__(self):
        super(GameState, self).__init__()
        self.available_state = ["START_GAME", "BEST_SCORE", "OPTIONS", "CREDITS"]
        self.current_select = 0
        self.next_state = None

    def startup(self, persistent):
        pass

    def get_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass