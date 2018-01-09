from entity import Entity
from ressources import load_image
import bisect


MAX_ITEM_HIT_BOX_W = 100
MAX_ITEM_HIT_BOX_H = 100

# Max and Min size for the character
MAX_SIZE_CHARACTER = 100
MIN_SIZE_CHARACTER = 20

# Modificator for items
SIZE_MODIFICATOR = 20
SPEED_MODIFICATOR = 0.25
GRAVITY_MODIFICATOR = 0.8


# Time before dying thanks to the poison, needs to be changed in map.py too
POISON_TIME = 300

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
        self.items = [item.update(dx, map) for item in self.items if (not item.collide(player) and item.pos_x + item.hitbox[0] >= 0 ) ]

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


# This item kill, as simple as that
class DeathItem(Item):
    def __init__(self, x0, y0, hitbox):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        Item.__init__(self,x0, y0, hitbox,"flame")
        
    def effect(self,player):
        player.is_dead = True

# The poison
class PoisonItem(Item):
    def __init__(self,x0, y0, hitbox):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        Item.__init__(self,x0, y0, hitbox,"poison")
        
    def effect(self, player):
        if player.poison == -1:
            player.poison = POISON_TIME

# The antidote

class AntidoteItem(Item):
    def __init__(self,x0, y0, hitbox):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        Item.__init__(self,x0, y0, hitbox,"antidote")
        
    def effect(self, player):
        player.poison = -1

# The feather

class FeatherItem(Item):
    def __init__(self,x0, y0, hitbox):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        Item.__init__(self,x0, y0, hitbox,"feather")
        
    def effect(self, player):
        player.gravity = max(0.5,player.gravity*GRAVITY_MODIFICATOR)

# Speed modificators

class SpeedItem(Item):
    def __init__(self, x0, y0, hitbox, sprite_name, speed_change):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        Item.__init__(self, x0, y0, hitbox, sprite_name)
        self.speed_change = speed_change
    def effect(self, player):
        player.mod_difficulty += self.speed_change

class SpeedUpItem(SpeedItem):
    def __init__(self,x0,y0,hitbox):
        SpeedItem.__init__(self,x0,y0,hitbox,"boots1",SPEED_MODIFICATOR)
        
class SpeedDownItem(SpeedItem):
    def __init__(self,x0,y0,hitbox):
        SpeedItem.__init__(self,x0,y0,hitbox,"boots2", -SPEED_MODIFICATOR)
    

    
        
# Size Items
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
        new_hit_box = (min(max(player.hitbox[0] + self.hit_box_change,MIN_SIZE_CHARACTER),MAX_SIZE_CHARACTER),
                       min(max(player.hitbox[1] + self.hit_box_change,MIN_SIZE_CHARACTER),MAX_SIZE_CHARACTER))

        player.pos_y += (player.hitbox[1] - new_hit_box[1])
        player.switch_hit_box(new_hit_box)


class SizeUpItem(SizeItem):
    def __init__(self, x0, y0, hitbox):
        SizeItem.__init__(self, x0, y0, hitbox, "red_shroom", SIZE_MODIFICATOR)


class SizeDownItem(SizeItem):
    def __init__(self, x0, y0, hitbox):
        SizeItem.__init__(self, x0, y0, hitbox, "green_shroom", -SIZE_MODIFICATOR )

