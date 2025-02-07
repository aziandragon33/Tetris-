import os
import pygame as pg

# Makes path to folder in D:/danie/OneDrive/Desktop/data)
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

"""
def load_image(name, colorkey = None, scale = 1)

This function loads an image and fits a rectangle to the image based on the 
variables given 

Inputs:
    name; name of image
    colorkey; key of color in image that is made transparent. Default: -1 
    chooses pixel at (0,0) 
    scale; scales the image size. Default: 1
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
This class represents a single block which will make up one of four blocks of
each tetronimo. It is inheriting from the pygame sprite class.

Attributes:
    self.image; pygame.image 
    self.rect; pygame.rect
"""
class Block(pg.sprite.Sprite):
    def __init__(self):
        #Call Sprite initializer
        pg.sprite.Sprite.__init__(self)  
        self.image, self.rect = load_image("singleblock.png", -1, .25)


# Rhode Island Z
class RhodeIslandZ():
    """
    Tetromino for the green shape
    Creates 4 Block() types to create the shape and stores them in self.blocks
    self.w is used to to scale each block's placement when the size is changed
    """
    def __init__(self):
        self.a, self.b, self.c, self.d = Block(), Block(), Block(), Block()
        self.blocks = [self.a, self.b, self.c, self.d]
        self.w = self.a.rect.width #int
        self.center = [0, 0]
        
        self.a.rect.topleft = (0, 0)
        self.b.rect.topleft = (self.w, 0)
        self.c.rect.topleft = (self.w, self.w)
        self.d.rect.topleft = (self.w*2, self.w)
        
        self.moving_up = False
        self.moving_down = False
        self.moving_left = False
        self.moving_right = False
    
    """Updates tetronimo based on keypress"""
    def update(self):
        if self.moving_up:
            self._mv_up()
        elif self.moving_down:
            self._mv_down()
        elif self.moving_left:
            self._mv_left()
        elif self.moving_right:
            self._mv_right()
    
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
            
        

#Lets try and get a screen with an image. Nothing fancy
def main():
    pg.init()
    
    #Initialize Screen
    screen = pg.display.set_mode((1280, 900), pg.SCALED)
    
    # Make Background
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background.fill((170, 238, 187))
    
    #Create Text on Background
    if pg.font:
        font = pg.font.Font(None, 64)
        text = font.render("Tetris by Daniel", True, (10, 10, 10))
        textpos = text.get_rect(centerx=background.get_width() / 2, y=10)
        background.blit(text, textpos)
        
    # Display The Background
    screen.blit(background, (0, 0))
    pg.display.flip()
    
    # Prepare Game Objects
    r = RhodeIslandZ()
    """LOOK HERE"""
    allsprites = pg.sprite.RenderPlain(r.a,r.b,r.c,r.d)   
    clock = pg.time.Clock() 
    
    # Main Loop
    going = True
    while going:
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                going = False
            elif event.type == pg.KEYDOWN and event.key == pg.K_w:
                r.moving_up = True
                print("W")
            elif event.type == pg.KEYDOWN and event.key == pg.K_s:
                r.moving_down = True
                print("S")
            elif event.type == pg.KEYDOWN and event.key == pg.K_a:
                r.moving_left = True
                print("A")
            elif event.type == pg.KEYDOWN and event.key == pg.K_d:
                r.moving_right = True
                print("D")
                 
        allsprites.update()
        r.update()
                
        # Draw Everything
        screen.blit(background, (0, 0))
        allsprites.draw(screen)
        pg.display.flip()
            
    pg.quit()
    #test
    #some more comments
    #more changes!

    

# this calls the 'main' function when this script is executed
if __name__ == "__main__":
    main()
