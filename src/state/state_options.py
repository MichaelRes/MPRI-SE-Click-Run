from state_engine import GameState
import pygame as pg


class Options(GameState):

    def __init__(self):
        GameState.__init__(self)

    def get_event(self, event: pg.event):
        """
        Do something according to the last event that happened
        @param event: the last event that occurred
        """
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                self.next_state = "MAIN_MENU"
                self.done = True

    def draw(self, surface: pg.Surface):
        """
        Draw everything to the screen
        @param surface: The surface that will be displayed.
        """
        width, height = surface.get_size()

        surface.fill(pg.Color("black"))
        text_color = 255, 255, 255

        text = self.font.render("METTRE LES OPTIONS ICI", 1, text_color)
        width_text, height_text = text.get_size()
        surface.blit(text, ((width - width_text) / 2, (height - height_text) / 2))
        pg.display.flip()
