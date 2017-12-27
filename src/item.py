from entity import Entity
from player import Player


class Item(Entity):
    def __init__(self, x0, y0, hitbox, sprite):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        Entity.__init__(self, x0, y0, hitbox)
        self.sprite = sprite

    def draw(self, surface):
        """
        Display the player on the surface.
        @param surface: The surface to display the player on.
        @type surface: pygame.Surface
        @rtype: None
        """
        surface.blit(self.sprite, (self.pos_x, self.pos_y))


class SizeItem(Item):
    def __init__(self, x0, y0, hitbox, sprite):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        Entity.__init__(self, x0, y0, hitbox, sprite)

    def effect(self, player):

