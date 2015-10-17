'''
Pygame code here
'''
import sys
import pygame
from pygame.locals import QUIT

from engine import SabioData
from utils import ImageSprite, BaseHelperClass, ScreenBaseClass, CURSOR, COLORS

import consts


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
            selected_character = consts.BOY
        else:
            selected_character = consts.GIRL

        level = LevelSelectionScreen(self.screen)
        self.menu_items.empty()
        level.run()

        return True


    def run(self):
        '''runs the screen'''
        self.set_background()
        label = ImageSprite(consts.CHARACTER_SPRITES['label'])
        self.screen.blit(label.image, self.translate_percent_centered(50, 20, label.rect))

        boy = ImageSprite(consts.CHARACTER_SPRITES['boy'], name='boy')
        self.menu_items.add(boy)
        boy.rect.left, boy.rect.top = self.translate_percent_centered(30, 55, boy.rect)
        self.screen.blit(boy.image, boy.rect)

        girl = ImageSprite(consts.CHARACTER_SPRITES['girl'], name='girl')
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
        self.text_font = pygame.font.Font(consts.FONT_PATH, 40)
        self.small_font = pygame.font.Font(consts.FONT_PATH, 24)
        self.selected_character = selected_character

    def level_finished_message(self, message):
        surface = self.show_text_rect(message,
                                      self.small_font, (500, 300),
                                      self.translate_percent(13, 30),
                                      COLORS['grey'], COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=COLORS['yellow'],
                                      parent_alpha=191)
        pygame.display.update()
        pygame.time.wait(consts.GAME_OVER_TIME)
        return LevelSelectionScreen(self.screen).run()

    def click_callback(self, sprite):
        rect = sprite.rect
        pos = (rect.left, rect.top)
        self.menu_items.empty()
        if sprite.name == str(self.current_question.get('respuesta')):
            #respuesta correcta, registramos puntaje
            self.data.win()
            #se muestra un check
            checkbox = ImageSprite(consts.SABIO_SPRITES['checkbox_checked'], pos)
            self.update_score()
            if self.data.has_won():
                self.level_finished_message(consts.WIN_MESSAGE)
        else:
            self.data.loss()
            self.render_lives()
            if self.data.game_over():
                self.level_finished_message(consts.GAME_OVER_MESSAGE)
            else:
                checkbox = ImageSprite(consts.SABIO_SPRITES['checkbox_bad'], pos)

        self.screen.blit(checkbox.image, checkbox.rect)
        pygame.display.update(rect)
        #esperar un round
        pygame.time.wait(1000)
        #mostrar otra pregunta
        self.next_question()

    def render_lives(self, num=None):
        sprite_name = "%s_life" % self.selected_character
        super(SabioScreen, self).render_lives(consts.SABIO_SPRITES[sprite_name], num)

    def run(self):
        self.set_background()

        book = ImageSprite(consts.SABIO_SPRITES['book'])
        self.screen.blit(book.image, self.translate_percent(2, 2))

        owl = ImageSprite(consts.SABIO_SPRITES['owl'])
        self.screen.blit(owl.image, self.translate_percent_centered(65, 33, book.rect))

        character = ImageSprite(consts.SABIO_SPRITES[self.selected_character])
        self.screen.blit(character.image,
                         self.translate_percent_centered(15, 83,
                                                         character.rect))

        #displaying score
        self.update_score()

        #diplaying Vidas text
        self.show_text(str('VIDAS'), self.text_font,
                       self.translate_percent(87, 2),
                       COLORS['white'])
        self.render_lives()

        self.next_question()
        #pygame.display.update()

    def next_question(self):
        self.current_question = self.data.get_random_question()
        self.display_reading(self.current_question.get('lectura', ''))

    def display_reading(self, reading):
        surface = self.show_text_rect(reading,
                                      self.small_font, (500, 300),
                                      self.translate_percent(13, 30),
                                      COLORS['grey'], COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=COLORS['yellow'],
                                      parent_alpha=191)
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
                                      COLORS['grey'], COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=COLORS['yellow'],
                                      parent_alpha=191)
        #agregar sprites de opcion de menu
        pos = self.translate_percent(20, 40)
        for i, option in enumerate(self.current_question.get('opciones')):
            checkbox = ImageSprite(consts.SABIO_SPRITES['checkbox'], pos, name=str(i))
            self.menu_items.add(checkbox)
            self.screen.blit(checkbox.image, checkbox.rect)
            text_pos = (pos[0]+40, pos[1]-3)

            #separamos texto largote
            if len(option) > consts.MAX_QUESTION_CHARS:
                lines = []
                new_option = ''
                tmp_len = len(new_option)
                for word in option.split(' '):
                    tmp_len = len(new_option)
                    if (tmp_len + len(word) + 1) < consts.MAX_QUESTION_CHARS:
                        new_option += ' ' + word
                    else:
                        lines.append(new_option)
                        new_option = word
                lines.append(new_option)

                for line in lines:
                    self.show_text(line, self.small_font, text_pos, COLORS['grey'])
                    pos = (pos[0], pos[1] + 30)
                    text_pos = (pos[0]+40, pos[1]-3)
            else:
                self.show_text(option, self.small_font, text_pos, COLORS['grey'])
                pos = (pos[0], pos[1] + 60)

        pygame.display.update()

        self.detect_click()


class LevelSelectionScreen(ScreenBaseClass):
    background_src = 'assets/img/backgrounds/sabio.png'
    menu_items = pygame.sprite.Group()

    def run(self):
        '''runs the screen'''
        self.set_background()
        mundos = ImageSprite(consts.START_SPRITES['mundos'])
        self.screen.blit(mundos.image, self.translate_percent_centered(50, 20, mundos.rect))
        #TODO: get this list from saved game data
        for i, s in enumerate(['lamp', 'book_locked', 'feather_locked', 'cloud_locked']):
            sprite = ImageSprite(consts.START_SPRITES.get(s), name=s)
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
            self.menu_items.empty()
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
        '''Runs the main game'''
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
