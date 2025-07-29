import pygame as pg
import pymunk.pygame_util
import math
from config import WIDTH, HEIGHT, images, SCALE_X, SCALE_Y
from random import randint


class Player(pg.sprite.Sprite):
    def __init__(self, space, x, y):
        super().__init__()
        MASS, RADIUS = 1, SCALE_X*0.8

        self.image_center = pg.image.load(images["player"]).convert_alpha()
        self.image_center = pg.transform.smoothscale(
            self.image_center, (RADIUS * 2, RADIUS * 2))
        
        self.image_right = pg.image.load(images["player_right"]).convert_alpha()
        self.image_right = pg.transform.smoothscale(
            self.image_right, (RADIUS * 2, RADIUS * 2))
        self.image_left = pg.image.load(images["player_left"]).convert_alpha()
        self.image_left = pg.transform.smoothscale(
            self.image_left, (RADIUS * 2, RADIUS * 2))
        
        self.image_right_down = pg.image.load(
            images["player_right_down"]).convert_alpha()
        self.image_right_down = pg.transform.smoothscale(
            self.image_right_down, (RADIUS * 2, RADIUS * 2))
        self.image_left_down = pg.image.load(
            images["player_left_down"]).convert_alpha()
        self.image_left_down = pg.transform.smoothscale(
            self.image_left_down, (RADIUS * 2, RADIUS * 2))

        self.image = self.image_center

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.JUMP_VECTOR = pymunk.Vec2d(0, SCALE_Y * 20)  # Импульс вверх
        self.RIGHT_VECTOR = pymunk.Vec2d(
            SCALE_X*8, SCALE_Y*5)  # Импульс вправо
        # Импульс влево
        self.LEFT_VECTOR = pymunk.Vec2d(-SCALE_X*8, SCALE_Y*5)

        self.last_update = pg.time.get_ticks()

        moment = pymunk.moment_for_circle(MASS, 0, RADIUS)
        self.body = pymunk.Body(MASS, moment)
        self.body.position = (x, HEIGHT - y)
        # self.body.velocity = (0, 0)
        self.shape = pymunk.Circle(self.body, RADIUS)
        self.shape.elasticity = 1
        # self.shape.friction = 0
        self.shape.collision_type = 1
        self.shape.sprite = self  # Добавляем ссылку на спрайт в форму

        space.add(self.body, self.shape)

        # Включается True после столкновения (проверяется при нажатии клавиатуры)
        self.after_collision = False
        self.in_jump = False
        self.to_right = False
        self.to_left = False
        self.to_center = True
        self.alive = True

    def update(self):

        if self.alive:
            if -0.5 <= self.body.velocity.x <= 0.5:
                self.image = self.image_center
            elif self.body.velocity.x > 0.5 and self.body.velocity.y > 0:
                self.image = self.image_right
            elif self.body.velocity.x < -0.5 and self.body.velocity.y > 0:
                self.image = self.image_left
            elif self.body.velocity.x > 0.5 and self.body.velocity.y < -150:
                self.image = self.image_right_down
            elif self.body.velocity.x < -0.5 and self.body.velocity.y < -150:
                self.image = self.image_left_down

        else:
            self.image = pg.image.load(images["dead"]).convert_alpha()
            self.image = pg.transform.smoothscale(
                self.image, (SCALE_X * 2, SCALE_X * 2))
        # Синхронизируем положение спрайта и тела pymunk
        self.rect.centerx = self.body.position[0]
        self.rect.centery = HEIGHT - self.body.position[1]


class Plate(pg.sprite.Sprite):
    def __init__(self, space, x, y):
        super().__init__()
        self.image = pg.image.load(images["plate"]).convert_alpha()
        self.image = pg.transform.smoothscale(
            self.image, (SCALE_X, SCALE_Y))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Создаём статическое тело
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x, HEIGHT - y)
        # Создаём прямоугольную форму
        self.shape = pymunk.Poly.create_box(
            self.body, size=(SCALE_X, SCALE_Y))
        self.shape.elasticity = 1
        self.shape.friction = 1
        self.shape.collision_type = 2
        # Добавляем форму в пространство
        space.add(self.body, self.shape)

        def update(self):
            # Синхронизируем положение спрайта и тела pymunk
            self.rect.centerx = self.body.position[0]
            self.rect.centery = HEIGHT - self.body.position[1]


class Brick(pg.sprite.Sprite):
    def __init__(self, space, x, y):
        super().__init__()
        self.image = pg.image.load(images["brick"]).convert_alpha()
        self.image = pg.transform.smoothscale(
            self.image, (SCALE_X, SCALE_Y))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        # Создаём статическое тело
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x, HEIGHT - y)
        # Создаём прямоугольную форму
        self.shape = pymunk.Poly.create_box(
            self.body, size=(SCALE_X, SCALE_Y))
        self.shape.elasticity = 1
        self.shape.friction = 0.5
        self.shape.collision_type = 2
        # Добавляем форму в пространство
        space.add(self.body, self.shape)


class DBrick(pg.sprite.Sprite):
    def __init__(self, space, x, y):
        super().__init__()
        self.image = pg.image.load(images["dbrick"]).convert_alpha()
        self.image = pg.transform.smoothscale(
            self.image, (SCALE_X, SCALE_Y))
        self.orig_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Создаём динамическое тело
        mass = 0.3
        moment = pymunk.moment_for_box(mass, (SCALE_X, SCALE_Y))
        self.body = pymunk.Body(mass, moment, body_type=pymunk.Body.DYNAMIC)
        self.body.position = (x, HEIGHT - y)

        # Создаём прямоугольную форму
        self.shape = pymunk.Poly.create_box(
            self.body, size=(SCALE_X, SCALE_Y))
        self.shape.elasticity = 0.5
        self.shape.friction = 0.9
        self.shape.collision_type = 3
        # Добавляем форму в пространство
        space.add(self.body, self.shape)
        self.body.sleep()

    def update(self):
        # Синхронизируем положение спрайта и тела pymunk
        self.rect.centerx = self.body.position[0]
        self.rect.centery = HEIGHT - self.body.position[1]
        # Вращаем спрайт
        self.image = pg.transform.rotate(
            self.orig_image, math.degrees(self.body.angle))
        self.rect = self.image.get_rect(center=self.rect.center)


class Spike(pg.sprite.Sprite):
    def __init__(self, space, x, y):
        super().__init__()
        self.image = pg.image.load(images["spike"]).convert_alpha()
        self.image = pg.transform.smoothscale(
            self.image, (SCALE_X, SCALE_Y//2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y + SCALE_Y//4)
        # Создаём статическое тело
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (x, HEIGHT - y - SCALE_Y//4)
        # Создаём прямоугольную форму
        self.shape = pymunk.Poly.create_box(
            self.body, size=(SCALE_X, SCALE_Y//2))
        self.shape.collision_type = 5
        # Добавляем форму в пространство
        space.add(self.body, self.shape)


class Pipe(pg.sprite.Sprite):
    def __init__(self, space, x, y):
        super().__init__()
        self.orig_image = pg.image.load(images["pipe"]).convert_alpha()
        self.orig_image = pg.transform.smoothscale(
            self.orig_image, (SCALE_X, SCALE_Y//2))
        self.image = self.orig_image
        self.rect = self.image.get_rect()
        # Положение верха картинки
        self.rect.center = (x, y - SCALE_Y//4)

        self.x_bottom, self.y_bottom = self.rect.midbottom

        # Создаём статическое тело
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        # Положение центра pipe
        self.body.position = (x, HEIGHT - y - SCALE_Y//4)
        # Создаём прямоугольную форму
        self.shape = pymunk.Poly.create_box(
            self.body, size=(SCALE_X, SCALE_Y//2))
        self.shape.elasticity = 1
        self.shape.friction = 0.5
        self.shape.collision_type = 6
        self.shape.sprite = self  # Добавляем ссылку на спрайт в форму

        # Добавляем форму в пространство
        space.add(self.body, self.shape)
        self.pressed = False
        self.y_size = SCALE_Y*1.5
        self.current_time = pg.time.get_ticks()

    def update(self):
        if self.pressed:

            # Делаем Pipe SCALE_Y*1.5 и уменьшаем каждые 10 мс
            if (self.y_size > SCALE_Y//2) and (pg.time.get_ticks() - self.current_time > 10):
                self.image = pg.transform.smoothscale(
                    self.orig_image, (SCALE_X, self.y_size))
                self.rect = self.image.get_rect()
                self.rect.midbottom = (self.x_bottom, self.y_bottom)
                self.y_size -= 1
                self.current_time = pg.time.get_ticks()

            elif (self.y_size <= SCALE_Y//2):
                self.pressed = False
                self.y_size = SCALE_Y*2
                self.image = self.orig_image
                self.rect = self.image.get_rect()

        # Синхронизируем положение спрайта и тела pymunk
        self.rect.centerx = self.body.position[0]
        self.rect.centery = HEIGHT - self.body.position[1]


class Like(pg.sprite.Sprite):
    def __init__(self, space, x, y):
        super().__init__()
        self.image = pg.image.load(images["like"]).convert_alpha()
        self.image = pg.transform.smoothscale(
            self.image, (SCALE_X*2, SCALE_Y*2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.JUMP_VECTOR = pymunk.Vec2d(0, SCALE_Y * 10)  # Импульс вверх
        self.last_update = pg.time.get_ticks()

        # Создаём динамический лайк
        mass = 1
        moment = pymunk.moment_for_box(mass, (SCALE_X*2, SCALE_Y*2))
        self.body = pymunk.Body(mass, moment)
        self.body.position = (x, HEIGHT - y)

        # Создаём прямоугольную форму
        self.shape = pymunk.Poly.create_box(
            self.body, size=(SCALE_X*2, SCALE_Y*2.5))
        self.shape.elasticity = 0.5
        self.shape.friction = 0.9
        self.shape.collision_type = 4
        # Добавляем форму в пространство
        space.add(self.body, self.shape)
        self.moves = False

    def update(self):

        # Чтобы не прыгал в стороны
        self.body.velocity = (0, self.body.velocity.y)

        now = pg.time.get_ticks()
        # Подпрыгивает ~каждую секунду
        if (now - self.last_update > 600) and self.body.velocity.y < 1:
            self.body.apply_impulse_at_world_point(
                self.JUMP_VECTOR, self.body.position)
            self.last_update = now

        # Синхронизируем положение спрайта и тела pymunk
        self.rect.centerx = self.body.position[0]
        self.rect.centery = HEIGHT - self.body.position[1]


class Star(pg.sprite.Sprite):
    def __init__(self, space, HEIGHT, SCALE_X, SCALE_Y, image_path, x, y):
        super().__init__()

        self.alive = True

        self.image = pg.image.load(image_path).convert_alpha()
        self.image = pg.transform.smoothscale(
            self.image, (SCALE_X, SCALE_Y))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        # Создаём динамический лайк
        mass = 1
        moment = pymunk.moment_for_box(mass, (SCALE_X, SCALE_Y))
        self.body = pymunk.Body(mass, moment)
        self.body.position = (x, HEIGHT - y)
        self.body.velocity = (
            randint(-WIDTH//2, WIDTH//2), randint(HEIGHT//2, HEIGHT))

        # Создаём прямоугольную форму
        self.shape = pymunk.Poly.create_box(
            self.body, size=(SCALE_X, SCALE_Y))
        self.shape.elasticity = 0.5
        self.shape.friction = 0.9
        self.shape.collision_type = 5
        # Фильтр ,чтобы не реагировали на столкновения
        self.shape.filter = pymunk.ShapeFilter(categories=0, mask=0)
        # Добавляем форму в пространство
        space.add(self.body, self.shape)
        self.space = space

    def update(self):
        # global space
        # Синхронизируем положение спрайта и тела pymunk
        self.rect.centerx = self.body.position[0]
        self.rect.centery = HEIGHT - self.body.position[1]

        self.check_to_kill()

    def check_to_kill(self):

        if (WIDTH > self.body.position[0] < 0) or (self.body.position[1] < 0):
            self.kill()
            # print("Star sprite killed.")
            self.space.remove(self.body, self.shape)
            # print("Star body removed.")
            self.alive = False


# Класс кнопки меню
class MenuButton(pg.sprite.Sprite):
    def __init__(self, text, x, y):
        super().__init__()
        self.image = pg.image.load(images["menu_button"]).convert_alpha()
        self.image = pg.transform.smoothscale(
            self.image, (SCALE_X * 4, SCALE_Y * 4))
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        # <--- устанавливаем координаты центра спрайта
        self.rect.center = (x, y)

        # Шрифт
        font = pg.font.Font(None, SCALE_X * 3)
        self.text = text
        self.text_surface = font.render(text, True, (0, 0, 200))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

        self.is_hovered = False

    def draw(self, surface):
        mouse_pos = pg.mouse.get_pos()

        if self.rect.collidepoint(mouse_pos):
            # print("Mouse on", self.text)  # Если наведен, красим в красный
            original_center = self.rect.center  # Сохраняем центр
            self.image = pg.transform.smoothscale(
                self.image, (SCALE_X * 4.5, SCALE_Y * 4.5))
            self.rect = self.image.get_rect()
            self.rect.center = original_center  # Восстанавливаем центр
        else:
            self.image = self.orig_image

        surface.blit(self.image, self.rect)
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
