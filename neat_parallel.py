import multiprocessing
import os

import neat

import flappy as flap

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

# Basic network structure
# inputs:
# 1. distance to pipe,
# 2. vertical velocity,
# 3. vertical distance to top pipe,
# 4. distance traveled
# outputs:
# 1. jump if >= 0.5


def eval_genome(genome, config):
    test = neat.nn.FeedForwardNetwork.create(genome, config)
    score = flap.run_instance(net=test)
    return score


def run(config_file):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    p = neat.Population(config)

    while True:
        gen = int(input("How many generations: "))
        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        # Run for up to 300 generations.
        pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome)
        winner = p.run(pe.evaluate, gen)

        # Display the winning genome.
        print(f"\nBest genome:\n{winner}")

        # Show most fit genome playing flappy bird!
        winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
        b = flap.run_instance(net=winner_net, ticks_per_frame=3, draw=False, print_score=True)
    

if __name__ == "__main__":
    run("config_flappy")
