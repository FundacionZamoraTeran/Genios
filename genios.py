# -*- coding: utf-8 -*-
'''
Pygame code here
'''
import sys
import pygame
from pygame.locals import QUIT

from gi.repository import Gtk

from engine import SabioData, PoetaData, CuenteroData, GenioData, GameState
from utils import ImageSprite, BaseHelperClass, ScreenBaseClass, \
                  CURSOR, COLORS, EVENT_REFRESH

import consts

selected_character = None

class CharacterSelectionScreen(ScreenBaseClass):
    '''
    class for character selection screen
    '''
    background_src = 'assets/img/backgrounds/sabio.png'
    menu_items = pygame.sprite.Group()
    selected_character = None
    background_music = 'assets/audio/background/intro-background.ogg'
    HELP_TEXT = u"Conviértete en sabio, poeta, cuentero y genio. Lee y escucha con atención para comprender lo que te dicen las palabras... "

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

    def show_help(self):
        font = pygame.font.Font(consts.FONT_PATH, 20)
        pos = self.translate_percent(25, 80)
        size = (600, 60)
        surface = self.show_text_rect(self.HELP_TEXT, font, size, pos,
                                      COLORS['grey'], COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=COLORS['yellow'],
                                      parent_alpha=191)

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

        self.render_exit_button()
        self.play_music()
        self.show_help()
        pygame.display.update()

        self.detect_click()

class CuenteroScreen(ScreenBaseClass):
    background_src= 'assets/img/backgrounds/cuentero.png'
    seconds_per_word = 60/70.0
    box_size = (840, 550)
    max_question_chars = 50
    LEVEL_NAME = 'book'
    background_music = 'assets/audio/background/cuentero-background.ogg'
    split_paragraphs = True

    def __init__(self, screen):
        super(CuenteroScreen, self).__init__(screen)
        self.data = CuenteroData()
        self.text_font = pygame.font.Font(consts.FONT_PATH, 40)
        self.small_font = pygame.font.Font(consts.FONT_PATH, 24)
        self.selected_character = selected_character
        self.box_pos = self.translate_percent(25, 20)

    def answer_expired(self):
        super(CuenteroScreen, self).answer_expired()
        if self.data.game_over():
            self.level_finished_message(consts.GAME_OVER_MESSAGE, LevelSelectionScreen)
        else:
            self.next_question()

    def click_callback(self, sprite):
        rect = sprite.rect
        pos = (rect.left, rect.top)
        self.menu_items.empty()
        self.stop_sound()
        if sprite.name == str(self.current_question.get('respuesta')):
            #respuesta correcta, registramos puntaje
            self.data.win()
            self.play_sound(consts.CORRECT_SOUND)
            #se muestra un check
            checkbox = ImageSprite(consts.CUENTERO_SPRITES['checkbox_checked'], pos)
            self.update_score()
            if self.data.has_won():
                self.play_sound(consts.WIN_SOUND)
                self.data.game_state.unlock_next_level(self.LEVEL_NAME)
                self.level_finished_message(consts.WIN_MESSAGE, LevelSelectionScreen)
        else:
            self.data.loss()
            self.play_sound(consts.LOSS_SOUND)
            self.render_lives()
            if self.data.game_over():
                self.level_finished_message(consts.GAME_OVER_MESSAGE, LevelSelectionScreen)
            else:
                checkbox = ImageSprite(consts.CUENTERO_SPRITES['checkbox_bad'], pos)

        self.screen.blit(checkbox.image, checkbox.rect)
        pygame.display.update(rect)
        #esperar un round
        pygame.time.wait(1000)
        #mostrar otra pregunta
        self.next_question()

    def render_lives(self, num=None):
        sprite_name = "%s_life" % self.selected_character
        super(CuenteroScreen, self).render_lives(consts.CUENTERO_SPRITES[sprite_name], num)

    def run(self):
        self.set_background()

        icon = ImageSprite(consts.CUENTERO_SPRITES['icon'])
        self.screen.blit(icon.image, self.translate_percent(2, 2))

        character = ImageSprite(consts.CUENTERO_SPRITES[self.selected_character])
        self.screen.blit(character.image,
                         self.translate_percent_centered(15, 83,
                                                         character.rect))

        #displaying score
        self.update_score()

        #diplaying Vidas text
        self.render_exit_button()
        self.show_lives_text()
        self.render_lives()
        self.play_music()

        self.next_question()

    def display_question(self, question):
        pos = self.translate_percent(35, 35)
        super(CuenteroScreen, self).display_question(question, consts.CUENTERO_SPRITES, pos)


class PoetaScreen(ScreenBaseClass):
    background_src= 'assets/img/backgrounds/poeta.png'
    seconds_per_word = 60/50.0
    box_size = (750, 450)
    max_question_chars = 50
    LEVEL_NAME = 'feather'
    background_music = 'assets/audio/background/poeta-background.ogg'
    split_paragraphs = True

    def __init__(self, screen):
        super(PoetaScreen, self).__init__(screen)
        self.data = PoetaData()
        self.text_font = pygame.font.Font(consts.FONT_PATH, 40)
        self.small_font = pygame.font.Font(consts.FONT_PATH, 24)
        self.selected_character = selected_character
        self.box_pos = self.translate_percent(25, 25)

    def answer_expired(self):
        super(PoetaScreen, self).answer_expired()
        if self.data.game_over():
            self.level_finished_message(consts.GAME_OVER_MESSAGE, LevelSelectionScreen)
        else:
            self.next_question()

    def click_callback(self, sprite):
        rect = sprite.rect
        pos = (rect.left, rect.top)
        self.menu_items.empty()
        self.stop_sound()
        if sprite.name == str(self.current_question.get('respuesta')):
            #respuesta correcta, registramos puntaje
            self.data.win()
            self.play_sound(consts.CORRECT_SOUND)
            #se muestra un check
            checkbox = ImageSprite(consts.POETA_SPRITES['checkbox_checked'], pos)
            self.play_sound(consts.CORRECT_SOUND)
            self.update_score()
            if self.data.has_won():
                self.play_sound(consts.WIN_SOUND)
                self.data.game_state.unlock_next_level(self.LEVEL_NAME)
                self.level_finished_message(consts.WIN_MESSAGE, LevelSelectionScreen)
        else:
            self.data.loss()
            self.play_sound(consts.LOSS_SOUND)
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
        self.render_exit_button()
        self.show_lives_text()
        self.render_lives()
        self.play_music()

        self.next_question()
        #pygame.display.update()


    def display_question(self, question):
        pos = self.translate_percent(30, 40)
        super(PoetaScreen, self).display_question(question, consts.POETA_SPRITES, pos)


class SabioScreen(ScreenBaseClass):
    background_src= 'assets/img/backgrounds/sabio.png'
    seconds_per_word = 1
    box_size = (500, 300)
    max_question_chars = 30
    LEVEL_NAME = 'cloud'
    background_music = 'assets/audio/background/sabio-background.ogg'

    def __init__(self, screen):
        super(SabioScreen, self).__init__(screen)
        self.data = SabioData()
        self.text_font = pygame.font.Font(consts.FONT_PATH, 40)
        self.small_font = pygame.font.Font(consts.FONT_PATH, 24)
        self.selected_character = selected_character
        self.box_pos = self.translate_percent(13, 30)

    def answer_expired(self):
        super(SabioScreen, self).answer_expired()
        if self.data.game_over():
            self.level_finished_message(consts.GAME_OVER_MESSAGE, LevelSelectionScreen)
        else:
            self.next_question()

    def click_callback(self, sprite):
        rect = sprite.rect
        pos = (rect.left, rect.top)
        self.menu_items.empty()
        self.stop_sound()
        if sprite.name == str(self.current_question.get('respuesta')):
            #respuesta correcta, registramos puntaje
            self.data.win()
            self.play_sound(consts.CORRECT_SOUND)
            #se muestra un check
            checkbox = ImageSprite(consts.SABIO_SPRITES['checkbox_checked'], pos)
            self.update_score()
            if self.data.has_won():
                self.play_sound(consts.WIN_SOUND)
                self.data.game_state.unlock_next_level(self.LEVEL_NAME)
                self.level_finished_message(consts.WIN_MESSAGE, LevelSelectionScreen)
        else:
            self.data.loss()
            self.play_sound(consts.LOSS_SOUND)
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

        self.render_exit_button()
        self.show_lives_text()
        self.render_lives()

        self.play_music()

        self.next_question()
        #pygame.display.update()


    def display_question(self, question):
        pos = self.translate_percent(20, 40)
        super(SabioScreen, self).display_question(question, consts.SABIO_SPRITES, pos)

class GenioScreen(ScreenBaseClass):
    background_src= 'assets/img/backgrounds/genio.png'
    seconds_per_word = 0.1 #60/20
    box_size = (600, 300)
    max_question_chars = 40
    LEVEL_NAME = 'lamp'

    def __init__(self, screen):
        super(GenioScreen, self).__init__(screen)
        self.data = GenioData()
        self.text_font = pygame.font.Font(consts.FONT_PATH, 40)
        self.small_font = pygame.font.Font(consts.FONT_PATH, 24)
        self.selected_character = selected_character
        self.box_pos = self.translate_percent(10, 30)
        self.dialog_pos = self.translate_percent(20, 15)
        self.dialog = ImageSprite(consts.GENIO_SPRITES['dialog'], self.dialog_pos)

    def answer_expired(self):
        super(GenioScreen, self).answer_expired()
        if self.data.game_over():
            self.level_finished_message(consts.GAME_OVER_MESSAGE, LevelSelectionScreen)
        else:
            self.next_question()

    def play_audio(self, audio_name):
        path =  'assets/audio/%s'  % audio_name
        sound = pygame.mixer.Sound(path)
        ch = sound.play()
        while ch.get_busy():
            pygame.time.delay(100)

    def click_callback(self, sprite):
        rect = sprite.rect
        pos = (rect.left, rect.top)
        self.menu_items.empty()
        self.stop_sound()
        if sprite.name == str(self.current_question.get('respuesta')):
            #respuesta correcta, registramos puntaje
            self.data.win()
            self.play_sound(consts.CORRECT_SOUND)
            #se muestra un check
            checkbox = ImageSprite(consts.GENIO_SPRITES['checkbox_checked'], pos)
            self.update_score()
            if self.data.has_won():
                self.play_sound(consts.WIN_SOUND)
                self.data.game_state.unlock_next_level(self.LEVEL_NAME)
                self.level_finished_message(consts.WIN_MESSAGE, LevelSelectionScreen)
        else:
            self.data.loss()
            self.play_sound(consts.LOSS_SOUND)
            self.render_lives()
            if self.data.game_over():
                self.level_finished_message(consts.GAME_OVER_MESSAGE, LevelSelectionScreen)
            else:
                checkbox = ImageSprite(consts.GENIO_SPRITES['checkbox_bad'], pos)

        self.screen.blit(checkbox.image, checkbox.rect)
        pygame.display.update()
        #esperar un round
        pygame.time.wait(3000)
        #mostrar otra pregunta
        self.next_question()

    def render_lives(self, num=None):
        sprite_name = "%s_life" % self.selected_character
        super(GenioScreen, self).render_lives(consts.GENIO_SPRITES[sprite_name], num)

    def run(self):
        self.set_background()

        book = ImageSprite(consts.GENIO_SPRITES['icon'])
        self.screen.blit(book.image, self.translate_percent(2, 2))

        character = ImageSprite(consts.GENIO_SPRITES[self.selected_character])
        self.screen.blit(character.image,
                         self.translate_percent_centered(15, 83,
                                                         character.rect))

        genie = ImageSprite(consts.GENIO_SPRITES['genie'])
        self.screen.blit(genie.image, self.translate_percent(65, 17))


        #TODO: mostrar al genio

        #displaying score
        self.update_score()

        self.render_exit_button()
        self.show_lives_text()
        self.render_lives()

        pygame.display.update()
        pygame.time.wait(1000)
        self.play_music()
        self.next_question()


    def display_question(self, question):
        #TODO: esconder al genio
        pos = self.translate_percent(20, 40)
        super(GenioScreen, self).display_question(question, consts.GENIO_SPRITES, pos)

    def clean_question(self):
        pos = self.box_pos
        size = self.box_size
        margin = 20
        parent_pos = (pos[0] - (margin/2), pos[1] - (margin/2))
        parent_size = (size[0] + margin, size[1] + margin)
        parent_rect = pygame.Rect(parent_pos, parent_size)
        self.screen.blit(self.background, parent_pos, parent_rect)
        pygame.display.update(parent_rect)

    def show_dialog(self):
        self.screen.blit(self.dialog.image, self.dialog_pos)
        pygame.display.update()

    def clean_dialog(self):
        self.screen.blit(self.background, self.dialog_pos, self.dialog.rect)
        pygame.display.update()

    def next_question(self):
        self.clean_question()
        self.show_dialog()
        self.current_question = self.data.get_random_question()
        #tocamos el audio
        self.play_audio(self.current_question.get('audio'))
        self.clean_dialog()
        self.display_question(self.current_question.get('pregunta'))

class LevelSelectionScreen(ScreenBaseClass):
    background_src = 'assets/img/backgrounds/sabio.png'
    menu_items = pygame.sprite.Group()
    background_music = 'assets/audio/background/intro-background.ogg'
    help_size = (600, 100)
    text_surface = None
    music_playing = True

    def __init__(self, *args, **kwargs):
        super(LevelSelectionScreen, self).__init__(*args, **kwargs)
        self.help_pos = self.translate_percent(25, 80)

    def get_level_list(self):
        level_list = []
        gs = GameState()
        gs.load()
        level_list = gs.available_levels[:]
        for level in gs.locked_levels:
            level_list.append('%s_locked' % level)

        return level_list

    def show_help(self, message):
        font = pygame.font.Font(consts.FONT_PATH, 20)
        self.text_surface = self.show_text_rect(message, font, self.help_size,
                                      self.help_pos, COLORS['grey'],
                                      COLORS['white'], justification=1,
                                      parent_background=COLORS['yellow'],
                                      alpha=191, parent_alpha=191)


    def run(self):
        '''runs the screen'''
        self.set_background()
        mundos = ImageSprite(consts.START_SPRITES['mundos'])
        self.screen.blit(mundos.image, self.translate_percent_centered(50, 20, mundos.rect))
        self.menu_items.empty()
        for i, s in enumerate(self.get_level_list()):
            sprite = ImageSprite(consts.START_SPRITES.get(s), name=s)
            self.menu_items.add(sprite)

            #to calculate evenly percentages, 20, 40, 60, 80
            position = 20 * (i + 1)
            sprite.rect.left, sprite.rect.top = \
                    self.translate_percent_centered(position, 45, sprite.rect)
            self.screen.blit(sprite.image, sprite.rect)

        self.render_exit_button()
        self.play_music()
        pygame.display.update()

        #click detection
        self.detect_click()

    def click_callback(self, sprite):
        if sprite.name.endswith('_locked'):
            pass
            #TODO: mostrar mensaje de que no se puede?
        else:
            #cargamos nuevo nivel
            if sprite.name == 'cloud':
                SabioScreen(self.screen).run()
            elif sprite.name == 'feather':
                PoetaScreen(self.screen).run()
            elif sprite.name == 'book':
                CuenteroScreen(self.screen).run()
            elif sprite.name == 'lamp':
                GenioScreen(self.screen).run()
            self.menu_items.empty()


    def hover_callback(self, sprite):
        if 'cloud' in sprite.name:
            message = u"Sabio, podrás descifrar los dichos populares, las adivinanzas y las emociones que sabiduría te darán."
            audio = 'assets/audio/background/sabio-voz.ogg'
        elif 'feather' in sprite.name :
            message = u"Poeta, descubrirás las formas, aromas, figuras de las palabras, lo bello y lo profundo se revela en un verso."
            audio = 'assets/audio/background/poeta-voz.ogg'
        elif 'book' in sprite.name:
            message = u"Cuentero, conocerás nuevos personajes y lugares, todo puede ser posible si dispuesto estás y con una historia puedes volar."
            audio = 'assets/audio/background/cuentero-voz.ogg'
        elif 'lamp' in sprite.name:
            message = u"Genio, desarrollarás tu máximo potencial como sabio, poeta y cuentero, en genio te convertirás si sabes bien escuchar."
            audio = 'assets/audio/background/genio-voz.ogg'

        #play music and show text
        self.show_help(message)
        self.play_music(audio, 0)
        self.music_playing = False
        pygame.display.update()

    def exit_hover(self):
        if not self.music_playing:
            self.play_music()
            self.music_playing = True

        if self.text_surface:
            pos = self.help_pos
            size = self.help_size
            margin = 20
            parent_pos = (pos[0] - (margin/2), pos[1] - (margin/2))
            parent_size = (size[0] + margin, size[1] + margin)
            parent_rect = pygame.Rect(parent_pos, parent_size)
            self.screen.blit(self.background, parent_pos, parent_rect)
            pygame.display.update(parent_rect)


class MainClass(BaseHelperClass):
    '''Main Class that starts the game'''

    def __init__(self, init_pygame=False):
        '''Start screen init'''
        #Hack para sugargame
        if init_pygame:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption('Genios')
            pygame.display.update()
        else:
            self.screen = None

    def start_screen(self):
        '''Runs the main game'''
        start = CharacterSelectionScreen(self.screen)
        start.run()

    def main(self):
        '''Runs main loop and stuff'''
        self.cursor = pygame.cursors.compile(CURSOR)

        #Hack para sugargame
        if not self.screen:
            self.screen = pygame.display.get_surface()

        pygame.mouse.set_cursor((32,32), (1,1), *self.cursor)
        pygame.time.set_timer(EVENT_REFRESH, 1000)
        self.start_screen()
        while True:
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == QUIT:
                    try:
                        pygame.quit()
                    except:
                        pass
                    sys.exit()
                    break

if __name__ == '__main__':
    MainClass(init_pygame=True).main()
