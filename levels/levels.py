import json
import pygame as pg
import pymunk.pygame_util
from shapes import Player, Like, Brick, DBrick, Plate, Spike, Pipe
from config import WIDTH, HEIGHT, FPS, SCALE_X, SCALE_Y, NUM_X, NUM_Y, GRAVITY, images, tiles, gamemap

# Список pipe (Очистить!!!)


def add_tile_to_gamemap(space, all_sprites, ID, cx, cy):
    if ID == 0:
        return
    if ID == tiles["player"]:  # ID player в tilesheet
        tile = Player(space, cx, cy)
        gamemap["player"] = tile
    if ID == tiles["like"]:  # ID like в tilesheet
        tile = Like(space, cx, cy)
        gamemap["like"] = tile
    if ID == tiles["plate"]:  # ID plate в tilesheet
        tile = Plate(space, cx, cy)
    if ID == tiles["dbrick"]:  # ID dbrick в tilesheet
        tile = DBrick(space, cx, cy)
    if ID == tiles["brick"]:  # ID brick в tilesheet
        tile = Brick(space, cx, cy)
    if ID == tiles["spike"]:  # ID spike в tilesheet
        tile = Spike(space, cx, cy)
    if ID == tiles["pipe"]:  # ID brick в tilesheet
        tile = Pipe(space, cx, cy)
    all_sprites.add(tile)

# Загрузка уровней


def load_level(level_number, space, all_sprites):
    # Загружаем уровень с диска
    file_path = f"levels\\{level_number}.tmj"
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    if data:
        print("JSON loaded.")
        level_single = data["layers"][0]["data"]
        # Создаем список [[Ячейка с номером формы, ... NUM_X раз], ...]
        level_chunked = [level_single[i:i + NUM_X]
                         for i in range(0, len(level_single), NUM_X)]
    else:
        print("Не удалось загрузить JSON.")

    # Очищаем all_sprites и space от всех спрайтов
    all_sprites.empty()
    for body in list(space.bodies):
        for shape in list(body.shapes):
            space.remove(body, shape)
    print("Bodies deleted from space.")
    gamemap.clear()

    # Задаем текущий уровень игры
    gamemap["current_level"] = level_number
    # Фон игры
    gamemap["back_game"] = pg.transform.scale(
        pg.image.load(images["back_game"]).convert(), (WIDTH, HEIGHT))

    # Заполняем спрайтами all_sprites и gamemap
    for i in range(len(level_chunked[0])):
        for j in range(len(level_chunked)):
            cx = SCALE_X // 2 + SCALE_X * i
            cy = SCALE_Y // 2 + SCALE_Y * j
            add_tile_to_gamemap(space, all_sprites,
                                level_chunked[j][i], cx, cy)

    print("Loaded total sprites:", all_sprites)
    gamemap["state"] = "game"
    gamemap["win"] = False
    gamemap["time_to_menu"] = 0

    # Создаем границы экрана по краям и сверху
    # Создание тела (статическое тело не имеет массы и момента инерции)
    lb_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rb_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    ub_body = pymunk.Body(body_type=pymunk.Body.STATIC)

    # lb_body.position = (0, 0)  # Положение не имеет значения для статических тел

    # Создание сегмента (линии) для платформы.  Толщина = 1 пиксель.
    lb_line = pymunk.Segment(lb_body, (0, 0), (0, HEIGHT), 1)  # 1 - толщина
    lb_line.friction = 0.8    # Трение (для примера)
    lb_line.elasticity = 0.5  # Упругость (для примера)
    rb_line = pymunk.Segment(
        rb_body, (WIDTH, 0), (WIDTH, HEIGHT), 1)  # 1 - толщина
    rb_line.friction = 0.8    # Трение (для примера)
    rb_line.elasticity = 0.5  # Упругость (для примера)
    ub_line = pymunk.Segment(
        ub_body, (0, HEIGHT), (WIDTH, HEIGHT), 1)  # 1 - толщина
    ub_line.friction = 0.8    # Трение (для примера)
    ub_line.elasticity = 0.5  # Упругость (для примера)

    # Добавление платформы в пространство
    space.add(lb_body, lb_line)
    space.add(rb_body, rb_line)
    space.add(ub_body, ub_line)

    return gamemap, all_sprites, gamemap["player"]
