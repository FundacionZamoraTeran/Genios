import sys
import pygame
from pygame.locals import QUIT
from gi.repository import Gtk
import consts

OLPC_SCREEN_SIZE = (1200, 900)
EVENT_REFRESH = pygame.USEREVENT+1

import logging
_logger = logging.getLogger('genio-activity')

class ImageSprite(pygame.sprite.Sprite):
    '''Class to create a background image'''

    def __init__(self, image_file, location=(0, 0), name=None, scale=None):
        '''
            image_file: filepath for the image
            location: tuple of x y coordinates
            name: name for the sprite
            scale: tuple of the new size of the image
        '''
        pygame.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = pygame.image.load(image_file).convert_alpha()
        if scale:
            self.image = pygame.transform.scale(self.image, scale)

        self.name = name
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class BaseHelperClass(object):
    '''
    Helper class to locate objects on the screen based on percentage
    need to improve the name of this
    '''
    width, height = OLPC_SCREEN_SIZE
    game_state = None

    def translate_percent(self, width, height):
        '''translates percentages to screen positions'''
        x = (width / 100.0) * self.width
        y = (height / 100.0) * self.height
        return x, y

    def translate_percent_centered(self, width, height, rect):
        '''
        translates percentages to screen positions
        using the sprite center as point instead of top corner
        '''
        x, y = self.translate_percent(width, height)
        x = x - (rect.width/2.0)
        y = y - (rect.height/2.0)
        return x, y

    #def read_file(self):
    #    '''Sugar functions to read data from the diary'''
    #    self.game_state.load()

    #def write_file(self):
    #    '''Sugar functions to write data from the diary'''
    #    self.game_state.save()

class ScreenBaseClass(BaseHelperClass):
    '''
    Base class to draw screens it contains
    helper methods for screen and click detection
    '''
    score_surface = None
    selected_character = None
    lives_sprites = pygame.sprite.Group()
    menu_items = pygame.sprite.Group()
    current_question = None

    def __init__(self, screen):
        self.screen = screen


    def show_lives_text(self):
        self.show_text(str('VIDAS'), self.text_font,
                       self.translate_percent(87, 2),
                       COLORS['white'])

    def set_background(self):
        '''Sets the background on the screen'''
        background = ImageSprite(self.background_src, scale=OLPC_SCREEN_SIZE)
        self.screen.blit(background.image, background.rect)
        surface = pygame.Surface(OLPC_SCREEN_SIZE)
        surface.blit(background.image, background.rect)
        self.background = surface
        return background

    def run(self):
        '''This method is executed to start drawing stuff on screen'''
        raise NotImplementedError

    def play_music(self):
        if self.background_music:
            self.stop_music()
            pygame.mixer.music.set_volume(1.0)
            pygame.mixer.music.load(self.background_music)
            pygame.mixer.music.play(-1)

    def stop_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

    def click_callback(self):
        '''This method is executed when detecting a click on items'''
        raise NotImplementedError

    def update_score(self, score=None):
        pos = self.translate_percent(15, 8)
        score = score or self.data.score
        if self.score_surface:
            rect = self.score_surface.get_rect()
            rect.left, rect.top = pos
            self.screen.blit(self.background, pos, rect)

        self.score_surface = self.show_text(str(score), self.text_font,
                                            pos, COLORS['white'])

    def render_lives(self, sprite_path, num=None):
        num = num or self.data.current_lives
        initial_location = self.translate_percent(85, 8)

        self.lives_sprites.clear(self.screen, self.background)
        self.lives_sprites.empty()

        for x in range(num):
            sprite = ImageSprite(sprite_path, initial_location)
            self.lives_sprites.add(sprite)
            initial_location = (initial_location[0] + 55, initial_location[1])

        self.lives_sprites.draw(self.screen)

    def next_question(self):
        self.current_question = self.data.get_random_question()
        self.display_reading(self.current_question.get('lectura', ''))

    def level_finished_message(self, message, next_screen):
        surface = self.show_text_rect(message,
                                      self.small_font, self.box_size,
                                      self.box_pos,
                                      COLORS['grey'], COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=COLORS['yellow'],
                                      parent_alpha=191)
        pygame.display.update()
        pygame.time.wait(consts.GAME_OVER_TIME)
        return next_screen(self.screen).run()


    def detect_click(self):
        '''Event loop to detect clicks'''
        while True:
            #hack para sugargame
            while Gtk.events_pending():
                Gtk.main_iteration()

            for event in pygame.event.get():
                if event.type == QUIT:
                    try:
                        pygame.quit()
                        sys.exit()
                        return
                    except Exception, e:
                        return
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in self.menu_items \
                                       if s.rect.collidepoint(pos)]
                    for s in clicked_sprites:
                        self.click_callback(s)
                        break
                elif event.type == EVENT_REFRESH:
                    pygame.display.update()
                else:
                    continue

    def show_text(self, text, font, pos=(0, 0), color=(255, 255, 255)):
        sprite = font.render(text, 1, color)
        rect = sprite.get_rect()
        rect.left, rect.top = pos
        self.screen.blit(sprite, rect)
        return sprite

    def show_text_rect(self, text, font, size, pos, color,
                       background, justification=0, alpha=None,
                       parent_background=None, parent_alpha=None,
                       margin=20):

        rect = pygame.Rect(pos, size)
        surface = self._render_textrect(text, font, rect, color,
                                        justification=justification)

        if parent_background:
            parent_size = (size[0] + margin, size[1] + margin)
            parent_pos = (pos[0] - (margin/2), pos[1] - (margin/2))
            parent_rect = pygame.Rect(parent_pos, parent_size)
            parent_surface = pygame.Surface(parent_size)
            parent_surface.fill(parent_background)
            parent_surface.set_alpha(parent_alpha)

            surface2 = pygame.Surface(rect.size)
            surface2.fill(background)
            surface2.set_alpha(alpha)

            self.screen.blit(self.background, parent_pos, parent_rect)
            self.screen.blit(parent_surface, parent_rect)
            self.screen.blit(surface2, rect)
        else:
            self.screen.blit(self.background, pos, rect)


        self.screen.blit(surface, rect)
        return surface

    def _render_textrect(self, string, font, rect,
                         text_color, background_color=None,
                         justification=0, alpha=None):
        """Returns a surface containing the passed text string, reformatted
        to fit within the given rect, word-wrapping as necessary. The text
        will be anti-aliased.

        Takes the following arguments:

        string - the text you wish to render. \n begins a new line.
        font - a Font object
        rect - a rectstyle giving the size of the surface requested.
        text_color - a three-byte tuple of the rgb value of the
                    text color. ex (0, 0, 0) = BLACK
        background_color - a three-byte tuple of the rgb value of the surface.
        justification - 0 (default) left-justified
                        1 horizontally centered
                        2 right-justified

        Returns the following values:

        Success - a surface object with the text rendered onto it.
        Failure - raises a TextRectException if the text won't fit onto the surface.
        """

        final_lines = []

        requested_lines = string.splitlines()

        # Create a series of lines that will fit on the provided
        # rectangle.

        for requested_line in requested_lines:
            if font.size(requested_line)[0] > rect.width:
                words = requested_line.split(' ')
                # if any of our words are too long to fit, return.
                for word in words:
                    if font.size(word)[0] >= rect.width:
                        raise Exception("The word " + word + " is too long to fit in the rect passed.")
                # Start a new line
                accumulated_line = ""
                for word in words:
                    test_line = accumulated_line + word + " "
                    # Build the line while the words fit.
                    if font.size(test_line)[0] < rect.width:
                        accumulated_line = test_line
                    else:
                        final_lines.append(accumulated_line)
                        accumulated_line = word + " "
                final_lines.append(accumulated_line)
            else:
                final_lines.append(requested_line)

        # Let's try to write the text out on the surface.

        if background_color:
            surface = pygame.Surface(rect.size)
            surface.fill(background_color)
        if alpha:
            surface.set_alpha(alpha)
        else:
            surface = pygame.Surface(rect.size, pygame.SRCALPHA, 32)

        accumulated_height = 0
        for line in final_lines:
            if accumulated_height + font.size(line)[1] >= rect.height:
                raise Exception("Once word-wrapped, the text string was too tall to fit in the rect.")
            if line != "":
                tempsurface = font.render(line, 1, text_color)
                if justification == 0:
                    surface.blit(tempsurface, (0, accumulated_height))
                elif justification == 1:
                    surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
                elif justification == 2:
                    surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
                else:
                    raise Exception("Invalid justification argument: " + str(justification))
            accumulated_height += font.size(line)[1]

        return surface

    def display_reading(self, reading):
        surface = self.show_text_rect(reading,
                                      self.small_font, self.box_size,
                                      self.box_pos,
                                      COLORS['grey'], COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=COLORS['yellow'],
                                      parent_alpha=191)
        pygame.display.update()
        #removing pun
        words = len(reading.split(' '))
        time_to_wait = words * int(self.seconds_per_word * 1000)
        pygame.time.wait(time_to_wait)
        #display question

        self.display_question(self.current_question.get('pregunta'))


    def display_question(self, question, sprite_dict, pos):
        surface = self.show_text_rect(question,
                                      self.small_font, self.box_size,
                                      self.box_pos,
                                      COLORS['grey'], COLORS['white'],
                                      justification=1, alpha=191,
                                      parent_background=COLORS['yellow'],
                                      parent_alpha=191)
        #agregar sprites de opcion de menu
        #pos = self.translate_percent(30, 40)
        for i, option in enumerate(self.current_question.get('opciones')):
            checkbox = ImageSprite(sprite_dict['checkbox'], pos, name=str(i))
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

CURSOR = (
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  ",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ",
        "XXX.........................XXXX",
        "XXX..........................XXX",
        "XXX..........................XXX",
        "XXX.........................XXXX",
        "XXX.......XXXXXXXXXXXXXXXXXXXXX ",
        "XXX........XXXXXXXXXXXXXXXXXXX  ",
        "XXX.........XXX                 ",
        "XXX..........XXX                ",
        "XXX...........XXX               ",
        "XXX....X.......XXX              ",
        "XXX....XX.......XXX             ",
        "XXX....XXX.......XXX            ",
        "XXX....XXXX.......XXX           ",
        "XXX....XXXXX.......XXX          ",
        "XXX....XXXXXX.......XXX         ",
        "XXX....XXX XXX.......XXX        ",
        "XXX....XXX  XXX.......XXX       ",
        "XXX....XXX   XXX.......XXX      ",
        "XXX....XXX    XXX.......XXX     ",
        "XXX....XXX     XXX.......XXX    ",
        "XXX....XXX      XXX.......XXX   ",
        "XXX....XXX       XXX.......XXX  ",
        "XXX....XXX        XXX.......XXX ",
        "XXX....XXX         XXX.......XXX",
        "XXX....XXX          XXX......XXX",
        "XXX....XXX           XXX.....XXX",
        "XXX....XXX            XXX...XXXX",
        " XXX..XXX              XXXXXXXX ",
        "  XXXXXX                XXXXXX  ",
        "   XXXX                  XXXX   "
)

COLORS = {
    'white': (255, 255, 255),
    'black': (0, 0, 0),
    'grey': (130, 130, 130),
    'yellow': (252, 185, 24),
}
