class Entity:
    """
    The class for the entity in the game.
    """

    def __init__(self, x0, y0, hitbox):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        self.pos_x = x0
        self.pos_y = y0
        self.hitbox = hitbox

    def collide(self, other):
        return self.pos_x + self.hitbox[0] >= other.pos_x and self.pos_x <= other.pos_x + other.hitbox[0] and \
            self.pos_y + self.hitbox[1] >= other.pos_y and self.pos_y <= other.pos_y + other.hitbox[1]


class MovingEntity(Entity):
    """
    The class for a moving entity in the game
    """

    def __init__(self, x0, y0, vx0, vy0, hitbox):
        """
        @param x0: The x-axis position of the entity.
        @type x0: int
        @param y0: The y-axis position of the entity.
        @type y0: int
        @param vx0: The speed of the entity on the x-axis.
        @type vx0: int
        @param vy0: The speed of the entity on the y-axis.
        @type vy0: int
        @param hitbox: the hitbox of the entity
        @type hitbox: int, int
        """
        Entity.__init__(self, x0, y0, hitbox)
        self.v_x = vx0
        self.v_y = vy0
        self.gravity = 1
