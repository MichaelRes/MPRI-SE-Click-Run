from entity import Entity
from ressources import load_image
import bisect


MAX_ITEM_HIT_BOX_W = 100
MAX_ITEM_HIT_BOX_H = 100


class ItemManager:
    def __init__(self):
        self.items = []
        """self.add(SizeUpItem(400, 589, (50, 50)))
        self.add(SizeUpItem(500, 589, (50, 50)))
        self.add(SizeUpItem(600, 200, (50, 50)))
        self.add(SizeUpItem(1300, 200, (50, 50)))"""

    def add(self, item):
        bisect.insort(self.items, item)

    def update(self, dx, player, map):
        self.items = [item.update(dx, map) for item in self.items if not item.collide(player)]

    def display(self, surface, low_x, high_x):
        # TODO Améliorer un peu la vitesse de ce code
        i = 0
        while i < len(self.items):
            if self.items[i].pos_x >= (low_x - MAX_ITEM_HIT_BOX_W) and self.items[i].pos_y <= high_x:
                self.items[i].draw(surface)
            i += 1


class Item(Entity):
    def __init__(self, x0, y0, hitbox, sprite_name):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        Entity.__init__(self, x0, y0, hitbox)
        self.sprite = load_image("item/%s.png" % sprite_name, self.hitbox)

    def draw(self, surface):
        """
        Display the player on the surface.
        @param surface: The surface to display the player on.
        @type surface: pygame.Surface
        @rtype: None
        """
        surface.blit(self.sprite, (self.pos_x, self.pos_y))

    def collide(self, player):
        if Entity.collide(self, player):
            self.effect(player)
            return True

    def effect(self, player):
        raise NotImplementedError

    def update(self, dx, game_map):
        if game_map.display_width * game_map.dim_bloc - dx < self.pos_x < game_map.display_width * game_map.dim_bloc:
            game_map.put_on_the_ground(self)
        self.pos_x -= dx
        return self

    def __lt__(self, other):
        return self.pos_x < other.pos_x


class SizeItem(Item):
    def __init__(self, x0, y0, hitbox, sprite_name, hit_box_change):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        Item.__init__(self, x0, y0, hitbox, sprite_name)
        self.hit_box_change = hit_box_change

    def effect(self, player):
        new_hit_box = (player.hitbox[0] + self.hit_box_change, player.hitbox[1] + self.hit_box_change)
        player.pos_y += (player.hitbox[1] - new_hit_box[1])
        player.switch_hit_box(new_hit_box)


class SizeUpItem(SizeItem):
    def __init__(self, x0, y0, hitbox):
        SizeItem.__init__(self, x0, y0, hitbox, "red_shroom", 20)


class SizeDownItem(SizeItem):
    def __init__(self, x0, y0, hitbox):
        SizeItem.__init__(self, x0, y0, hitbox, "green_shroom", -20)

