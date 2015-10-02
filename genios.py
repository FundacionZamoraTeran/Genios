import sys
import pygame
from pygame.locals import QUIT

OLPC_SCREEN_SIZE = (1200, 900)
WHITE = (255, 255, 255)

class Background(pygame.sprite.Sprite):
    '''Class to create a background image'''

    def __init__(self, image_file, location):
        '''
            image_file: filepath for the image
            location: tuple of x y coordinates
        '''
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class MainClass(object):
    '''Main Class that starts the game'''
    start_background = 'assets/img/backgrounds/mundo1.png'

    def __init__(self):
        '''Start screen init'''
        pygame.init()
        self.screen = pygame.display.set_mode(OLPC_SCREEN_SIZE)
        pygame.display.set_caption('Genios')

        self.screen.fill(WHITE)
        pygame.display.update()

    def start_screen(self):
        background = Background(self.start_background, (0,0))
        self.screen.blit(background.image, background.rect)
        pygame.display.update()
        #TODO: create levels menu


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
