from . import state_engine
import pygame as pg
import score
from map import Map


key_dict = {
    pg.K_a: "A",
    pg.K_b: "B",
    pg.K_c: "C",
    pg.K_d: "D",
    pg.K_e: "E",
    pg.K_f: "F",
    pg.K_g: "G",
    pg.K_h: "H",
    pg.K_i: "I",
    pg.K_j: "J",
    pg.K_k: "K",
    pg.K_l: "L",
    pg.K_m: "M",
    pg.K_n: "N",
    pg.K_o: "O",
    pg.K_p: "P",
    pg.K_q: "Q",
    pg.K_r: "R",
    pg.K_s: "S",
    pg.K_t: "T",
    pg.K_u: "U",
    pg.K_v: "V",
    pg.K_w: "W",
    pg.K_x: "X",
    pg.K_y: "Y",
    pg.K_z: "Z",
}


class AddScore(state_engine.GameState):
    """
    The state to add a new best score.
    """
    def __init__(self):
        """
        @rtype: None
        """
        state_engine.GameState.__init__(self)
        self.add_score_map = Map()

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
                self.persist["MAP"] = self.add_score_map
                self.done = True

            elif event.key in key_dict.keys():
                if len(self.best_score.pseudo) < 3:
                    self.best_score.pseudo += key_dict[event.key]

            elif event.key == pg.K_BACKSPACE:
                self.best_score.pseudo = self.best_score.pseudo[:-1]

            elif event.key == pg.K_RETURN:
                if len(self.best_score.pseudo) == 3:
                    score.ScoreManager().add_score(self.best_score, self.best_score_pos)
                    self.next_state = "MAIN_MENU"
                    self.persist["MAP"] = self.add_score_map
                    self.done = True

    def update(self):
        """
        Update the state.
        @rtype: None
        """
        self.add_score_map.update(5)

    def startup(self, persistent):
        """
        Called when a state resumes being active.
        @param persistent: a dict passed from state to state
        @type persistent: dict{}
        @rtype: None
        """
        self.persist = persistent
        if "MAP" in self.persist:
            self.add_score_map = self.persist["MAP"]
        self.best_score = persistent["score"]
        self.best_score_pos = persistent["pos"]

    def draw(self, surface):
        """
        Draw everything to the screen.
        @param surface: The surface that will be displayed.
        @type surface: pygame.Surface
        @rtype: None
        """
        width, height = surface.get_size()

        self.add_score_map.display(surface)
        text_color = 0, 0, 0

        text = self.font.render("GAME_OVER", 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2))

        text = self.font.render("Nouveau meilleur score !!! -> QUEL EST VOTRE PSEUDO ???", 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2 + 24))

        text = self.font.render(self.best_score.pseudo + "_"*(3 - len(self.best_score.pseudo)), 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2 + 48))

