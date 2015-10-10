import sys
import pygame
from pygame.locals import QUIT

OLPC_SCREEN_SIZE = (1200, 900)

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

    def translate_percent(self, width, height):
        '''translates percentages to screen positions'''
        x = (width / 100) * self.width
        y = (height / 100) * self.height
        return x, y

    def translate_percent_centered(self, width, height, rect):
        '''
        translates percentages to screen positions
        using the sprite center as point instead of top corner
        '''
        x, y = self.translate_percent(width, height)
        x = x - (rect.width/2)
        y = y - (rect.height/2)
        return x, y

class ScreenBaseClass(BaseHelperClass):
    '''
    Base class to draw screens it contains
    helper methods for screen and click detection
    '''

    def __init__(self, screen):
        self.screen = screen

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

    def click_callback(self):
        '''This method is executed when detecting a click on items'''
        raise NotImplementedError

    def detect_click(self):
        '''Event loop to detect clicks'''
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    clicked_sprites = [s for s in self.menu_items \
                                       if s.rect.collidepoint(pos)]
                    for s in clicked_sprites:
                        self.click_callback(s)
                        break

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
