import multiprocessing
import os

import neat

import dino
import flappy as flap

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"
os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"

# Basic network structure
# inputs:
# 1. distance to pipe,
# 2. vertical velocity,
# 3. vertical distance to top pipe,
# 4. distance traveled
# outputs:
# 1. jump if >= 0.5


def eval_genome_flap(genome, config):
    test = neat.nn.FeedForwardNetwork.create(genome, config)
    score = flap.run_instance(net=test)
    return score


def eval_genome_dino(genome, config):
    test = neat.nn.FeedForwardNetwork.create(genome, config)
    score = dino.run_instance(net=test)
    return score


# Main function for NEAT
# Inputs:
#   game: one of {"flappy", "dino"} to use that game
#   config_file: a provided NEAT config file
#   save: whether to save the results to files
#   draw_final: whether to draw the final network playing the game
# Outputs:
#   The winning neural network
def run(game, config_file, save=False, draw_final=False):
    if game == "flappy":
        eval = eval_genome_flap
    else:
        eval = eval_genome_dino

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    # Population of networks
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run for up to 300 generations.
    pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval)
    winner = p.run(pe.evaluate, 500)

    # Display the winning genome.
    print(f"\nBest genome:\n{winner}")
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
    if save:
        stats.save()
    if game == "flappy":
        flap.run_instance(net=winner_net, draw=True, ticks_per_frame=1)
    else:
        dino.run_instance(net=winner_net, draw=True, ticks_per_frame=1)
    return winner_net


if __name__ == "__main__":
    run(game="flappy", config_file="config_flappy", save=True, draw_final=False)
