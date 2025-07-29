import pygame as pg
from config import WIDTH, HEIGHT, FPS, SCALE_X, images
from levels.levels import load_level
from shapes import MenuButton
from keyboard import check_game_keys

# Меню выбора уровня


def menu(surface, space, gamemap, all_sprites):

    back_menu = pg.transform.scale(pg.image.load(
        images["back_game"]).convert(), (WIDTH, HEIGHT))

    # Создание кнопки
    button_size = SCALE_X*4
    x1 = WIDTH//2 - button_size*2
    y1 = HEIGHT - HEIGHT*0.8
    text = 1
    button_sprites = pg.sprite.Group()  # Группа спрайтов button

    # gamemap, all_sprites, player = load_level(6, space, all_sprites)
    # return

    for i in range(0, 5):
        for j in range(0, 5):
            x = x1 + (button_size)*j
            y = y1 + (button_size)*i
            button = MenuButton(str(text), x, y)
            button_sprites.add(button)
            text += 1

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pg.mouse.get_pos()
                for button_sprite in button_sprites:
                    if button_sprite.is_clicked(mouse_pos):
                        print("Нажата кнопка", button_sprite.text)
                        # Загрузка уровня с определенным level_number
                        level_number = button_sprite.text
                        gamemap, all_sprites, player = load_level(
                            level_number, space, all_sprites)
                        print("Loading level", level_number)

    # space.step(1 / FPS)
    surface.blit(back_menu, (0, 0))

    # Отрисовка кнопок
    for button_sprite in button_sprites:
        button_sprite.draw(surface)

    pg.display.flip()
    pg.time.Clock().tick(FPS)

# Цикл игры


def game(surface, space, clock, gamemap, all_sprites):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            check_game_keys(gamemap["player"])
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                gamemap, all_sprites, player = load_level(
                    gamemap["current_level"], space, all_sprites)
                print("Loading level", gamemap["current_level"])

    space.step(1 / FPS)
    surface.blit(gamemap["back_game"], (0, 0))

    # Обновление всех спрайтов в группе
    all_sprites.update()

    # Отображение всех спрайтов в группе
    # Статичные кирпичи вынести в отдельную группу, чтобы не рисовать на каждом кадре
    all_sprites.draw(surface)

    pg.display.flip()
    clock.tick(FPS)
    # print(pg.time.get_ticks())

    # if not gamemap["player"].alive:
    #    print("Player is dead.")


def restart(surface, space, gamemap, all_sprites):

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            keys = pg.key.get_pressed()
            if keys[pg.K_UP]:
                gamemap, all_sprites, player = load_level(
                    gamemap["current_level"], space, all_sprites)
                print("Loading level", gamemap["current_level"])
            if keys[pg.K_DOWN]:
                gamemap["state"] = "menu"

    back_restart = pg.image.load(images["explosion"]).convert_alpha()
    back_restart = pg.transform.scale(back_restart, (WIDTH//4, HEIGHT//4))
    back_rect = back_restart.get_rect()
    # <--- устанавливаем координаты центра спрайта
    back_rect.center = (WIDTH//2, HEIGHT//2)

    # Шрифт
    font = pg.font.Font(None, SCALE_X)
    text = "UP: Restart DOWN: Menu"
    text_surface = font.render(text, True, (0, 0, 200))
    text_rect = text_surface.get_rect(center=back_rect.center)

    surface.blit(back_restart, back_rect)
    surface.blit(text_surface, text_rect)

    pg.display.flip()
    pg.time.Clock().tick(FPS)
