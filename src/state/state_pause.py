from state_engine import GameState
import pygame as pg


class Pause(GameState):

    def __init__(self):
        GameState.__init__(self)
        self.available_state = ["GAME", "MAIN_MENU"]
        self.current_select = 0
        self.next_state = None

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                self.current_select = (self.current_select - 1) % len(self.available_state)
            elif event.key == pg.K_DOWN:
                self.current_select = (self.current_select + 1) % len(self.available_state)
            elif event.key == pg.K_RETURN:
                self.next_state = self.available_state[self.current_select]
                self.done = True

    def draw(self, surface):
        width, height = surface.get_size()

        for i, name_state in enumerate(self.available_state):
            if i == self.current_select:
                text_color = 255, 0, 0
            else:
                text_color = 255, 255, 255
            text = self.font.render(name_state, 1, text_color)
            width_text, _ = text.get_size()
            surface.blit(text, ((width - width_text) / 2, i*100))
        pg.display.flip()
