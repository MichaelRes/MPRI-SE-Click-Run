from state_engine import GameState
import pygame as pg
import sys
sys.path.append("..")
import score


key_dict = {
    pg.K_a: "A",
    pg.K_b: "B",
    pg.K_c: "C",
}

class AddScore(GameState):
    """
    The state for the game over.
    """
    def __init__(self) -> None:
        GameState.__init__(self)

    def get_event(self, event: pg.event) -> None:
        """
        Do something according to the last event that happened.
        @param event: the last event that occurred.
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "MAIN_MENU"
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
                    self.done = True

    def startup(self, persistent: {}) -> None:
        """
        Called when a state resumes being active.
        @param persistent: a dict passed from state to state
        """
        self.best_score = persistent["score"]
        self.best_score_pos = persistent["pos"]

    def draw(self, surface: pg.Surface) -> None:
        """
        Draw everything to the screen.
        @param surface: The surface that will be displayed.
        """
        width, height = surface.get_size()

        surface.fill(pg.Color("black"))
        text_color = 255, 255, 255

        text = self.font.render("GAME_OVER", 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2))

        text = self.font.render("Nouveau meilleur score !!! -> QUEL EST VOTRE PSEUDO ???", 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2 + 24))

        text = self.font.render(self.best_score.pseudo + "_"*(3 - len(self.best_score.pseudo)), 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2 + 48))

        pg.display.flip()