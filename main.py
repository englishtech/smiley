# Меню выбора уровенй доделать
# Табличка победы и смерти
# Смерть смайлика об шипы -> Restart & Menu
# Спрайт like менять на star, когда с ним сталкивается player
# player лицом в сторону движения
# рандомные фоны игры и другой фон меню


import pygame as pg
import pymunk.pygame_util
from config import WIDTH, HEIGHT, FPS, GRAVITY, SCALE_X, NUM_X, NUM_Y, images, gamemap
from collisions import check_handlers
import states


# Переворот координат под pymunk - (0, 0) - левый нижний угол
pymunk.pygame_util.positive_y_is_up = True

# инициализация pygame
pg.init()
surface = pg.display.set_mode((WIDTH, HEIGHT), pg.RESIZABLE)
clock = pg.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(surface)
all_sprites = pg.sprite.Group()
space = pymunk.Space()
space.gravity = GRAVITY
space.sleep_time_threshold = 0.3


# Проверка всех хэндлеров
check_handlers(space, all_sprites, gamemap)


# Основной цикл
while True:

    # Не пора ли вызвать экран меню (если smile коснулся like, и прошло 3000 мс)
    if (gamemap["win"] == True) and (pg.time.get_ticks() - gamemap["time_to_menu"] > 3000):
        # Вызов таблички победы и выбора меню или след. уровень
        gamemap["state"] = "menu"

    # Обработка событий
    if gamemap["state"] == "menu":
        states.menu(surface, space, gamemap, all_sprites)

    if gamemap["state"] == "game":
        states.game(surface, space, clock, gamemap, all_sprites)

    if gamemap["state"] == "restart":
        states.restart(surface, space, gamemap, all_sprites)
