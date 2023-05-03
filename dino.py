# Flappy bird clone
import random
from collections import deque

import pygame as pg

random.seed(0)

# sim parameters
WORLD_X = 1000
WORLD_Y = 200

# drawing parameters
DINO_SIZE = 20
DINO_COLOR = (99, 99, 99)
PIPE_COLOR = (71, 71, 71)
BACKGROUND_COLOR = (224, 224, 224)

# game parameters
GRAVITY = 0.4
JUMP_FORCE = -10
TERMINAL_VEL = 60
DINO_START = [DINO_SIZE + 20, WORLD_Y - DINO_SIZE]

# pipe parameters
PIPE_SPEED = 5
PIPE_SPEED_INC = 0.1
PIPE_WIDTH = (20, 60)
PIPE_HEIGHT = (20, 60)


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
    dino_pos = DINO_START.copy()
    dino_vel = 0
    pipe_speed = PIPE_SPEED
    real_pipes = deque([])
    fake_pipes = deque([])
    pipe_timer = float("inf")
    dist_traveled = 0
    game_over = False
    tick = 0
    obstacle_spacing = random.randint(300, 800)
    obstacle_height = random.randint(20, 60)
    obstacle_width = random.randint(20, 60)

    if draw:
        pg.init()
        pg.display.set_caption("Flappy Bird Game")
        clock = pg.time.Clock()
        screen = pg.display.set_mode((WORLD_X, WORLD_Y))
        screen.fill(BACKGROUND_COLOR)
        pg.draw.circle(screen, DINO_COLOR, DINO_START, DINO_SIZE)
        if net is None:
            if pause(clock):
                dino_vel = JUMP_FORCE

    while True:
        if dist_traveled >= 1000000:
            game_over = True
            pg.quit()
            return dist_traveled
        # --- Pipes ---
        # make new pipes
        if pipe_timer >= (obstacle_spacing + obstacle_width) // pipe_speed:
            obstacle_spacing = random.randint(300, 800)
            obstacle_height = random.randint(20, 60)
            obstacle_width = random.randint(20, 60)
            x = WORLD_X + obstacle_width
            pipe = [x, obstacle_width, obstacle_height]
            real_pipes.append(pipe)
            pipe_timer = 0
            pipe_speed += PIPE_SPEED_INC
        else:
            pipe_timer += 1

        # pipe movement
        dist_traveled += pipe_speed
        real_pipes = deque(
            [[pipe[0] - pipe_speed, pipe[1], pipe[2]] for pipe in real_pipes]
        )
        fake_pipes = deque(
            [[pipe[0] - pipe_speed, pipe[1], pipe[2]] for pipe in fake_pipes]
        )

        # bird movement
        if dino_pos[1] + DINO_SIZE + dino_vel >= WORLD_Y:
            dino_pos[1] = WORLD_Y - DINO_SIZE
            dino_vel = 0
        elif dino_vel < TERMINAL_VEL:
            dino_vel += GRAVITY
        dino_pos[1] += dino_vel

        # first real pipe
        (d_x, d_y) = (dino_pos[0], dino_pos[1])
        (p_x, p_height, p_width) = (
            real_pipes[0][0],
            real_pipes[0][1],
            real_pipes[0][2],
        )

        # if pipe can no longer touch bird, move to fake pipes
        if p_x + p_width + DINO_SIZE < d_x:
            fake_pipes.append(real_pipes.popleft())
            (p_x, p_height, p_width) = (
                real_pipes[0][0],
                real_pipes[0][1],
                real_pipes[0][2],
            )

        # get rid of old offscreen pipes
        if fake_pipes:
            if fake_pipes[0][0] - pipe_speed <= -fake_pipes[0][1]:
                fake_pipes.popleft()

        # network inputs as follows
        # 1: horizontal distance to 1st pipe
        # 2: 1st pipe height
        # 3: 1st pipe width
        # 4: horizontal distance to 2nd pipe
        # 5: 2nd pipe height
        # 6: 2nd pipe width
        # 7: distance traveled
        # network output: sigmoid function to jump
        if net is not None:
            if d_y == (WORLD_Y - DINO_SIZE):
                try:
                    (p2_x, p2_height, p2_width) = (
                        real_pipes[1][0],
                        real_pipes[1][1],
                        real_pipes[1][2],
                    )
                except IndexError:
                    (p2_x, p2_height, p2_width) = (float("inf"), 0, 0)
                inputs = [
                    p_x - d_x,
                    dino_vel,
                    p_height - d_y,
                    dist_traveled,
                    p_height,
                    p_width,
                    p2_x - d_x,
                    p2_height,
                    p2_width
                ]
                if net.activate(inputs)[0] >= 0.5:
                    dino_vel = JUMP_FORCE

        # find collision
        if d_x + DINO_SIZE >= p_x:
            if d_x - DINO_SIZE <= p_x + p_width:
                if d_y + DINO_SIZE >= WORLD_Y - p_height:
                    game_over = True

        if draw:
            tick += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    quit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE and d_y == (WORLD_Y - DINO_SIZE):
                        dino_vel = JUMP_FORCE
                    elif event.key == pg.K_p:
                        if pause(clock) and d_y == (WORLD_Y - DINO_SIZE):
                            dino_vel = JUMP_FORCE
            if tick % ticks_per_frame == 0:
                screen.fill(BACKGROUND_COLOR)
                pg.draw.circle(screen, DINO_COLOR, dino_pos, DINO_SIZE)
                for pipe in real_pipes + fake_pipes:
                    pipe = pg.Rect(pipe[0], WORLD_Y - pipe[2], pipe[1], pipe[2])
                    pg.draw.rect(screen, PIPE_COLOR, pipe)
                pg.display.flip()
                clock.tick(60)

            if game_over:
                if print_score:
                    print("score:", dist_traveled)
                    pg.quit()
                    quit()
        
        elif game_over:
            if print_score:
                print("dino score:", dist_traveled)
            return dist_traveled
    

if __name__ == "__main__":
    run_instance(human=True)
