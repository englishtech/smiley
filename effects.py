import pygame as pg
from shapes import Like, Star
from config import WIDTH, HEIGHT, FPS, SCALE_X, SCALE_Y, NUM_X, NUM_Y, images


def stars_burst(space, all_sprites, gamemap):  # Эффект разлетающихся star
    like_sprite = gamemap["like"]
    print("Collision with smile!")
    for _ in range(50):
        star = Star(space, HEIGHT, SCALE_X, SCALE_Y,
                    images["like"], like_sprite.body.position[0], HEIGHT - like_sprite.body.position[1])

        all_sprites.add(star)
    print("Ended.")
    like_sprite.kill()
    gamemap["win"] = True
    gamemap["time_to_menu"] = pg.time.get_ticks()
