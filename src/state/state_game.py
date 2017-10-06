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
            #Let's try to make the player jump by modifiying its velocity after checking if it's on the ground
            if event.key==K_SPACE:
                if game_map.on_the_ground(self.player.pos_x,self.player.pos_y,self.player.hitbox):
                    self.player.v_y=max(10,self.player.v_y)


    def update(self):
        Game.update(self)
        
        #Update of the pos
        x0=self.player.pos_x
        (x,y),is_the_game_over=self.game_map.move_test(self.player.pos_x,self.player.pos_y,self.player.hitbox,self.player.v_x,self.player.v_y)
        self.player.pos_x=x
        self.player.pos_y=y

        #Something to do in case the game is over
        if is_the_game_over:
            self.done=True

        #Update depending on whether the player is on the ground or not
        if self.game_map.on_the_ground(self.player.pos_x,self.player.pos_y,self.player.hitbox):
            self.player.action=action.RUNNING
            self.player.v_y=max(self.player.v_y,0)
        else:
            self.player.action=action.JUMPING
            self.player.v_y=max(self.player.v_y+self.acceleration_y,1000)
        #Update of the game_map
        game_map.update(x-x0)

    def draw(self,surface):
        GameState.draw(self,surface)
        game_map.draw()
