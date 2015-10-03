import sys
import pygame
from pygame.locals import QUIT

OLPC_SCREEN_SIZE = (1200, 900)
WHITE = (255, 255, 255)

get_sprite_path = lambda x, y: 'assets/img/sprites/%s/%s' % (x, y)

START_SPRITES = {
    'book': get_sprite_path('start', 'book.png'),
    'book_locked': get_sprite_path('start', 'book-locked.png'),
    'cloud': get_sprite_path('start', 'cloud.png'),
    'cloud_locked': get_sprite_path('start', 'cloud-locked.png'),
    'lamp': get_sprite_path('start', 'lamp.png'),
    'lamp_locked': get_sprite_path('start', 'lamp-locked.png'),
    'feather': get_sprite_path('start', 'feather.png'),
    'feather_locked': get_sprite_path('start', 'feather-locked.png'),
    'mundos': get_sprite_path('start', 'mundos.png'),
}


class ImageSprite(pygame.sprite.Sprite):
    '''Class to create a background image'''

    def __init__(self, image_file, location=(0,0), name=None):
        '''
            image_file: filepath for the image
            location: tuple of x y coordinates
        '''
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.name = name
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class BaseHelperClass(object):
    '''
    Helper class to locate objects on the screen based on percentage
    need to improve the name of this
    '''
    width, height = OLPC_SCREEN_SIZE

    def translate_percent(self, w, h):
        '''translates percentages to screen positions'''
        x = (w / 100) * self.width
        y = (h / 100) * self.height
        return x, y

    def translate_percent_centered(self, w, h, rect):
        '''
        translates percentages to screen positions
        using the sprite center as point instead of top corner
        '''
        x, y = self.translate_percent(w, h)
        x = x - (rect.width/2)
        y = y - (rect.height/2)
        return x, y

class StartScreen(BaseHelperClass):
    background = 'assets/img/backgrounds/mundo1.png'
    menu_items = pygame.sprite.Group()


    def __init__(self, screen):
        self.screen = screen


    def run(self):
        '''runs the screen'''
        background = ImageSprite(self.background)
        self.screen.blit(background.image, background.rect)
        mundos = ImageSprite(START_SPRITES['mundos'])
        self.screen.blit(mundos.image, self.translate_percent_centered(50, 20, mundos.rect))
        #TODO: get this list from saved game data
        for i, s in enumerate(['lamp', 'book_locked', 'feather_locked', 'cloud_locked']):
            sprite = ImageSprite(START_SPRITES.get(s), name=s)
            self.menu_items.add(sprite)

            #to calculate evenly percentages, 20, 40, 60, 80
            position = 20 * (i + 1)
            sprite.rect.left, sprite.rect.top = self.translate_percent_centered(position, 45, sprite.rect)
            self.screen.blit(sprite.image, sprite.rect)

        pygame.display.update()

        #click detection
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in self.menu_items if s.rect.collidepoint(pos)]
                    for s in clicked_sprites:
                        if s.name.endswith('_locked'):
                            #TODO: mostrar mensaje de que no se puede?
                            continue
                        else:
                            #cargamos nuevo nivel
                            print("Cargamos nuevo nivel")
                            break



class MainClass(BaseHelperClass):
    '''Main Class that starts the game'''

    def __init__(self):
        '''Start screen init'''
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Genios')
        pygame.display.update()

    def start_screen(self):
        start = StartScreen(self.screen)
        start.run()

    def main(self):
        '''Runs main loop and stuff'''

        self.start_screen()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()


if __name__ == '__main__':
    start = MainClass()
    start.main()
