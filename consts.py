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
    'checkbox': get_sprite_path('sabio', 'checkbox.png'),
    'checkbox_checked': get_sprite_path('sabio', 'checkbox-checked.png'),
    'checkbox_bad': get_sprite_path('sabio', 'checkbox-bad.png'),
}

FONT_PATH = 'assets/fonts/PatuaOne-Regular.ttf'

BOY = 'boy'
GIRL = 'girl'

GAME_OVER_TIME = 2000 #3 segundos
MAX_QUESTION_CHARS = 30

#messages
WIN_MESSAGE = "Felicidades, pasas al siguiente nivel!"
GAME_OVER_MESSAGE = 'Vuelve a Intentarlo'
