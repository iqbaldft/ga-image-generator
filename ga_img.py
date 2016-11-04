#! /usr/bin/env python3

import sys
import pygame
import random


def main():
    pygame.init()

    size = (128, 200)
    display_surface = pygame.display.set_mode(size)
    pygame.display.set_caption('nyaaa')
    WHITE = (255, 255, 255)
    display_surface.fill(WHITE)
    # pygame.draw.circle(display_surface, (0,0,255), (20,20), 20, 0)
    play(display_surface)


def play(display_surface):
    x = 20
    y = 20
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # DO something before update

        # Testing purpose, delete later
        x += 20
        y += 20
        pygame.draw.circle(display_surface, (0, 0, 255), (x, y), 20)
        pygame.draw.circle()
        pygame.time.delay(100)
        if x % 50 == 0:
            display_surface.fill((255, 255, 255))
        # ???

        pygame.display.update()


def new_gen(surface):
    surface_size = surface.get_size()
    max_color = 255
    min_color = 0
    max_x = surface_size[0]
    min_x = 0
    max_y = surface_size[1]
    min_y = 0
    max_radius = min(surface_size)
    min_radius = 0
    chromosome = [
        random.randrange(min_color, max_color),     # R
        random.randrange(min_color, max_color),     # G
        random.randrange(min_color, max_color),     # B
        random.randrange(min_color, max_color),     # A
        random.randrange(min_x, max_x),             # x
        random.randrange(min_y, max_y),             # y
        random.randrange(min_radius, max_radius),   # radius
        random.random(),                            # z
    ]
    return chromosome


def new_chromosome(surface, total_circle):
    chromosome = []
    for i in range(total_circle):
        chromosome.append(new_gen(surface))
    return chromosome


def ga_init(surface, population_size, total_circle):
    population = []
    for i in range(population_size):
        population.append(new_chromosome(surface, total_circle))
    return population


def crossover(population, crossover_rate=0.5):
    parent1 = None
    parent2 = None
    new_population = []

    for candidate in population:
        r = random.random()
        if r > crossover_rate:
            if parent1 is None:
                parent1 = candidate
            else:
                parent2 = candidate
        if parent2 is not None:
            child1 = []
            child2 = []
            cross_point = random.randrange(0, len(parent1))
            for i in range(len(parent1)):
                if i < cross_point:
                    child1.append(parent1[i])
                    child2.append(parent2[i])
                else:
                    child1.append(parent2[i])
                    child2.append(parent1[i])
            new_population.append(child1)
            new_population.append(child2)
            parent1 = None
            parent2 = None
    total_population = population + new_population
    return total_population


def mutation(population, surface, total_circle, mutation_rate=0.5):
    new_population = []

    for candidate in population:
        r = random.random()
        if r > mutation_rate:
            parent = candidate
            child = []
            mutation_point = random.randrange(0, len(parent))

            for i in range(len(parent)):
                if i != mutation_point:
                    child.append(parent[i])
                else:
                    child.append(new_chromosome(surface, total_circle))
            new_population.append(child)
    total_population = population + new_population
    return total_population


def clean_duplicates(population):
    new_population = []
    for chromosome in population:
        if chromosome not in new_population:
            new_population.append(chromosome)
    return new_population


def individu_translate(surface, chromosome):
    size = surface.get_size()
    white = (255, 255, 255, 255)
    surface.fill(white)
    z = {}
    for i in range(chromosome):
        z[chromosome[i][7]] = i
    z_rank = sorted(z.keys())

    for i in z_rank:
        # chromosome : [gen, ge, ge, ... , gen]
        # gen        : [ R, G, B, A, x, y, radius, z]
        gen = chromosome[i]
        color = (gen[0], gen[1], gen[2], gen[3])
        pos = (gen[4], gen[5])
        radius = gen[6]
        pygame.draw.circle(surface, color, pos, radius)

    individu = []
    for x in range(size[0]):
        for y in range(size[1]):
            individu.append(surface.get_at((x, y)))
    return individu


def image_translate(image):
    raw_image = []
    size = image.get_size()
    for x in size[0]:
        for y in size[1]:
            raw_image.append(image.get_at((x, y)))
    return raw_image


def fitness_calculation(surface, population, image):
    # TODO fitness calculation algorithm
    # tiap pixel gambar hasil dibandingkan rgb-nya dengan tujuan
    fitness = []
    raw_image = image_translate(image)
    population_individu = []



    for chromosome in population:
        population_individu.append(individu_translate(surface, chromosome))





def selection(population, population_size):
    # TODO selection algorithm
    print('belum... udah ngantuk dulu, ikan bobo... lanjut besok lagi yaa...')


if __name__ == '__main__':
    main()
