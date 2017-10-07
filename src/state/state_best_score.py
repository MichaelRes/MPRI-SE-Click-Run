from state_engine import GameState
import pygame as pg


class BestScore(GameState):

    def __init__(self):
        GameState.__init__(self)
        with open("best_score", 'r') as f:
            self.score_data = [l.strip().split() for l in f]

    def startup(self, persistent):
        pass

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "MAIN_MENU"
                self.done = True

    def update(self, dt):
        pass

    def draw(self, surface):
        width, height = surface.get_size()

        surface.fill(pg.Color("black"))
        for i, score in enumerate(self.score_data):
            text_color = 255, 255, 255

            text = self.font.render(score[0] + " " + score[1], 1, text_color)
            width_text, _ = text.get_size()
            surface.blit(text, ((width - width_text)/ 2, i*50))
        pg.display.flip()
