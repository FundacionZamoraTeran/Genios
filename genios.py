'''
Pygame code here
'''
import sys
import pygame
from pygame.locals import QUIT

from engine import SabioData, PoetaData
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

class PoetaScreen(ScreenBaseClass):
    background_src= 'assets/img/backgrounds/poeta.png'
    seconds_per_word = 0.1 #60/20
    box_size = (750, 350)
    max_question_chars = 50

    def __init__(self, screen):
        super(PoetaScreen, self).__init__(screen)
        self.data = PoetaData()
        self.text_font = pygame.font.Font(consts.FONT_PATH, 40)
        self.small_font = pygame.font.Font(consts.FONT_PATH, 24)
        self.selected_character = selected_character
        self.box_pos = self.translate_percent(25, 30)

    def click_callback(self, sprite):
        rect = sprite.rect
        pos = (rect.left, rect.top)
        self.menu_items.empty()
        if sprite.name == str(self.current_question.get('respuesta')):
            #respuesta correcta, registramos puntaje
            self.data.win()
            #se muestra un check
            checkbox = ImageSprite(consts.POETA_SPRITES['checkbox_checked'], pos)
            self.update_score()
            if self.data.has_won():
                self.level_finished_message(consts.WIN_MESSAGE, LevelSelectionScreen)
        else:
            self.data.loss()
            self.render_lives()
            if self.data.game_over():
                self.level_finished_message(consts.GAME_OVER_MESSAGE, LevelSelectionScreen)
            else:
                checkbox = ImageSprite(consts.POETA_SPRITES['checkbox_bad'], pos)

        self.screen.blit(checkbox.image, checkbox.rect)
        pygame.display.update(rect)
        #esperar un round
        pygame.time.wait(1000)
        #mostrar otra pregunta
        self.next_question()



    def render_lives(self, num=None):
        sprite_name = "%s_life" % self.selected_character
        super(PoetaScreen, self).render_lives(consts.POETA_SPRITES[sprite_name], num)

    def run(self):
        self.set_background()

        icon = ImageSprite(consts.POETA_SPRITES['icon'])
        self.screen.blit(icon.image, self.translate_percent(2, 2))

        #owl = ImageSprite(consts.POETA_SPRITES['owl'])
        #self.screen.blit(owl.image, self.translate_percent_centered(65, 33, icon.rect))

        character = ImageSprite(consts.POETA_SPRITES[self.selected_character])
        self.screen.blit(character.image,
                         self.translate_percent_centered(15, 83,
                                                         character.rect))

        #displaying score
        self.update_score()

        #diplaying Vidas text
        self.show_lives_text()
        self.render_lives()

        self.next_question()
        #pygame.display.update()

    def display_reading(self, reading):
        surface = self.show_text_rect(reading,
                                      self.small_font, self.box_size,
                                      self.box_pos,
                                      COLORS['grey'], COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=COLORS['yellow'],
                                      parent_alpha=191)
        pygame.display.update()
        #TODO agregar deteccion de click y boton para siguiente
        words = len(reading.split(' '))
        time_to_wait = int(words * self.seconds_per_word * 1000)
        time_to_wait = 2000
        pygame.time.wait(time_to_wait)
        #display question

        self.display_question(self.current_question.get('pregunta'))

    def display_question(self, question):
        surface = self.show_text_rect(question,
                                      self.small_font, self.box_size,
                                      self.box_pos,
                                      COLORS['grey'], COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=COLORS['yellow'],
                                      parent_alpha=191)
        #agregar sprites de opcion de menu
        pos = self.translate_percent(30, 40)
        for i, option in enumerate(self.current_question.get('opciones')):
            checkbox = ImageSprite(consts.POETA_SPRITES['checkbox'], pos, name=str(i))
            self.menu_items.add(checkbox)
            self.screen.blit(checkbox.image, checkbox.rect)
            text_pos = (pos[0]+40, pos[1]-3)

            #separamos texto largote
            if len(option) > self.max_question_chars:
                lines = []
                new_option = ''
                tmp_len = len(new_option)
                for word in option.split(' '):
                    tmp_len = len(new_option)
                    if (tmp_len + len(word) + 1) < self.max_question_chars:
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


class SabioScreen(ScreenBaseClass):
    background_src= 'assets/img/backgrounds/sabio.png'
    seconds_per_word = 0.1 #60/20
    box_size = (500, 300)

    def __init__(self, screen):
        super(SabioScreen, self).__init__(screen)
        self.data = SabioData()
        self.text_font = pygame.font.Font(consts.FONT_PATH, 40)
        self.small_font = pygame.font.Font(consts.FONT_PATH, 24)
        self.selected_character = selected_character
        self.box_pos = self.translate_percent(13, 30)

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
                self.level_finished_message(consts.WIN_MESSAGE, LevelSelectionScreen)
        else:
            self.data.loss()
            self.render_lives()
            if self.data.game_over():
                self.level_finished_message(consts.GAME_OVER_MESSAGE, LevelSelectionScreen)
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

        book = ImageSprite(consts.SABIO_SPRITES['icon'])
        self.screen.blit(book.image, self.translate_percent(2, 2))

        owl = ImageSprite(consts.SABIO_SPRITES['owl'])
        self.screen.blit(owl.image, self.translate_percent_centered(65, 33, book.rect))

        character = ImageSprite(consts.SABIO_SPRITES[self.selected_character])
        self.screen.blit(character.image,
                         self.translate_percent_centered(15, 83,
                                                         character.rect))

        #displaying score
        self.update_score()

        self.show_lives_text()
        self.render_lives()

        self.next_question()
        #pygame.display.update()


    def display_reading(self, reading):
        surface = self.show_text_rect(reading,
                                      self.small_font, self.box_size,
                                      self.box_pos,
                                      COLORS['grey'], COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=COLORS['yellow'],
                                      parent_alpha=191)
        pygame.display.update()
        #TODO agregar deteccion de click y boton para siguiente
        words = len(reading.split(' '))
        time_to_wait = int(words * self.seconds_per_word * 1000)
        time_to_wait = 2000
        pygame.time.wait(time_to_wait)
        #display question

        self.display_question(self.current_question.get('pregunta'))

    def display_question(self, question):
        surface = self.show_text_rect(question,
                                      self.small_font, self.box_size,
                                      self.box_pos,
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
        for i, s in enumerate(['lamp', 'book_locked', 'feather', 'cloud_locked']):
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
            if sprite.name == 'lamp':
                SabioScreen(self.screen).run()
            elif sprite.name == 'feather':
                PoetaScreen(self.screen).run()
            self.menu_items.empty()
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
