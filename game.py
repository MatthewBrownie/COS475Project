# Flappy bird clone
import random

import pygame as pg

# drawing parameters
CANVAS_X = 600
CANVAS_Y = 800
BIRD_SIZE = 27
BIRD_COLOR = "yellow"
PIPE_COLOR = (18, 122, 23)
BACKGROUND_COLOR = (156, 195, 217)

# game parameters
GRAVITY = 0.55
JUMP_FORCE = 10
TERMINAL_VEL = 50
PIPE_WIDTH = 100
PIPE_GAP = 200
PIPE_SPACING = 300
PIPE_SPEED = 3

# init stuff
bird_pos = pg.Vector2(2 * CANVAS_X / 5, CANVAS_Y / 2)
bird_vel = pg.Vector2(0, 0)
count = 0
score = 0
pipes = []
pipe_id = 1


# pg setup
pg.init()
screen = pg.display.set_mode((CANVAS_X, CANVAS_Y))
pg.display.set_caption("Flappy Bird Game")
clock = pg.time.Clock()
running = True


def create_pipe():
    global pipe_id
    x = CANVAS_X + PIPE_WIDTH
    gap = random.randint(0 + PIPE_GAP, CANVAS_Y - PIPE_GAP)
    pipe = (x, gap, pipe_id)
    pipe_id += 1
    return pipe


def reset():
    pg.time.wait(300)
    global bird_pos, bird_vel, count, score, pipes, pipe_id
    bird_pos = pg.Vector2(2 * CANVAS_X / 5, CANVAS_Y / 2)
    bird_vel = pg.Vector2(0, 0)
    count = 0
    score = 0
    pipes = []
    pipe_id = 1
    print("GAME OVER\n\n")
    pause()


def pause():
    screen.fill(BACKGROUND_COLOR)
    pg.draw.circle(screen, BIRD_COLOR, bird_pos, BIRD_SIZE)
    paused = True
    while paused:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    paused = False
                    bird_vel.y = -JUMP_FORCE
        pg.display.flip()
        clock.tick(60)


screen.fill(BACKGROUND_COLOR)
pg.draw.circle(screen, BIRD_COLOR, bird_pos, BIRD_SIZE)
pause()
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                bird_vel.y = -JUMP_FORCE

    # Wipe screen with background color
    screen.fill(BACKGROUND_COLOR)

    # --- Pipes ---
    # new pipes
    if count % round((PIPE_SPACING + PIPE_WIDTH) / PIPE_SPEED, 0) == 0 or not pipes:
        pipes.append(create_pipe())

    # score and pipe deletion
    first_pipe = pipes[0]
    if first_pipe[0] <= bird_pos.x:
        if score != first_pipe[2]:
            score = first_pipe[2]
            if score % 2 == 0 and score != 0:
                PIPE_SPEED += .3
            print(f"Score: {score}")
    if first_pipe[0] - PIPE_SPEED <= -PIPE_WIDTH:
        pipes.pop(0)

    # movement and draw pipe
    for i, (x, gap, pid) in enumerate(pipes):
        # shift all pipes
        pipes[i] = (x - PIPE_SPEED, gap, pid)

        top_pipe = pg.Rect(x, 0, PIPE_WIDTH, gap - PIPE_GAP)
        bottom_pipe = pg.Rect(x, gap, PIPE_WIDTH, 10000)

        pg.draw.rect(screen, PIPE_COLOR, top_pipe)
        pg.draw.rect(screen, PIPE_COLOR, bottom_pipe)

    # --- Bird ---
    # bird movement
    if bird_vel.y < TERMINAL_VEL:
        bird_vel.y += GRAVITY
    bird_pos += bird_vel

    # draw bird
    pg.draw.circle(screen, BIRD_COLOR, bird_pos, BIRD_SIZE)
    pg.display.flip()

    # collision
    (b_x, b_y) = (bird_pos.x, bird_pos.y)
    if b_y + BIRD_SIZE >= CANVAS_Y:
        reset()
    else:
        for x, gap, _ in pipes:
            if b_x + BIRD_SIZE <= x:
                break
            if b_x - BIRD_SIZE >= x + PIPE_WIDTH:
                break
            if (b_y - BIRD_SIZE >= gap - PIPE_GAP) and (b_y + BIRD_SIZE <= gap):
                break
            reset()

    # Display and tick
    clock.tick(60)
    count += 1

pg.quit()
