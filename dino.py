# Flappy bird clone
import random
from collections import deque

import pygame as pg

random.seed(0)

# sim parameters
WORLD_X = 1000
WORLD_Y = 200

# drawing parameters
BIRD_SIZE = 20
BIRD_COLOR = (99, 99, 99)
PIPE_COLOR = (71, 71, 71)
BACKGROUND_COLOR = (224, 224, 224)

# game parameters
GRAVITY = 0.4
JUMP_FORCE = -10
TERMINAL_VEL = 60
BIRD_BB = 25
GROUND = WORLD_Y - 10
BIRD_START = [20, GROUND - BIRD_SIZE]

# pipe parameters
PIPE_SPEED = 5
PIPE_SPEED_INC = 0.1


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
    obstacle_spacing = random.randint(100, 500)
    obstacle_width = random.randint(20, 60)

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
        if pipe_timer >= (obstacle_spacing + obstacle_width) // pipe_speed:
            x = WORLD_X + obstacle_width
            gap = WORLD_Y - random.randint(10, 50)
            pipe = [x, gap, obstacle_width]
            real_pipes.append(pipe)
            pipe_timer = 0
            pipe_speed += PIPE_SPEED_INC
            obstacle_spacing = random.randint(200, 700)
            obstacle_width = random.randint(20, 60)
        else:
            pipe_timer += 1

        # pipe movement
        dist_traveled += pipe_speed
        real_pipes = deque([[pipe[0] - pipe_speed, pipe[1]] for pipe in real_pipes])
        fake_pipes = deque([[pipe[0] - pipe_speed, pipe[1]] for pipe in fake_pipes])

        # bird movement
        if bird_pos[1] >= BIRD_START[1]:
            bird_pos[1] = BIRD_START[1]
        elif bird_vel < TERMINAL_VEL:
            bird_vel += GRAVITY
        bird_pos[1] += bird_vel

        # first real pipe
        first = real_pipes[0]

        # if pipe can no longer touch bird, move to fake pipes
        if first[0] + obstacle_width + BIRD_BB < bird_pos[0]:
            fake_pipes.append(real_pipes.popleft())

        # get rid of old offscreen pipes
        if fake_pipes:
            first = fake_pipes[0]
            if first[0] - pipe_speed <= -obstacle_width:
                fake_pipes.popleft()

        (b_x, b_y) = (bird_pos[0], bird_pos[1])
        (p_x, p_y) = (real_pipes[0][0], real_pipes[0][1])

        # network inputs as follows
        # 1: distance to pipe
        # 2: vertical velocity
        # 3: vertical distance to top pipe
        # 4: distance traveled
        # network output: sigmoid function to jump
        if net is not None:
            if net.activate([p_x - b_x, bird_vel, p_y - b_y, dist_traveled])[0] >= 0.5 and bird_pos[1] >= BIRD_START[1] - 3:
                bird_vel = JUMP_FORCE

        # find collision
        elif b_x + BIRD_BB >= p_x:
            if b_x - BIRD_BB <= p_x + obstacle_width:
                if (b_y + BIRD_BB >= p_y):
                    game_over = True

        if draw:
            tick += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN and human:
                    if event.key == pg.K_SPACE and bird_pos[1] >= BIRD_START[1] - 5:
                        bird_vel = JUMP_FORCE
                    elif event.key == pg.K_p and bird_pos[1] >= BIRD_START[1] - 5:
                        if pause(clock):
                            bird_vel = JUMP_FORCE
            if tick % ticks_per_frame == 0:
                screen.fill(BACKGROUND_COLOR)
                pg.draw.circle(screen, BIRD_COLOR, bird_pos, BIRD_SIZE)
                for pipe in real_pipes + fake_pipes:
                    bottom_pipe = pg.Rect(pipe[0], pipe[1], obstacle_width, 10000)
                    pg.draw.rect(screen, PIPE_COLOR, bottom_pipe)
                pg.display.flip()
                clock.tick(60)

            if game_over:
                if print_score:
                    print("score:", dist_traveled / obstacle_width)
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
                print("score:", dist_traveled / obstacle_width)
            return dist_traveled / obstacle_width
        

# if __name__ == "__main__":
#     run_instance(human=True)
