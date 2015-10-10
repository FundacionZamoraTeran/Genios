'''
Pygame code here
'''
import sys
import pygame
from pygame.locals import QUIT

from engine import SabioData
from utils import ImageSprite, BaseHelperClass, ScreenBaseClass, CURSOR, COLORS

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

CHARACTER_SPRITES = {
    'boy': get_sprite_path('character', 'boy.png'),
    'girl': get_sprite_path('character', 'girl.png'),
    'label': get_sprite_path('character', 'label.png'),
}

SABIO_SPRITES = {
    'book': get_sprite_path('sabio', 'book.png'),
    'boy': get_sprite_path('sabio', 'boy.png'),
    'boy_life': get_sprite_path('sabio', 'boy-life.png'),
    'girl': get_sprite_path('sabio', 'girl.png'),
    'girl_life': get_sprite_path('sabio', 'girl-life.png'),
    'owl': get_sprite_path('sabio', 'owl.png'),
}

FONT_PATH = 'assets/fonts/PatuaOne-Regular.ttf'

BOY = 'boy'
GIRL = 'girl'

selected_character = None


class CharacterSelectionScreen(ScreenBaseClass):
    '''
    class for character selection screen
    '''
    background_src = 'assets/img/backgrounds/sabio.png'
    menu_items = pygame.sprite.Group()
    selected_character = None

    def click_callback(self, sprite):
        global selected_character
        if sprite.name == 'boy':
            selected_character = BOY
        else:
            selected_character = GIRL

        level = LevelSelectionScreen(self.screen)
        level.run()

        return True


    def run(self):
        '''runs the screen'''
        self.set_background()
        label = ImageSprite(CHARACTER_SPRITES['label'])
        self.screen.blit(label.image, self.translate_percent_centered(50, 20, label.rect))

        boy = ImageSprite(CHARACTER_SPRITES['boy'], name='boy')
        self.menu_items.add(boy)
        boy.rect.left, boy.rect.top = self.translate_percent_centered(30, 55, boy.rect)
        self.screen.blit(boy.image, boy.rect)

        girl = ImageSprite(CHARACTER_SPRITES['girl'], name='girl')
        self.menu_items.add(girl)
        girl.rect.left, girl.rect.top = self.translate_percent_centered(70, 55, girl.rect)
        self.screen.blit(girl.image, girl.rect)

        pygame.display.update()

        self.detect_click()

class SabioScreen(ScreenBaseClass):
    background_src= 'assets/img/backgrounds/sabio.png'
    lives_sprites = pygame.sprite.Group()
    menu_items = pygame.sprite.Group()
    current_question = None
    seconds_per_word = 0.1 #60/20
    initial_time = None
    score_surface = None

    def __init__(self, screen):
        super(SabioScreen, self).__init__(screen)
        self.data = SabioData()
        self.text_font = pygame.font.Font(FONT_PATH, 40)
        self.small_font = pygame.font.Font(FONT_PATH, 24)

    def click_callback(self, sprite):
        pass

    def update_score(self, score):
        pos = self.translate_percent(15, 8)
        if self.score_surface:
            rect = self.score_surface.get_rect()
            rect.left, rect.top = pos
            self.screen.blit(self.background, pos, rect)
            self.score_surface.blit(self.background, self.score_surface.get_rect())

        self.score_surface = self.show_text(str(score), self.text_font,
                                            pos, COLORS['white'])

    def render_lives(self, num=None):
        num = num or self.data.max_lives
        initial_location = self.translate_percent(85, 8)
        sprite_name = "%s_life" % selected_character

        self.lives_sprites.clear(self.screen, self.background)
        self.lives_sprites.empty()

        for x in range(num):
            sprite = ImageSprite(SABIO_SPRITES[sprite_name], initial_location)
            self.lives_sprites.add(sprite)
            initial_location = (initial_location[0] + 55, initial_location[1])

        self.lives_sprites.draw(self.screen)

    def run(self):
        self.set_background()

        book = ImageSprite(SABIO_SPRITES['book'])
        self.screen.blit(book.image, self.translate_percent(2, 2))

        owl = ImageSprite(SABIO_SPRITES['owl'])
        self.screen.blit(owl.image, self.translate_percent_centered(65, 33, book.rect))

        character = ImageSprite(SABIO_SPRITES[selected_character])
        self.screen.blit(character.image,
                         self.translate_percent_centered(15, 83,
                                                         character.rect))

        #displaying score
        self.update_score(self.data.score)

        #diplaying Vidas text
        self.show_text(str('VIDAS'), self.text_font,
                       self.translate_percent(87, 2),
                       COLORS['white'])
        self.render_lives()

        self.current_question = self.data.get_random_question()
        self.display_reading(self.current_question.get('lectura', ''))

        #pygame.display.update()

    def display_reading(self, reading):
        surface = self.show_text_rect(reading,
                                      self.small_font, (500, 300),
                                      self.translate_percent(13, 30),
                                      COLORS['grey'], COLORS['white'], 1)
        pygame.display.update()
        #TODO agregar deteccion de click y boton para siguiente
        words = len(reading.split(' '))
        time_to_wait = int(words * self.seconds_per_word * 1000)
        pygame.time.wait(time_to_wait)
        #display question

        self.display_question(self.current_question.get('pregunta'))

    def display_question(self, question):
        surface = self.show_text_rect(question,
                                      self.small_font, (500, 300),
                                      self.translate_percent(13, 30),
                                      COLORS['grey'], COLORS['white'], 1)
        pygame.display.update()


class LevelSelectionScreen(ScreenBaseClass):
    background_src = 'assets/img/backgrounds/sabio.png'
    menu_items = pygame.sprite.Group()

    def run(self):
        '''runs the screen'''
        self.set_background()
        mundos = ImageSprite(START_SPRITES['mundos'])
        self.screen.blit(mundos.image, self.translate_percent_centered(50, 20, mundos.rect))
        #TODO: get this list from saved game data
        for i, s in enumerate(['lamp', 'book_locked', 'feather_locked', 'cloud_locked']):
            sprite = ImageSprite(START_SPRITES.get(s), name=s)
            self.menu_items.add(sprite)

            #to calculate evenly percentages, 20, 40, 60, 80
            position = 20 * (i + 1)
            sprite.rect.left, sprite.rect.top = \
                    self.translate_percent_centered(position, 45, sprite.rect)
            self.screen.blit(sprite.image, sprite.rect)

        pygame.display.update()

        #click detection
        self.detect_click()

    def click_callback(self, sprite):
        if sprite.name.endswith('_locked'):
            pass
            #TODO: mostrar mensaje de que no se puede?
        else:
            #cargamos nuevo nivel
            SabioScreen(self.screen).run()
            print("Cargamos nuevo nivel")

class MainClass(BaseHelperClass):
    '''Main Class that starts the game'''

    def __init__(self):
        '''Start screen init'''
        pygame.init()
        self.cursor = pygame.cursors.compile(CURSOR)
        pygame.mouse.set_cursor((32,32), (1,1), *self.cursor)
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Genios')
        pygame.display.update()

    def start_screen(self):
        start = CharacterSelectionScreen(self.screen)
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
    MainClass().main()
