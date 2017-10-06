class StateGame(GameState):
    """
    Main state for the game
    """
    def _init__(self):
        GameState.__init__(self)
        self.player=Player(0,0,5,0)
        self.game_map=Map()
        self.acceleration_x=0 #As said, x variables aint of any use at the moment
        self.acceleration_y=2
        
    def startup(self,persistent):
        GameState.startup(self,persistent)

    def get_event(self,event):
        GameState.get_event(self,event)
        if event.type== KEYDOWN:
            if event.key==K_SPACE:
                if game_map.isOnTheGround(self.player.pos_x,self.player.pos_y,self.player.hitbox):
                    self.player.v_y=max(10,self.player.v_y)
                    #Let's try to make the player jump by modifiying its velocity after checking if it's on the ground

    def update(self):
        Game.update(self)
        
        #On met à jour la position en fonction des collisions
        x0=self.player.pos_x
        x,y,is_the_game_over=self.game_map.move(self.player.pos_x,self.player.pos_y,self.player.v_x,self.player.v_y,self.player.hitbox)
        self.player.pos_x=x
        self.player.pos_y=y


        #Update depending on whether the player is on the ground or not
        if self.game_map.isOnTheGround(self.player.pos_x,self.player.pos_y,self.player.hitbox):
            self.player.action=action.RUNNING
            self.player.v_y=max(self.player.v_y,0)
        else:
            self.player.action=action.JUMPING
            self.player.v_y=self.player.v_y+=self.acceleration_y
        
        game_map.update(x-x0)

        return
        

    def draw(self,surface):
        GameState.draw(self,surface)
        game_map.draw()
