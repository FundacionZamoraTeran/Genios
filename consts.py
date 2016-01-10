# -*- coding: utf-8 -*-
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
    'icon': get_sprite_path('sabio', 'cloud.png'),
    'boy': get_sprite_path('sabio', 'boy.png'),
    'boy_life': get_sprite_path('sabio', 'boy-life.png'),
    'girl': get_sprite_path('sabio', 'girl.png'),
    'girl_life': get_sprite_path('sabio', 'girl-life.png'),
    'owl': get_sprite_path('sabio', 'owl.png'),
    'checkbox': get_sprite_path('common', 'checkbox.png'),
    'checkbox_checked': get_sprite_path('common', 'checkbox-checked.png'),
    'checkbox_bad': get_sprite_path('common', 'checkbox-bad.png'),
}

POETA_SPRITES = {
    'icon': get_sprite_path('poeta', 'feather.png'),
    'boy': get_sprite_path('poeta', 'boy.png'),
    'boy_life': get_sprite_path('poeta', 'boy-life.png'),
    'girl': get_sprite_path('poeta', 'girl.png'),
    'girl_life': get_sprite_path('poeta', 'girl-life.png'),
    'checkbox': get_sprite_path('common', 'checkbox.png'),
    'checkbox_checked': get_sprite_path('common', 'checkbox-checked.png'),
    'checkbox_bad': get_sprite_path('common', 'checkbox-bad.png'),
}

CUENTERO_SPRITES = {
    'icon': get_sprite_path('cuentero', 'book.png'),
    'boy': get_sprite_path('cuentero', 'boy.png'),
    'boy_life': get_sprite_path('cuentero', 'boy-life.png'),
    'girl': get_sprite_path('cuentero', 'girl.png'),
    'girl_life': get_sprite_path('cuentero', 'girl-life.png'),
    'checkbox': get_sprite_path('common', 'checkbox.png'),
    'checkbox_checked': get_sprite_path('common', 'checkbox-checked.png'),
    'checkbox_bad': get_sprite_path('common', 'checkbox-bad.png'),
}

GENIO_SPRITES = {
    'icon': get_sprite_path('genio', 'lamp.png'),
    'boy': get_sprite_path('genio', 'boy.png'),
    'boy_life': get_sprite_path('genio', 'boy-life.png'),
    'girl': get_sprite_path('genio', 'girl.png'),
    'girl_life': get_sprite_path('genio', 'girl-life.png'),
    'checkbox': get_sprite_path('common', 'checkbox.png'),
    'checkbox_checked': get_sprite_path('common', 'checkbox-checked.png'),
    'checkbox_bad': get_sprite_path('common', 'checkbox-bad.png'),
    'genie': get_sprite_path('genio', 'genio.png'),
    'dialog': get_sprite_path('genio', 'dialogo.png'),
}

FONT_PATH = 'assets/fonts/BOMBARD.ttf'

TIMEOUT_SOUND = 'assets/audio/effects/timeout.ogg'
WIN_SOUND = 'assets/audio/effects/win.ogg'
CORRECT_SOUND = 'assets/audio/effects/correct.ogg'
LOSS_SOUND = 'assets/audio/effects/loss.ogg'
CLOCK_SOUND = 'assets/audio/effects/tictac.ogg'

BOY = 'boy'
GIRL = 'girl'

GAME_OVER_TIME = 3000 #3 segundos
MAX_QUESTION_CHARS = 30

#messages
WIN_MESSAGE = "Felicitaciones te haz convertido en un genio!"
GAME_OVER_MESSAGE = 'Vuelve a Intentarlo'
