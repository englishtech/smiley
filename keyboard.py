import pygame as pg
# from player import Player


def check_game_keys(player):
    # Получаем состояние клавиш
    keys = pg.key.get_pressed()
    print(player.body.velocity)
    # Проверяем, какие клавиши нажаты
    # Если скорость падения < 50 каких-то единиц
    if keys[pg.K_UP] and player.in_jump == False:
        player.body.velocity = (player.body.velocity.x, 0)

        player.body.apply_impulse_at_world_point(
            player.JUMP_VECTOR, player.body.position)
        player.in_jump = True
    if keys[pg.K_RIGHT] and player.after_collision:
        player.body.velocity = (0, player.body.velocity.y)
        player.body.apply_impulse_at_world_point(
            player.RIGHT_VECTOR, player.body.position)
        player.after_collision = False
    if keys[pg.K_LEFT] and player.after_collision:
        player.body.velocity = (0, player.body.velocity.y)
        player.body.apply_impulse_at_world_point(
            player.LEFT_VECTOR, player.body.position)
        player.after_collision = False
    if keys[pg.K_DOWN]:
        player.body.velocity = (0, 0)
    if keys[pg.K_F11]:
        pg.display.toggle_fullscreen()
