import os
import pygame as pg

# Makes path to folder in D:/danie/OneDrive/Desktop/data)
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

"""
def load_image(name, colorkey = None, scale = 1)
    Loads a block image and creates a pg.rect to match size. Can be scaled with
    the 'scale' variable

Inputs:
    name = name of image
    colorkey = key of color in image that is made transparent. Default: -1 
    chooses pixel at (0,0) 
    scale = scales the image size. Default: 1
Returns:
    (pygame image, rectangle on pygame image)
"""
def load_image(name, colorkey = None, scale = 1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    image = image.convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()



        
        
"""
class Block(pg.sprite.Sprite)
    Represents a single block which will make up one of four blocks of
    each tetronimo. Inheriting from the pygame sprite class.
"""
class Block(pg.sprite.Sprite):
    def __init__(self, image_name):
        pg.sprite.Sprite.__init__(self)  
        self.image, self.rect = load_image(image_name, -1, .5)
    
    def get_coords(self):
        return([list(self.rect.topleft), list(self.rect.topright), list(self.rect.bottomleft), list(self.rect.bottomright)])
      
        
"""
class Tetronimo()
    Parent class for each tetronimo. Contains the Blocks() that make up each
    tetronimo, movement, and rotation
"""
class Tetronimo():
    def __init__(self, image_name):
        self.a, self.b, self.c, self.d = Block(image_name), Block(image_name), Block(image_name), Block(image_name)
        self.blocks = [self.a, self.b, self.c, self.d]
        
        self.w = self.a.rect.width #int
                
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.rotate = False
        
    """Getter for block width"""
    def get_width(self):
        return (self.w)
        
    """Updates origin based on which direction user is moving block"""
    def _update_origin(self):
        if self.moving_up:
            self.origin[1] -= self.w
        elif self.moving_down:
            self.origin[1] += self.w
        elif self.moving_left:
            self.origin[0] -= self.w
        elif self.moving_right:
            self.origin[0] += self.w
        # print("Origin:", self.origin[0], self.origin[1])
    
    """Updates tetronimo based on keypress"""
    def update(self):
        self._update_origin()
        if self.moving_up:
            self._mv_up()
        elif self.moving_down:
            self._mv_down()
        elif self.moving_left:
            self._mv_left()
        elif self.moving_right:
            self._mv_right()
        elif self.rotate:
            self._rotate()
    
    """Moves blocks up"""
    def _mv_up(self):
        i = 0
        for i in range(0, len(self.blocks)):
            self.blocks[i].rect.move_ip(0, -self.w)
        self.moving_up = False
        
    """Moves blocks down"""
    def _mv_down(self):
        i = 0
        for i in range(0, len(self.blocks)):
            self.blocks[i].rect.move_ip(0, self.w)
        
    """Moves blocks left"""
    def _mv_left(self):
        i = 0
        for i in range(0, len(self.blocks)):
            self.blocks[i].rect.move_ip(-self.w, 0)
        
    """Moves blocks right"""
    def _mv_right(self):
        i = 0
        for i in range(0, len(self.blocks)):
            self.blocks[i].rect.move_ip(self.w, 0)
        
    """Rotates block 90 degrees"""
    def _rotate(self):     
        rotate = pg.transform.rotate
        i = 0
        for i in range(0, len(self.blocks)):        
            self.blocks[i].image = rotate(self.blocks[i].image, -90)
            current = self.blocks[i].rect.center #current position

            self.blocks[i].rect.center = (-current[1] + self.origin[1] + self.origin[0], current[0] - self.origin[0] + self.origin[1])
        # math from rotation matrix from offpoint center. Move center to be new origin then rotate
        # border_r = -border_t + py + px
        # border_b = border_l- px + py
        
        self.rotate = False
        self.check_rotate
        
    """Checks if rotate will push tetronimo outside of the border"""
    def check_rotate(self):
        return False
        
    
    """Border = [l,r,t,b]"""
    def check_move(self, direction, size, border = []):
        cords_a = self.a.get_coords()
        cords_d = self.d.get_coords()
        match direction:
            case "r":
                for i in range(0,4):
                    if cords_a[i][0] + size > border[1] or cords_d[i][0] + size > border[1]:
                       return False 
                return True
           
            case "l":
                for i in range(0,4):
                    if cords_a[i][0] - size < border[0] or cords_d[i][0] - size < border[0]:
                       return False 
                return True
            
            #not bottom border but first lbock
            case "d":
                for i in range(0,4):
                    if cords_a[i][1] + size > border[3] or cords_d[i][1] + size > border[3]:
                       return False 
                return True
            
        
    def _removeBlock(self, block):
        #remove block from tetronimo. Question is how to keep track of all tetronimos and pick blocks
        return 0
     
    
"""
class RhodeIslandZ(Tetronimo)
    Tetromino for the green Z shape
"""
class RhodeIslandZ(Tetronimo):
    
    def __init__(self, start = [0,0]):
        Tetronimo.__init__(self, "green.png")
        
        self.a.rect.center = (self.w * .5 + start[0], self.w * 1.5 + start[1])
        self.b.rect.center = (self.w * 1.5 + start[0], self.w * 1.5 + start[1])
        self.c.rect.center = (self.w * 1.5 + start[0], self.w * .5 + start[1])
        self.d.rect.center = (self.w * 2.5 + start[0], self.w * .5 + start[1])
        
        self.origin = [self.w * 1.5 + start[0], self.w * 1.5 + start[1]]
        
        
"""
class Game()
    Represents an instance of a Tetris game and controls game functionality
"""
class Game():
    def __init__(self):
        self.tetronimos = []
        self.speed = 1
        self.border = []
        self.current_t = None
        
    def add(self, tetroid, loc = [0,0]):
        match tetroid:
            case RhodeIslandZ:
                self.tetronimos.append(RhodeIslandZ(loc))
                self.current_t = self.tetronimos[-1]
            
            case _:
                print("Error invalid Tetronimo input to Game.add()")
                
    
def main():
    pg.init() #Game?
    game = Game()
    
    # Initialize Screen
    screen = pg.display.set_mode((1280,800)) #Game?
    
    # Make Background
    background = pg.Surface(screen.get_size()) #Game?
    background = background.convert()
    background.fill((0, 0, 0))
    
    # Create Text on Background
    # if pg.font:
    #     font = pg.font.Font(None, 64)
    #     text = font.render("Tetris by Daniel", True, (255, 10, 10))
    #     textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
    #     background.blit(text, textpos)
        
    
    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()
    
    # Create Test Block for Sizing of Border 
    reference_block = Block()
    """Need to add rendering for each Block per tetronimo"""
    
    #### Draw Board 
    block_width = reference_block.get_width()
    board_width = 10 * block_width
    screen_width = screen.get_width()
    
    # Game Area border_l: integer representing the x value of the left border
    border_l = (screen_width - board_width) / 2 
    border_r = border_l + board_width
    border_t = block_width * 3
    border_b = border_t + block_width * 20
    
    # Border of game
    pg.draw.lines(background, (0,255,0), True, ((border_l,border_t), (border_r, border_t), (border_r, border_b), (border_l, border_b)))
    
    # Draw Grid
    for i in range(0,20):
        pg.draw.line(background, (0,255,0), (border_l ,border_t+(block_width*i)), (border_r, border_t+(block_width*i)))
        
    for i in range(0,10):
        pg.draw.line(background, (0,255,0), (border_l+(block_width*i) ,border_t), (border_l+(block_width*i), border_b))
    
                                                                                                                                 
    # Spawn blocks always here
    game.add("RhodeIslandZ", [border_l+(block_width*3), border_t])
    r = RhodeIslandZ([border_l+(block_width*3), border_t])
    # active_tetronimo = r
    
    # Render and Create Clock
    allsprites = pg.sprite.RenderPlain(r.a,r.b,r.c,r.d)   #Game?
    clock = pg.time.Clock()  #Game?
    
    # Main Loop
    going = True
    while going:
        clock.tick(20)

        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_q:
                going = False
                
            elif event.type == pg.KEYDOWN and event.key == pg.K_z:
                game.current_t.rotate = True
                    
        keys = pg.key.get_pressed()
        game.moving_right = keys[pg.K_RIGHT] and game.current_t.check_move("r", block_width, [border_l,border_r,border_t,border_b])
        game.current_t.moving_left = keys[pg.K_LEFT] and game.current_t.check_move("l", block_width, [border_l,border_r,border_t,border_b])
        game.current_t.moving_down = keys[pg.K_DOWN] and game.current_t.check_move("d", block_width, [border_l,border_r,border_t,border_b])
        game.current_t.moving_up = keys[pg.K_UP]

            
                 
        allsprites.update()
        game.current_t.update()
        
        game.current_t.moving_up = False
        game.current_t.moving_down = False
        game.current_t.moving_left = False
        game.current_t.moving_right = False
                
        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.draw.circle(screen, "red", (r.origin), 5)
        pg.display.flip()
            
    pg.quit() 
    

if __name__ == "__main__":
    main()