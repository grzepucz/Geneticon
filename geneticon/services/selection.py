import json
import random
from math import ceil

from geneticon.models import Selection, Chromosome, Gene
from geneticon.services.functions import get_formula_by_name


def get_sorted_values(life_model, ancestors):
    calculated = []
    for subject in ancestors:
        subject_chromosomes = Chromosome.objects.filter(subject=subject)
        subject_genes = []
        if subject_chromosomes.exists():
            for chromosome in subject_chromosomes:
                subject_genes_value = decode_chromosome_value(
                    Gene.objects.filter(chromosome=chromosome),
                    life_model.function,
                    life_model.precision,
                    chromosome.size)
                subject_genes.append(subject_genes_value)
            function_value = get_formula_by_name(life_model.function.name)(subject_genes[0], subject_genes[1])
            calculated.append((function_value, subject))
    return sorted(calculated, key=lambda x: x[0], reverse=True if life_model.problem == 'MAX' else False)


def best_of_selection(life_model, ancestors, settings):
    if not settings['group_size']:
        return False
    return [
        item[1] for item in get_sorted_values(life_model, ancestors)
        [:settings['group_size']]]


def tournament_selection(life_model, ancestors, settings):
    if not settings['group_size']:
        return False

    calculated = get_sorted_values(life_model, ancestors)
    if len(calculated) < 2:
        return [calculated[0][1]]

    tournament = []
    for index in range(ceil(len(calculated)/int(settings['group_size']))):
        group_size = int(settings['group_size']) if len(calculated) >= int(settings['group_size']) else len(calculated)
        group = random.sample(calculated, group_size)
        calculated = [item for item in calculated if item not in group]
        tournament.append(sorted(group, key=lambda x: x[0], reverse=True if life_model.problem == 'MAX' else False))
    return [winner[0][1] for winner in tournament]


def roulette_selection(life_model, ancestors, settings):
    if not settings['group_size']:
        return False

    subjects = get_sorted_values(life_model, ancestors)
    calculated = [(1/item[0] if life_model.problem == 'MIN' else item[0], item[1]) for item in subjects]
    group_size = settings['group_size'] if len(calculated) > settings['group_size'] else len(calculated)
    roulette = []

    for index in range(group_size):
        circle_weight = sum([abs(item[0]) for item in calculated])
        distributor = [0, 0]  # [current, previous]
        pivot = random.random()
        for item in calculated:
            distributor_old = distributor[0]
            distributor_new = abs(item[0]) / circle_weight + distributor_old
            distributor = [distributor_new, distributor_old]
            if distributor_old < pivot <= distributor_new:
                roulette.append(item[1])
                calculated.remove(item)
                break
    return roulette


def select_from_population(life_model, ancestors):
    settings = json.loads(life_model.selection.settings)
    if life_model.selection.type == 'BEST':
        return best_of_selection(life_model, ancestors, settings)
    elif life_model.selection.type == 'TOURNAMENT':
        return tournament_selection(life_model, ancestors, settings)
    elif life_model.selection.type == 'ROULETTE':
        return roulette_selection(life_model, ancestors, settings)
    return []


def chromosome_binary_to_number(genes):
    gene_value = [str(value.allel) for value in sorted(genes, key=lambda x: x.locus)]
    return float(int("".join(gene_value), 2))


def decode_chromosome_value(genes, function, precision, chromosome_size):
    return round(function.domain_minimum
                 + chromosome_binary_to_number(genes)
                 * ((function.domain_maximum - function.domain_minimum)
                    / (2 ** chromosome_size - 1)),
                 int(precision))
