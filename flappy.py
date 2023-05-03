# Flappy bird clone
import random
from collections import deque

import pygame as pg

random.seed(0)

# sim parameters
WORLD_X = 600
WORLD_Y = 800

# game parameters
GRAVITY = 0.6
JUMP_FORCE = -10
TERMINAL_VEL = 60
BIRD_BB = 25
BIRD_START = [2 * WORLD_X / 5, WORLD_Y / 2]

# pipe parameters
PIPE_WIDTH = 100
PIPE_GAP = 200
PIPE_SPACING = 400
PIPE_SPEED = 5
PIPE_SPEED_INC = 0.1

# drawing parameters
BIRD_SIZE = 27
BIRD_COLOR = "yellow"
PIPE_COLOR = (18, 122, 23)
BACKGROUND_COLOR = (156, 195, 217)


def pause(clock):
    pg.display.flip()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    return True
                elif event.key == pg.K_p:
                    return False
        clock.tick(30)


def run_instance(net=None, draw=False, ticks_per_frame=1, print_score=False, human=False):
    # net: the network playing the game
    # draw: whether the game is "played" or just simulated
    # ticks_per_frame: how fast the game is played
    # print_score: whether the score is printed after the game is played
    # human: a param to let humans play

    if human: 
        draw = True
        print_score = True

    bird_pos = BIRD_START.copy()
    bird_vel = 0
    pipe_speed = PIPE_SPEED
    real_pipes = deque([])
    fake_pipes = deque([])
    pipe_timer = float("inf")
    dist_traveled = 0
    game_over = False
    tick = 0

    if draw:
        pg.init()
        pg.display.set_caption("Flappy Bird Game")
        clock = pg.time.Clock()
        screen = pg.display.set_mode((WORLD_X, WORLD_Y))
        screen.fill(BACKGROUND_COLOR)
        pg.draw.circle(screen, BIRD_COLOR, BIRD_START, BIRD_SIZE)
        if net is None:
            if pause(clock):
                bird_vel = JUMP_FORCE

    while True:
        if dist_traveled >= 100000:
            game_over = True
        # --- Pipes ---
        # make new pipes
        if pipe_timer >= (PIPE_SPACING + PIPE_WIDTH) // pipe_speed:
            x = WORLD_X + PIPE_WIDTH
            gap = random.randint(50 + PIPE_GAP, (WORLD_Y - 50) - PIPE_GAP)
            pipe = [x, gap]
            real_pipes.append(pipe)
            pipe_timer = 0
            pipe_speed += PIPE_SPEED_INC
        else:
            pipe_timer += 1

        # pipe movement
        dist_traveled += pipe_speed
        real_pipes = deque([[pipe[0] - pipe_speed, pipe[1]] for pipe in real_pipes])
        fake_pipes = deque([[pipe[0] - pipe_speed, pipe[1]] for pipe in fake_pipes])

        # bird movement
        if bird_vel < TERMINAL_VEL:
            bird_vel += GRAVITY
        bird_pos[1] += bird_vel

        # first real pipe
        first = real_pipes[0]

        # if pipe can no longer touch bird, move to fake pipes
        if first[0] + PIPE_WIDTH + BIRD_BB < bird_pos[0]:
            fake_pipes.append(real_pipes.popleft())

        # get rid of old offscreen pipes
        if fake_pipes:
            first = fake_pipes[0]
            if first[0] - pipe_speed <= -PIPE_WIDTH:
                fake_pipes.popleft()

        (b_x, b_y) = (bird_pos[0], bird_pos[1])
        (p_x, p_y) = (real_pipes[0][0], real_pipes[0][1])

        (p_x, p_height) = (
            real_pipes[0][0],
            real_pipes[0][1]
        )

        # network inputs as follows
        # 1: distance to pipe
        # 2: vertical velocity
        # 3: vertical distance to top pipe
        # 4: distance traveled
        # network output: sigmoid function to jump
        if net is not None:
<<<<<<< Updated upstream
            if net.activate([p_x - b_x, bird_vel, p_y - b_y, dist_traveled])[0] >= 0.5:
=======
            inputs = [p_x - b_x, 
                      bird_vel, 
                      p_y - b_y, 
                      dist_traveled,
                      0,
                      0,
                      0,
                      0,
                      0]

            if net.activate(inputs)[0] >= 0.5:
>>>>>>> Stashed changes
                bird_vel = JUMP_FORCE

        # find collision
        if b_y + BIRD_BB >= WORLD_Y:
            game_over = True
        elif b_x + BIRD_BB >= p_x:
            if b_x - BIRD_BB <= p_x + PIPE_WIDTH:
                if (b_y - BIRD_BB <= p_y - PIPE_GAP) or (b_y + BIRD_BB >= p_y):
                    game_over = True

        if draw:
            tick += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN and human:
                    if event.key == pg.K_SPACE:
                        bird_vel = JUMP_FORCE
                    elif event.key == pg.K_p:
                        if pause(clock):
                            bird_vel = JUMP_FORCE
            if tick % ticks_per_frame == 0:
                screen.fill(BACKGROUND_COLOR)
                pg.draw.circle(screen, BIRD_COLOR, bird_pos, BIRD_SIZE)
                for pipe in real_pipes + fake_pipes:
                    top_pipe = pg.Rect(pipe[0], 0, PIPE_WIDTH, pipe[1] - PIPE_GAP)
                    bottom_pipe = pg.Rect(pipe[0], pipe[1], PIPE_WIDTH, 10000)
                    pg.draw.rect(screen, PIPE_COLOR, top_pipe)
                    pg.draw.rect(screen, PIPE_COLOR, bottom_pipe)
                pg.display.flip()
                clock.tick(60)

            if game_over:
                if print_score:
                    print("score:", dist_traveled / (PIPE_WIDTH + PIPE_GAP))
                    pg.quit()
                    quit()
                pg.time.wait(250)
                bird_pos = BIRD_START.copy()
                bird_vel = 0
                real_pipes = deque([])
                fake_pipes = deque([])
                pipe_timer = float("inf")
                pipe_speed = 3
                dist_traveled = 0
                game_over = False
                screen.fill(BACKGROUND_COLOR)
                pg.draw.circle(screen, BIRD_COLOR, BIRD_START, BIRD_SIZE)
                if pause(clock):
                    bird_vel = JUMP_FORCE

        elif game_over:
            if print_score:
<<<<<<< Updated upstream
                print("score:", dist_traveled / (PIPE_WIDTH + PIPE_GAP))
            return dist_traveled / (PIPE_WIDTH + PIPE_GAP)
=======
                print("flappy score:", dist_traveled / (PIPE_WIDTH + PIPE_GAP))
            return dist_traveled / (PIPE_WIDTH + PIPE_GAP)
>>>>>>> Stashed changes
