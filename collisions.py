import pymunk
# Может, и не все константы импортировать...
from config import WIDTH, HEIGHT, FPS, SCALE_X, SCALE_Y, NUM_X, NUM_Y, images
from shapes import Player, Like, Brick, DBrick, Star, Pipe
from effects import stars_burst


def check_handlers(space, all_sprites, gamemap):
    # Типы столкновений
    COLLISION_TYPE_PLAYER = 1
    COLLISION_TYPE_BRICK = 2
    COLLISION_TYPE_DBRICK = 3
    COLLISION_TYPE_LIKE = 4
    COLLISION_TYPE_SPIKE = 5
    COLLISION_TYPE_PIPE = 6

# Обработчик столкновений между player и любым статическим brick

    def brick_collision(arbiter, space, data):
        player_shape = arbiter.shapes[0]
        player_body = player_shape.body
        player_sprite = gamemap["player"]
        point = arbiter.contact_point_set.points[0]

        # При приземлении сверху, чтобы не скакал в стороны
        if player_body.velocity.y < 0:
            player_body.velocity = (0, player_body.velocity.y * 0.6)
            player_sprite.in_jump = False

        # При ударе головой, чтобы не отскакивал вниз
        if player_body.velocity.y > 0:
            player_body.velocity = (
                player_body.velocity.x, player_body.velocity.y * 0)

        # При ударах влево/вправо, чтобы не отскакивал вбок
        if point.point_a[0] < (player_sprite.body.position[0] - SCALE_X/2):
            player_body.velocity = (0, player_body.velocity.y)
        if point.point_a[0] > (player_sprite.body.position[0] + SCALE_X/2):
            player_body.velocity = (0, player_body.velocity.y)

        player_sprite.after_collision = True

        return True

# Обработчик столкновений между player и любым dbrick

    def dbrick_collision(arbiter, space, data):
        player_shape = arbiter.shapes[0]
        player_body = player_shape.body
        player_sprite = gamemap["player"]
        point = arbiter.contact_point_set.points[0]

        # При приземлении сверху, чтобы не скакал в стороны
        if player_body.velocity.y < 0:
            player_body.velocity = (0, player_body.velocity.y * 0.6)
            player_sprite.in_jump = False

        # При ударе головой, чтобы не отскакивал вниз
        if player_body.velocity.y > 0:
            player_body.velocity = (
                player_body.velocity.x, player_body.velocity.y * 0)

        player_sprite.after_collision = True

        return True

# Обработчик столкновений между player и like

    def like_collision(arbiter, space, data):
        like_shape = arbiter.shapes[1]
        like_body = like_shape.body
        stars_burst(space, all_sprites, gamemap)
        return False

# Обработчик столкновений между player и spike

    def spike_collision(arbiter, space, data):
        gamemap["player"].alive = False
        print("Player is dead.")
        gamemap["state"] = "restart"
        return False

 # Обработчик столкновений между player и pipe

    def pipe_collision(arbiter, space, data):
        player_sprite = arbiter.shapes[0].sprite
        pipe_sprite = arbiter.shapes[1].sprite

        pipe_sprite.pressed = True

        player_sprite.body.velocity = (0, 0)
        player_sprite.body.apply_impulse_at_world_point(
            player_sprite.JUMP_VECTOR*2, player_sprite.body.position)
        player_sprite.after_collision = True
        return True

    # Хэндлер для обработки столкновения между player и любым brick
    handler = space.add_collision_handler(
        COLLISION_TYPE_PLAYER, COLLISION_TYPE_BRICK)
    handler.begin = brick_collision

    # Хэндлер для обработки столкновения между player и любым dbrick
    handler = space.add_collision_handler(
        COLLISION_TYPE_PLAYER, COLLISION_TYPE_DBRICK)
    handler.begin = dbrick_collision

    # Хэндлер для обработки столкновения между player и spike
    handler = space.add_collision_handler(
        COLLISION_TYPE_PLAYER, COLLISION_TYPE_SPIKE)
    handler.begin = spike_collision

    # Хэндлер для обработки столкновения между player и like
    handler = space.add_collision_handler(
        COLLISION_TYPE_PLAYER, COLLISION_TYPE_LIKE)
    handler.begin = like_collision

    # Хэндлер для обработки столкновения между player и pipe
    handler = space.add_collision_handler(
        COLLISION_TYPE_PLAYER, COLLISION_TYPE_PIPE)
    handler.begin = pipe_collision
