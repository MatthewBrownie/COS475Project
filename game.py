# Example file showing a basic pg "game loop"
import random

import pygame as pg

# drawing parameters
canvas_x = 768
canvas_y = 1024
bird_size = 30
bird_color = "yellow"
pipe_color = (0, 150, 0, 150)

# game parameters
gravity = 0.5
jump_force = 10
terminal_vel = 50
pipe_width = 100
pipe_gap = 200
pipe_spacing = 300
pipe_speed = 1

# init stuff
bird_pos = pg.Vector2(canvas_x / 3, canvas_y / 2)
bird_vel = pg.Vector2(0, 0)
pipes = []

# pg setup
pg.init()
screen = pg.display.set_mode((canvas_x, canvas_y))
pg.display.set_caption("Flappy Bird Game")
clock = pg.time.Clock()
count = 0
running = True


def create_pipe(count):
    x = canvas_x + pipe_width
    gap = random.randint(0 + pipe_gap, canvas_y - pipe_gap)
    pipe = (x, gap)
    return pipe


while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                bird_vel.y = -jump_force

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("pink")
    # Pipes
    if count % pipe_spacing == 0:
        pipes.append(create_pipe(count))

    for i, (x, gap) in enumerate(pipes):
        pipes[i] = (x - pipe_speed, gap)
        # top pipe
        pg.draw.rect(screen, pipe_color, pg.Rect(x, 0, pipe_width, gap - pipe_gap))
        # bottom pipe
        pg.draw.rect(screen, pipe_color, pg.Rect(x, gap, pipe_width, 10000))

    # Bird
    pg.draw.circle(screen, bird_color, bird_pos, bird_size)
    if (bird_pos.y + bird_vel.y + bird_size) >= canvas_y:
        bird_vel = pg.Vector2(bird_vel.x, bird_vel.y * -0.8)

    if bird_vel.y < terminal_vel:
        bird_vel.y += gravity

    bird_pos += bird_vel

    # Render and tick
    pg.display.flip()
    clock.tick(60)
    count += 1

pg.quit()
