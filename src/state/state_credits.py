from state_engine import GameState
import pygame as pg


class Credits(GameState):

    def __init__(self):
        GameState.__init__(self)

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
        text_color = 255, 255, 255

        text = self.font.render("METTRE LES CREDITS ICI", 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text)/ 2, (height - height_text) / 2))
        pg.display.flip()
