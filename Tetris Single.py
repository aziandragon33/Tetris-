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
class Game()
    Represents an instance of a Tetris game and controls game functionality
"""
class Game():
    def __init__(self):
        self.tetronimos = []
        self.speed = 1
        
        
"""
class Block(pg.sprite.Sprite)
    Represents a single block which will make up one of four blocks of
    each tetronimo. Inheriting from the pygame sprite class.
"""
class Block(pg.sprite.Sprite):
    def __init__(self, image_name):
        pg.sprite.Sprite.__init__(self)  
        self.image, self.rect = load_image(image_name, -1, .25)
      
        
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
        self.origin = [self.w * 1.5, self.w * 1.5]
                
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
        self.rotate = False
        
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
        self.moving_down = False
        
    """Moves blocks left"""
    def _mv_left(self):
        i = 0
        for i in range(0, len(self.blocks)):
            self.blocks[i].rect.move_ip(-self.w, 0)
        self.moving_left = False
        
    """Moves blocks right"""
    def _mv_right(self):
        i = 0
        for i in range(0, len(self.blocks)):
            self.blocks[i].rect.move_ip(self.w, 0)
        self.moving_right = False
        
    """Rotates block 90 degrees"""
    def _rotate(self):     
        rotate = pg.transform.rotate
        i = 0
        for i in range(0, len(self.blocks)):        
            self.blocks[i].image = rotate(self.blocks[i].image, -90)
            current = self.blocks[i].rect.center #current position

            self.blocks[i].rect.center = (-current[1] + self.origin[1] + self.origin[0], current[0] - self.origin[0] + self.origin[1])
        # math from rotation matrix from offpoint center. Move center to be new origin then rotate
        # x2 = -y1 + py + px
        # y2 = x1- px + py
        
        self.rotate = False
        
"""
class RhodeIslandZ(Tetronimo)
    Tetromino for the green Z shape
"""
class RhodeIslandZ(Tetronimo):
    
    def __init__(self):
        Tetronimo.__init__(self, "green.png")
        
        """Not best solution"""
        # for b in self.blocks:
        #     b.image, b.rect = load_image("green.png", -1, .25) #MUST BE 64x64
        
        # self.image, self.rect = load_image("singleblock.png", -1, .25)
        
        self.a.rect.center = (self.w*.5, self.w*1.5)
        self.b.rect.center = (self.w*1.5, self.w*1.5)
        self.c.rect.center = (self.w*1.5, self.w*.5)
        self.d.rect.center = (self.w*2.5, self.w*.5)

def main():
    pg.init()
    
    # Initialize Screen
    screen = pg.display.set_mode((1280,900))
    
    # Make Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((0, 0, 0))
    
    # Create Text on Background
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("Tetris by Daniel", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)
        
    # Draw Board
    width = screen.get_width()
    height = screen.get_height()
    
    left_margin = width*.25
    right_margin = width*.75
    top_margin = height*.1
    bottom_margin = height*.9


    
    # Border of game
    pg.draw.lines(background, (0,255,0), True, ((left_margin, top_margin), (left_margin, bottom_margin), (right_margin, bottom_margin), (right_margin, top_margin)))

    # Grid
    # for i in range(0,11):
    #     pg.draw.line(background, (255,255,255), (width*i/10, 0), (width*i/10, height))
    
    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()
    
    # Prepare Game Objects
    r = RhodeIslandZ()
    """Need to add rendering for each Block per tetronimo"""
    allsprites = pg.sprite.RenderPlain(r.a,r.b,r.c,r.d)   
    clock = pg.time.Clock() 
    
    # Main Loop
    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN and event.key == pg.K_q:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
                r.moving_up = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
                r.moving_down = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_LEFT:
                r.moving_left = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_RIGHT:
                r.moving_right = True
            elif event.type == pg.KEYDOWN and event.key == pg.K_z:
                r.rotate = True
            
                 
        allsprites.update()
        r.update()
                
        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.draw.circle(screen, "red", (r.origin), 5)
        pg.display.flip()
            
    pg.quit() 
    

if __name__ == "__main__":
    main()