import json
import random
from math import ceil

from geneticon.models import Chromosome, Gene
from geneticon.services.functions import get_formula_by_name


def sort_selected(result, problem):
    return [item[1] for item in sorted(result, key=lambda x: x[0], reverse=True if problem == 'MAX' else False)]


def get_group_size(settings, elements):
    try:
        if settings['group_size']:
            return settings['group_size']
    except KeyError:
        if settings['group_size_percent']:
            return ceil((int(settings['group_size_percent']) / 100) * len(elements))
        else:
            return 0


def get_sorted_values(life_model, ancestors):
    calculated = []
    formula = get_formula_by_name(life_model.function.name)

    for subject in ancestors:
        subject_chromosomes = Chromosome.objects.filter(subject=subject)
        subject_genes = []

        if subject_chromosomes.exists():
            function_value = False

            if life_model.representation == 'BINARY':
                for chromosome in subject_chromosomes:
                    subject_genes_value = decode_chromosome_value(
                        Gene.objects.filter(chromosome=chromosome),
                        life_model.function,
                        life_model.precision,
                        chromosome.size)
                    subject_genes.append(subject_genes_value)
                function_value = formula(subject_genes[0], subject_genes[1])
            if life_model.representation == 'REAL':
                function_value = formula(subject_chromosomes[0].real_value, subject_chromosomes[1].real_value)

            calculated.append((function_value, subject))

    return sorted(calculated, key=lambda x: x[0], reverse=True if life_model.problem == 'MAX' else False)


def best_of_selection(settings, elements):
    group_size = get_group_size(settings, elements)

    return [item for item in elements[:group_size]]


def tournament_selection(settings, elements, life_model):
    group_size = get_group_size(settings, elements)

    if len(elements) < 2:
        return [elements[0][1]]

    tournament = []
    for index in range(ceil(len(elements)/int(group_size))):
        tournament_group_size = int(group_size) if len(elements) >= int(group_size) else len(elements)
        group = random.sample(elements, tournament_group_size)
        elements = [item for item in elements if item not in group]
        tournament.append(sorted(group, key=lambda x: x[0], reverse=True if life_model.problem == 'MAX' else False))
    return [winner[0] for winner in tournament]


def roulette_selection(settings, elements, life_model):
    group_size = get_group_size(settings, elements)

    calculated = [(1/item[0] if life_model.problem == 'MIN' else item[0], item[1]) for item in elements]
    roulette_group_size = group_size if len(calculated) > group_size else len(calculated)
    roulette = []

    for index in range(roulette_group_size):
        circle_weight = sum([abs(item[0]) for item in calculated])
        distributor = [0, 0]  # [current, previous]
        pivot = random.random()
        for item in calculated:
            distributor_old = distributor[0]
            distributor_new = abs(item[0]) / circle_weight + distributor_old
            distributor = [distributor_new, distributor_old]
            if distributor_old < pivot <= distributor_new:
                roulette.append(item)
                calculated.remove(item)
                break
    return roulette


def select_from_population(life_model, ancestors):
    settings = json.loads(life_model.selection.settings)
    elements = get_sorted_values(life_model, ancestors)
    result = []

    if life_model.selection.type == 'BEST':
        result = best_of_selection(settings, elements)
    elif life_model.selection.type == 'TOURNAMENT':
        result = tournament_selection(settings, elements, life_model)
    elif life_model.selection.type == 'ROULETTE':
        result = roulette_selection(settings, elements, life_model)

    return sort_selected(result, life_model.problem)


def chromosome_binary_to_number(genes):
    gene_value = [str(value.allel) for value in sorted(genes, key=lambda x: x.locus)]
    return float(int("".join(gene_value), 2))


def decode_chromosome_value(genes, function, precision, chromosome_size):
    return round(function.domain_minimum
                 + chromosome_binary_to_number(genes)
                 * ((function.domain_maximum - function.domain_minimum)
                    / (2 ** chromosome_size - 1)),
                 int(precision))
