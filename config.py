# Константы экрана
FPS = 60
WIDTH, HEIGHT = 800, 600
NUM_X, NUM_Y = 40, 30  # 40 х 30 квадратов на экране
SCALE_X = WIDTH // NUM_X  # Размер квадрата
SCALE_Y = HEIGHT // NUM_Y  # Размер квадрата
GRAVITY = (0, -SCALE_Y*70)

# Словарь всех (не всех) объектов для проверки столкновений {Идентификатор: Объект Player}
gamemap = {}
gamemap["state"] = "menu"
gamemap["win"] = False

# Пути к изображениям
images = {}
images["back_game"] = 'img/back2.png'
images["back_menu"] = 'img/back2.png'
images["player"] = 'img/small_smile_smile.png'
images["player_right"] = 'img/small_smile_right1.png'
images["player_left"] = 'img/small_smile_left1.png'
images["player_right_down"] = 'img/small_smile_right2.png'
images["player_left_down"] = 'img/small_smile_left2.png'
images["dead"] = 'img/smile_fear1.png'
images["plate"] = 'img/plate.png'
images["brick"] = 'img/brick.png'
images["dbrick"] = 'img/brick_rev.png'
images["like"] = 'img/like.png'
images["pipe"] = 'img/pipe.png'
images["spike"] = 'img/spike.png'
images["menu_button"] = 'img/button5.png'
images["explosion"] = 'img/explosion.png'


# ID тайлов в редакторе tiled
tiles = {"player": 3,
         "like": 7,
         "plate": 6,
         "brick": 1,
         "dbrick": 2,
         "spike": 4,
         "pipe": 5}
