import math

from django.shortcuts import get_list_or_404

from geneticon.models import Subject, Chromosome, Gene, Life, OptimizationMethod
from geneticon.services.functions import get_formula_by_name


def get_generation(life_model, generation=1):
    subjects = Subject.objects.filter(population=life_model.population, generation=generation)

    if len(subjects) < 1:
        return False

    generation = []
    for subject in subjects:
        subject_chromosomes = get_list_or_404(Chromosome, subject=subject)
        subject_genes = []

        for chromosome in subject_chromosomes:
            subject_genes_value = decode_chromosome_value(
                get_list_or_404(Gene, chromosome=chromosome),
                life_model.function,
                life_model.precision)
            subject_genes.append((get_list_or_404(Gene, chromosome=chromosome), subject_genes_value))

        function_value = get_formula_by_name(life_model.function.name)(subject_genes[0][1], subject_genes[1][1])
        generation.append((subject, subject_genes, function_value))
    return generation


def calculate_chromosome_size(function, precision):
    return round(
        math.ceil(
            math.log2(
                (float(function.domain_maximum) - float(function.domain_minimum)) * (10 ** int(precision))
            ) + math.log2(1)), precision)


def chromosome_binary_to_number(genes):
    gene_value = [str(value.allel) for value in sorted(genes, key=lambda x: x.locus)]
    return float(int("".join(gene_value), 2))


def decode_chromosome_value(genes, function, precision):
    return function.domain_minimum \
           + chromosome_binary_to_number(genes) \
           * ((function.domain_maximum - function.domain_minimum)
              / (2 ** calculate_chromosome_size(function, precision) - 1))


def chromosome_number_to_binary():
    return True
