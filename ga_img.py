#! /usr/bin/env python3

import os
import sys

import pygame

import ga


def main():
    """
    the main method for initialization components and more...
    """
    # initialization
    pygame.init()

    # load image target
    os.chdir('/home/iko/Pictures/')
    image_target = pygame.image.load('iko_mini.jpg')
    grayscale = False
    transparent = True

    # setting surface
    width, height = image_target.get_size()
    surface = pygame.display.set_mode((width*2, height))
    pygame.display.set_caption('GA')

    # showing image target in the beginning of program
    surface.blit(image_target, (width, 0))
    pygame.display.flip()

    # setting ga parameter
    ga_parameter = {
        'population_size': 5,
        'crossover_rate': 0.5,
        'mutation_rate': 0.5,
        'total_circle': 128,
        'max_iteration': 150000,
    }

    population = ga.new_population(surface, ga_parameter['population_size'], image_target, ga_parameter['total_circle'],
                                   grayscale, transparent)

    # splitting initialization and running, for readability reason
    play(surface, image_target, population, ga_parameter, grayscale, transparent)


def play(surface, image_target, population, ga_parameter, grayscale, transparent):
    """
    running the GA !!!
    finally i could evolve more
    :param surface: pygame surface
    :param image_target: pygame image the target of reproduce
    :param population: current population
    :param ga_parameter: parameter of genetic algorithm
    :param grayscale: boolean is the image grayscale ?
    :param transparent: boolean do you want the circle to be transparent ?
    """
    for iteration in range(ga_parameter['max_iteration']):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.K_ESCAPE:
                # exited in the middle of process
                pygame.image.save(surface, 'interrupt, iter : {}.jp'.format(iteration))
                pygame.quit()
                sys.exit()

        pygame.display.set_caption('iter: {}'.format(iteration))

        if iteration < ga_parameter['max_iteration']:
            # crossover
            # print('{}:cross'.format(iteration))
            population = ga.population_crossover(surface, population, image_target, ga_parameter['crossover_rate'],
                                                 grayscale, transparent)
            # mutation
            # print('{}:mutate'.format(iteration))
            population = ga.population_mutation(surface, population, image_target, ga_parameter['mutation_rate'],
                                                grayscale, transparent)
            # selection
            # print('{}:select'.format(iteration))
            population = ga.selection(population, ga_parameter['population_size'])
            # best
            # print('{}:best'.format(iteration))
            best = ga.best_individu(population)
            best.draw()
            # print('i{}:p{}'.format(iteration, len(population)))
        else:
            break
        width, height = surface.get_size()
        surface.blit(image_target, (width/2, 0))
        pygame.display.update()
        # pygame.display.flip()
    pygame.image.save(surface, 'hasil.png')
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()
