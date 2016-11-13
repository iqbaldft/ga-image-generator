#! /usr/bin/env python3

import math
import operator
import random

import pygame


class Individu:
    """
    class for each individual in this genetic algorithm
    """
    index = 0
    target_raw = None

    def __init__(self, surface, image_target, chromosome, grayscale=False, transparent=True):
        """

        :param surface: pygame surface
        :param image_target: pygame image target image to reproduce
        :param chromosome: the chromosome of the individu,
        you could create this chromosome using function new_chromosome in this file
        :param grayscale: boolean if the image target is grayscale
        :param transparent: boolean to determine if the circles of reproduction using transparency or not
        """
        self.id = Individu.index
        Individu.index += 1
        self.surface = surface
        self.chromosome = chromosome
        self.image_target = image_target
        self.transparent = transparent
        self.grayscale = grayscale

        self.draw()
        self.fitness = self._distance_calc()

    def draw(self):
        """
        method for drawing the circles to the surface
        Note that this method does not update the surface
        it means the surface will still as it is even after this method finished running
        use pygame.display.update() or pygame.display.flip() to update the surface display
        """
        white = (255, 255, 255, 255)
        self.surface.fill(white)

        z = {}
        for i in range(len(self.chromosome)):
            index = self.chromosome[i][7]
            z[index] = i
        z_rank = sorted(z.keys())
        # z_rank is used so the circles will be drawn with the order of z_rank
        # higher z_rank means the circles will be on top of another lower z_rank circles
        for i in z_rank:
            width, height = self.surface.get_size()
            s = pygame.Surface((width / 2, height))
            if self.transparent:
                s.fill(white)
                s.set_colorkey(white)
            # chromosome : [gen, ge, ge, ... , gen]
            # gen        : [ R, G, B, A, x, y, radius, z]
            gen = self.chromosome[z[i]]
            color = (gen[0], gen[1], gen[2], gen[3])  # R G B A
            pos = (gen[4], gen[5])  # x, y
            radius = gen[6]
            pygame.draw.circle(s, color, pos, radius)

            if self.transparent:
                s.set_alpha(color[3])

            self.surface.blit(s, (0, 0))

    def _image_raw_color(self, individu_=True):
        """
        convert the image to list of color
        :param individu_: boolean using the generated image (True) or using image target (False)
        :return: list of color in order [(R, G, B, A), ...] -> i.e. [(255, 255, 255, 255), (0,0,0,128), ... ]
        """
        if individu_ :
            self.draw()
        width, height = self.surface.get_size()
        self.raw_color = []
        for x in range(width // 2):  # the display is split by 2 to display generated and target image
            for y in range(height):
                if individu_:
                    self.raw_color.append(self.surface.get_at((x, y)))
                else:
                    self.raw_color.append(self.image_target.get_at((x, y)))
        return self.raw_color

    def _distance_calc(self):
        """
        calculate the distance/similarity of generated image and the target image
        :return: integer sum of all the distance of each color of the pixel
        """
        raw_color = self._image_raw_color()
        if Individu.target_raw is None:
            Individu.target_raw = self._image_raw_color(False)

        distance = 0
        for color in range(0, len(raw_color), 2):
            if not self.grayscale:
                for i in range(len(raw_color[color]) - 1):
                    distance += math.fabs(raw_color[color][i] - Individu.target_raw[color][i])
            else:
                distance += math.fabs(raw_color[color][0] - Individu.target_raw[color][0])
        return distance


def new_gene(surface, grayscale=False):
    """
    create a new random gene needed for chromosome
    :param surface: pygame surface
    :param grayscale: boolean if the image is grayscale
    :return: list of a gene -> [ R, G, B, A, x, y, radius, z]
    """
    surface_size = surface.get_size()
    max_color = 255
    min_color = 0
    max_x = surface_size[0] // 2
    min_x = 0
    max_y = surface_size[1]
    min_y = 0
    max_radius = min(surface_size) // 4
    min_radius = 0
    gene = None
    if not grayscale:
        gene = [
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
        gene = [
            color,  # R
            color,  # G
            color,  # B
            random.randrange(min_color, max_color),  # A
            random.randrange(min_x, max_x),  # x
            random.randrange(min_y, max_y),  # y
            random.randrange(min_radius, max_radius),  # radius
            random.random(),  # z
        ]
    return gene


def new_chromosome(surface, total_circle, grayscale=False):
    """
    create a new random chromosome
    :param surface: pygame surface
    :param total_circle: integer how many circle do you want to be there ?
    :param grayscale: boolean if the image is grayscale
    :return: list of a chromosome -> [gene, gene,  ... ] which gene is [ R, G, B, A, x, y, radius, z]
    """
    chromosome = []
    for i in range(total_circle):
        chromosome.append(new_gene(surface, grayscale))
    return chromosome


def new_population(surface, population_size, image_target, total_circle, grayscale=False, transparent=True):
    """
    create a new population
    :param surface: pygame surface
    :param population_size: integer how many individual do you want to be in population ?
    :param image_target: pygame image target image to reproduce
    :param total_circle: integer how many circle do you want to be there ?
    :param grayscale: boolean if the image is grayscale
    :param transparent: boolean to determine if the circles of reproduction using transparency or not
    :return: list of a population -> [Individu, Individu, Individu, ... ]
    """
    population = []
    for i in range(population_size):
        population.append(
            Individu(surface, image_target, new_chromosome(surface, total_circle, grayscale), grayscale, transparent))
    return population


def choose_candidates(population, rate):
    fitnesses = [i.fitness for i in population]
    total_fitness = sum(fitnesses)
    roulette_wheel = []

    for i in range(len(fitnesses)):
        roulette_wheel.append((fitnesses[i] / total_fitness) + (sum(roulette_wheel) - sum(roulette_wheel[:-1])))
    candidates = []
    while len(candidates) < (len(population) * rate):
        r = random.random()
        for i in range(len(roulette_wheel)):
            if r < roulette_wheel[i]:
                candidates.append(population[i])
                break
    return candidates


def crossover(surface, parent1, parent2, image_target, grayscale=False, transparent=True):
    """
    function to add a couple of new children from a couple of parents with (currently) one point crossover method
    :param surface: pygame surface
    :param parent1: Individu the first parent (father ?)
    :param parent2: Individu the second parent (mother ?)
    :param image_target: pygame image target image to reproduce
    :param grayscale: boolean if the image is grayscale
    :param transparent: boolean to determine if the circles of reproduction using transparency or not
    :return: a couple of cute little children which has a chromosome cross from their parents -> (Individu, Individu)
    """
    parent_chromosome1 = parent1.chromosome
    parent_chromosome2 = parent2.chromosome
    cross_point = random.randrange(0, len(parent_chromosome1))

    child_chromosome1 = parent_chromosome1[:cross_point] + parent_chromosome2[cross_point:]
    child_chromosome2 = parent_chromosome2[:cross_point] + parent_chromosome1[cross_point:]

    child1 = Individu(surface, image_target, child_chromosome1, grayscale, transparent)
    child2 = Individu(surface, image_target, child_chromosome2, grayscale, transparent)
    return child1, child2


def population_crossover(surface, population, image_target, crossover_rate=0.5, grayscale=False, transparent=True):
    """
    select some candidate of crossover from population, then make them breed with (currently) single point crossover !
    the offspring will automaticaly included in the new population, so you would'nt miss them... :)
    :param surface: pygame surface
    :param population: lists of Individu, current population
    :param image_target: pygame image target image to reproduce
    :param crossover_rate: float crossover rate probability
    :param grayscale: boolean if the image is grayscale
    :param transparent: boolean to determine if the circles of reproduction using transparency or not
    :return: new population which contains the old population and the new offspring
    """
    candidates = choose_candidates(population, crossover_rate)
    parent1 = None
    offspring = []
    for candidate in candidates:
        if parent1 is None:
            parent1 = candidate
        else:
            parent2 = candidate

            child1, child2 = crossover(surface, parent1, parent2, image_target, grayscale, transparent)
            offspring.append(child1)
            offspring.append(child2)

            parent1 = None
    total_population = population + offspring
    return total_population


def mutation(surface, parent, image_target, grayscale=False, transparent=True):
    """
    Lets make a mutant with this single point mutation method ! said dr. mutante in his lab
    :param surface: pygame surface
    :param parent: Individu so you are the mutant candidate, eh ?
    :param image_target: pygame image target image to reproduce
    :param grayscale: boolean if the image is grayscale
    :param transparent: boolean to determine if the circles of reproduction using transparency or not
    :return: Individu the mutant child, which is only a gene different with his parent !
    """
    parent_chromosome = parent.chromosome
    mutation_point = random.randrange(0, len(parent_chromosome))

    child_chromosome = parent_chromosome.copy()
    child_chromosome[mutation_point] = new_gene(surface, grayscale)
    child = Individu(surface, image_target, child_chromosome, grayscale, transparent)
    return child


def population_mutation(surface, population, image_target, mutation_rate=0.5, grayscale=False, transparent=True):
    """
    Need a horde of mutant ? don't worry, this function will do it for you !
    this function will select a few candidate from your population, and poof!
    your new population wil contains some mutants !
    :param surface: pygame surface
    :param population: lists of Individu, current population
    :param image_target: pygame image target image to reproduce
    :param mutation_rate: float mutation rate probability
    :param grayscale: boolean if the image is grayscale
    :param transparent: boolean to determine if the circles of reproduction using transparency or not
    :return: a new population which contains the new mutants! don't worry though, the old population is still there
    """
    offspring = []
    candidates = choose_candidates(population, mutation_rate)

    for candidate in candidates:
        child = mutation(surface, candidate, image_target, grayscale, transparent)
        offspring.append(child)

    total_population = population + offspring
    return total_population


def selection(population, population_size):
    """
    This populations is too crowded, we need to kill some of them. said the king of tyrant
    :param population: lists of Individu, this current population is too dense
    :param population_size: int, so how many of them should live, your majesty ?
    :return: this new population is better, finally i could breathe
    """
    if len(population) > population_size:
        diff = len(population) - population_size
        population.sort(key=operator.attrgetter('fitness'))
        for i in range(diff):
            pop = population.pop()
    return population


def best_individu(population):
    """
    Look we had a champion over here !
    :param population: current population
    :return: Individu a champion ! the best of all ! well, at least in this generations
    """
    best_candidate = population.index(min(population, key=operator.attrgetter('fitness')))
    return population[best_candidate]
