import json
import math
import random
import string

from django.shortcuts import get_list_or_404
from .selection import decode_chromosome_value, select_from_population
from .hybridization import create_offspring
from geneticon.models import Subject, Chromosome, Gene, Life, OptimizationMethod
from geneticon.services.functions import get_formula_by_name


def create_generation(life_model, generation):
    ancestors = Subject.objects.filter(population=life_model.population, generation=generation-1)
    parents = select_from_population(life_model, ancestors)
    return create_offspring(life_model, parents, generation)


def get_generation(life_model, generation=1):
    subjects = Subject.objects.filter(population=life_model.population, generation=generation)

    if len(subjects) < 1:
        return False

    generation = []
    for subject in subjects:
        subject_chromosomes = Chromosome.objects.filter(subject=subject)
        subject_genes = []

        for chromosome in subject_chromosomes:
            subject_genes_value = decode_chromosome_value(
                get_list_or_404(Gene, chromosome=chromosome),
                life_model.function,
                life_model.precision,
                calculate_chromosome_size(life_model.function, life_model.precision))
            subject_genes.append((get_list_or_404(Gene, chromosome=chromosome), subject_genes_value))

        formula = get_formula_by_name(life_model.function.name)
        function_value = formula(subject_genes[0][1], subject_genes[1][1]) if len(subject_genes) else 'NaN'
        generation.append((subject, subject_genes, function_value))
    return sorted(generation, key=lambda x: x[2])


def calculate_chromosome_size(function, precision):
    return round(
        math.ceil(
            math.log2(
                (float(function.domain_maximum) - float(function.domain_minimum)) * (10 ** int(precision))
            ) + math.log2(1)), int(precision))


def chromosome_binary_to_number(genes):
    gene_value = [str(value.allel) for value in sorted(genes, key=lambda x: x.locus)]
    return float(int("".join(gene_value), 2))


def create_gene(chromosome):
    for i in range(chromosome.size):
        gene = Gene(allel=round(random.random()), locus=i, chromosome=chromosome)
        gene.save()


def create_chromosome(subject, function, precision, size=2):
    chromosome_size = calculate_chromosome_size(function, precision)

    for i in range(size):
        chromosome = Chromosome(
            size=chromosome_size,
            subject=subject)
        chromosome.save()
        create_gene(chromosome)


def create_subjects(population, function, precision, generation=1):
    for i in range(int(population.size)):
        subject = Subject(population=population, generation=generation)
        subject.name = ''.join(random.choice(string.ascii_lowercase) for j in range(10))
        subject.save()
        create_chromosome(subject, function, precision)


def chromosome_number_to_binary():
    return True
