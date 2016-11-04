#! /usr/bin/env python3

import math
import operator
import pygame
import random


class Individu:
    index = 0

    def __init__(self, surface, image_target, chromosome, transparent=True):
        self.id = Individu.index
        Individu.index += 1
        self.surface = surface
        self.chromosome = chromosome
        self.image_target = image_target
        self.transparent = transparent
        self.draw()
        self.fitness = self._distance_calc()



    def draw(self):
        # self.surface.fill(self.background)
        # self.surface.set_colorkey(self.background)
        white = (255, 255, 255, 255)
        black = (0, 0, 0, 255)
        self.surface.fill(white)
        # self.surface.set_colorkey(black)
        z = {}
        for i in range(len(self.chromosome)):
            index = self.chromosome[i][7]
            z[index] = i
        z_rank = sorted(z.keys())

        for i in z_rank:
            if self.transparent:
                s = pygame.Surface(self.surface.get_size())
                s.fill(white)
                s.set_colorkey(white)
            else:
                s = self.surface
            # chromosome : [gen, ge, ge, ... , gen]
            # gen        : [ R, G, B, A, x, y, radius, z]
            gen = self.chromosome[z[i]]
            color = (gen[0], gen[1], gen[2], gen[3])
            pos = (gen[4], gen[5])
            radius = gen[6]
            pygame.draw.circle(s, color, pos, radius)

            if self.transparent:
                s.set_alpha(color[3])

            self.surface.blit(s, (0, 0))

    def _image_raw_color(self, individu_=True):
        self.draw()
        width, height = self.surface.get_size()
        self.raw_color = []
        for x in range(width):
            for y in range(height):
                if individu_:
                    self.raw_color.append(self.surface.get_at((x, y)))
                else:
                    self.raw_color.append(self.image_target.get_at((x, y)))
        return self.raw_color

    def _distance_calc(self):
        raw_color = self._image_raw_color()
        target_raw_color = self._image_raw_color(False)
        distance = 0
        for color in range(0, len(raw_color), 2):
            dist = 0
            for i in range(len(raw_color[color]) - 1):
                dist += math.fabs(raw_color[color][i] - target_raw_color[color][i])
            distance += dist

        return distance


def new_gen(surface, grayscale=False):
    surface_size = surface.get_size()
    max_color = 255
    min_color = 0
    max_x = surface_size[0]
    min_x = 0
    max_y = surface_size[1]
    min_y = 0
    max_radius = min(surface_size) / 4
    min_radius = 0
    if not grayscale:
        gen = [
            random.randrange(min_color, max_color),  # R
            random.randrange(min_color, max_color),  # G
            random.randrange(min_color, max_color),  # B
            random.randrange(min_color, max_color),  # A
            random.randrange(min_x, max_x),  # x
            random.randrange(min_y, max_y),  # y
            random.randrange(min_radius, max_radius),  # radius
            random.random(),  # z
        ]
    else:
        color = random.randrange(min_color, max_color)
        gen = [
            color,  # R
            color,  # G
            color,  # B
            random.randrange(min_color, max_color),  # A
            random.randrange(min_x, max_x),  # x
            random.randrange(min_y, max_y),  # y
            random.randrange(min_radius, max_radius),  # radius
            random.random(),  # z
        ]
    return gen


def new_chromosome(surface, total_circle, grayscale=False):
    chromosome = []
    for i in range(total_circle):
        chromosome.append(new_gen(surface, grayscale))
    return chromosome


def new_population(surface, population_size, image_target, total_circle, grayscale=False, transparent=True):
    population = []
    for i in range(population_size):
        population.append(Individu(surface, image_target, new_chromosome(surface, total_circle, grayscale), transparent))
    return population


def crossover(surface, parent1, parent2, image_target, transparent=True):
    parent_chromosome1 = parent1.chromosome
    parent_chromosome2 = parent2.chromosome
    child_chromosome1 = []
    child_chromosome2 = []
    cross_point = random.randrange(0, len(parent_chromosome1))

    for i in range(len(parent_chromosome1)):
        if i < cross_point:
            child_chromosome1.append(parent_chromosome1[i])
            child_chromosome2.append(parent_chromosome2[i])
        else:
            child_chromosome1.append(parent_chromosome2[i])
            child_chromosome2.append(parent_chromosome1[i])
    child1 = Individu(surface, image_target, child_chromosome1, transparent)
    child2 = Individu(surface, image_target, child_chromosome2, transparent)
    return child1, child2


def population_crossover(surface, population, image_target, crossover_rate=0.5, transparent=True):
    parent1 = None
    parent2 = None
    offspring = []

    for candidate in population:
        r = random.random()
        if r > crossover_rate:
            if parent1 is None:
                parent1 = candidate
            else:
                parent2 = candidate
        if parent2 is not None:
            child1, child2 = crossover(surface, parent1, parent2, image_target, transparent)
            offspring.append(child1)
            offspring.append(child2)
            parent1 = None
            parent2 = None
    total_population = population + offspring
    return total_population


def mutation(surface, parent, image_target, grayscale=False, transparent=True):
    parent_chromosome = parent.chromosome
    child_chromosome = []
    mutation_point = random.randrange(0, len(parent_chromosome))

    for i in range(len(parent_chromosome)):
        if i != mutation_point:
            child_chromosome.append(parent_chromosome[i])
        else:
            child_chromosome.append(new_gen(surface, grayscale))
    child = Individu(surface, image_target, child_chromosome, transparent)
    return child


def population_mutation(surface, population, image_target, mutation_rate=0.5, grayscale=False, transparent=True):
    offspring = []

    for candidate in population:
        r = random.random()
        if r > mutation_rate:
            child = mutation(surface, candidate, image_target, grayscale, transparent)
            offspring.append(child)
    total_population = population + offspring
    return total_population


def selection(population, population_size):
    if len(population) > population_size:
        diff = len(population) - population_size
        population.sort(key=operator.attrgetter('fitness'))
        for i in range(diff):
            pop = population.pop()
    return population


def best_individu(population):
    best_candidate = population.index(min(population, key=operator.attrgetter('fitness')))
    return population[best_candidate]
