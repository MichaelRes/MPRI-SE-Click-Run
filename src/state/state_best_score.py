from . import state_engine
import pygame as pg
import sys
sys.path.append("..")
import score
from map import Map

class BestScore(state_engine.GameState):
    """
    The class for the best score state.
    """
    def __init__(self):
        """
        @rtype: None
        """
        state_engine.GameState.__init__(self)

        self.best_score_map = Map(None,None)
        self.current_select = 0

    def get_event(self, event):
        """
        Do something according to the last event that happened.
        @param event: the last event that occurred.
        @type event: pygame.event
        @rtype: None
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "MAIN_MENU"
                self.persist["MAP"] = self.best_score_map
                self.done = True
            elif event.key == pg.K_UP:
                self.current_select = (self.current_select - 1) % len(score.ScoreManager())
            elif event.key == pg.K_DOWN:
                self.current_select = (self.current_select + 1) % len(score.ScoreManager())
            elif event.key == pg.K_RETURN:
                replay_path = score.ScoreManager().instance.scores[self.current_select].get_replay_file()
                self.persist = {"REPLAY_PATH": replay_path}
                self.next_state = "GAME_REPLAY"
                self.done = True

    def update(self):
        """
        Update the state.
        @rtype: None
        """
        self.best_score_map.update(5)

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        @param persistent: a dict passed from state to state
        @type persistent: dict{}
        @rtype: None
        """
        self.persist = persistent
        if "MAP" in self.persist:
            self.best_score_map = self.persist["MAP"]

    def draw(self, surface):
        """
        Draw everything to the screen.
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        width, height = surface.get_size()
        self.best_score_map.display(surface)
        for i, s in enumerate(score.ScoreManager().instance.scores):
            if i == self.current_select:
                text_color = 255, 0, 0
            else:
                text_color = 0, 0, 0
            text = self.font.render(str(i+1) + " " + s.pseudo + " " + str(s.score), 1, text_color)
            width_text, _ = text.get_size()
            surface.blit(text, ((width - width_text) / 2, (24 * (i + 1)) + 100))
