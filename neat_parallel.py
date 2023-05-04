import multiprocessing
import os

import neat

import flappy as flap
import dino

import csv

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

# Basic network structure
# inputs:
# 1. distance to pipe,
# 2. vertical velocity,
# 3. vertical distance to top pipe,
# 4. distance traveled
# outputs:
# 1. jump if >= 0.5

def eval_genome_dino(genome, config):
    test = neat.nn.FeedForwardNetwork.create(genome, config)
    score = dino.run_instance(net=test)
    return score

def eval_genome_flap(genome, config):
    test = neat.nn.FeedForwardNetwork.create(genome, config)
    score = flap.run_instance(net=test)
    return score

# Main function for NEAT
# Inputs:
#   game: one of {"flappy", "dino"} to use that game
#   config_file: a provided NEAT config file
#   save: whether to save the results to files
#   draw_final: whether to draw the final network playing the game
# Outputs:
#   The winning neural network

def run_flap(config_file):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    p = neat.Population(config)
    i = 0

    while True:
        gen = int(input("How many generations: "))
        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        # Run for up to 300 generations.
        pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome_flap)
        winner = p.run(pe.evaluate, gen)

        # Display the winning genome.
        print(f"\nBest genome:\n{winner}")

        # Show most fit genome playing flappy bird!
        winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

        # draw it or allow it to keep going
        if i == 0:
            print("NOTE: Drawing will end the current population")
            i+=1
        a = input("Draw? Y/N\n")
        if a == "Y":
            b = flap.run_instance(net=winner_net, ticks_per_frame=3, draw=True, print_score=True)
        else:
            b = flap.run_instance(net=winner_net, ticks_per_frame=3, draw=False, print_score=True)

def run_flap_data(config_file, gen):
    # function to do 30 runs to aggregate generation data

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    j = 0
    data = []
    while j < 5:
        i=0
        p = neat.Population(config)
        while i<gen:
            # Add a stdout reporter to show progress in the terminal.
            p.add_reporter(neat.StdOutReporter(False))
            stats = neat.StatisticsReporter()
            p.add_reporter(stats)

            # Run for up to 300 generations.
            pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome_flap)
            winner = p.run(pe.evaluate, 1)

            # Display the winning genome.
            print(f"\nBest genome:\n{winner}")

            # Show most fit genome playing flappy bird!
            winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
            b = flap.run_instance(net=winner_net, ticks_per_frame=3, draw=False, print_score=True)
            if j == 0:
                data.append([i, b])
            else:
                data[i][1] += b
            i += 1
        j+=1

    for i in data:
        i[1] = i[1]/5

    # opening the csv file in 'w+' mode
    file = open('flap_data2.csv', 'w+', newline ='')
    
    # writing the data into the file
    with file:
        write = csv.writer(file)
        write.writerows(data)

def run_dino_data(config_file, gen):
    # function to do 30 runs to aggregate generation data

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    j = 0
    data = []
    while j < 30:
        i=0
        p = neat.Population(config)
        while i<gen:
            # Add a stdout reporter to show progress in the terminal.
            p.add_reporter(neat.StdOutReporter(False))
            stats = neat.StatisticsReporter()
            p.add_reporter(stats)

            # Run for up to 300 generations.
            pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome_dino)
            winner = p.run(pe.evaluate, 1)

            # Display the winning genome.
            print(f"\nBest genome:\n{winner}")

            # Show most fit genome playing flappy bird!
            winner_net = neat.nn.FeedForwardNetwork.create(winner, config)
            b = dino.run_instance(net=winner_net, ticks_per_frame=3, draw=False, print_score=True)
            if j == 0:
                data.append([i, b])
            else:
                data[i][1] += b
            i += 1
        j+=1

    for i in data:
        i[1] = i[1]/30

    # opening the csv file in 'w+' mode
    file = open('dino_data.csv', 'w+', newline ='')
    
    # writing the data into the file
    with file:
        write = csv.writer(file)
        write.writerows(data)
    
def run_dino(config_file):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    p = neat.Population(config)
    i = 0

    while True:
        gen = int(input("How many generations: "))
        # Add a stdout reporter to show progress in the terminal.
        p.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        p.add_reporter(stats)

        # Run for up to 300 generations.
        pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome_dino)
        winner = p.run(pe.evaluate, gen)

        # Display the winning genome.
        print(f"\nBest genome:\n{winner}")

        # Show most fit genome playing flappy bird!
        winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

        c = dino.run_instance(net=winner_net, ticks_per_frame=3, draw=True, print_score=True)
        print("Dino score:", str(c))

def run_flap_dino(config_file):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    tot = 10
    data = []
    j = 0
    while j < tot:
        p = neat.Population(config)
        it = 0

        while it < 30:
            # Add a stdout reporter to show progress in the terminal.
            p.add_reporter(neat.StdOutReporter(False))
            stats = neat.StatisticsReporter()
            p.add_reporter(stats)

            # Run for up to 300 generations.
            pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome_flap)
            winner = p.run(pe.evaluate, 1)

            # Display the winning genome.
            print(f"\nBest genome:\n{winner}")

            # Show most fit genome playing flappy bird!
            winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

            b = flap.run_instance(net=winner_net, ticks_per_frame=1, draw=False, print_score=True)
            
            if j == 0:
                data.append([it, b])
            else:
                data[it][1] += b
            it += 1

        while it < 50:
            # Run for up to 300 generations.
            pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome_dino)
            winner = p.run(pe.evaluate, 1)

            # Display the winning genome.
            print(f"\nBest genome:\n{winner}")

            # Show most fit genome playing flappy bird!
            winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

            d = dino.run_instance(net=winner_net, ticks_per_frame=1, draw=False, print_score=True)

            if j == 0:
                data.append([it, b])
            else:
                data[it][1] += d
            it += 1

        j += 1


    # opening the csv file in 'w+' mode
    file = open('flappy_dino2.csv', 'w+', newline ='')
    for i in data:
        i[1] = i[1]/tot
    
    # writing the data into the file
    with file:
        write = csv.writer(file)
        write.writerows(data)

def run_dino_flap(config_file):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file,
    )

    tot = 10
    data = []
    j = 0
    while j < tot:
        p = neat.Population(config)
        it = 0

        while it < 30:
            # Add a stdout reporter to show progress in the terminal.
            p.add_reporter(neat.StdOutReporter(False))
            stats = neat.StatisticsReporter()
            p.add_reporter(stats)

            # Run for up to 300 generations.
            pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome_dino)
            winner = p.run(pe.evaluate, 1)

            # Display the winning genome.
            print(f"\nBest genome:\n{winner}")

            # Show most fit genome playing flappy bird!
            winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

            b = dino.run_instance(net=winner_net, ticks_per_frame=1, draw=False, print_score=True)
            
            if j == 0:
                data.append([it, b])
            else:
                data[it][1] += b
            it += 1

        while it < 50:
            # Run for up to 300 generations.
            pe = neat.ParallelEvaluator(multiprocessing.cpu_count(), eval_genome_flap)
            winner = p.run(pe.evaluate, 1)

            # Display the winning genome.
            print(f"\nBest genome:\n{winner}")

            # Show most fit genome playing flappy bird!
            winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

            d = flap.run_instance(net=winner_net, ticks_per_frame=1, draw=False, print_score=True)

            if j == 0:
                data.append([it, b])
            else:
                data[it][1] += d
            it += 1

        j += 1

    # opening the csv file in 'w+' mode
    file = open('dino_flappy.csv', 'w+', newline ='')
    for i in data:
        i[1] = i[1]/tot
    
    # writing the data into the file
    with file:
        write = csv.writer(file)
        write.writerows(data)

if __name__ == "__main__":
    run_dino_flap("config_default")
