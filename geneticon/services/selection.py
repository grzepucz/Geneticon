import json

from geneticon.models import Selection, Chromosome, Gene
from geneticon.services.functions import get_formula_by_name


def best_of_selection(life_model, ancestors):
    calculated = []
    settings = json.loads(life_model.selection.settings)
    if not settings['group_size']:
        return False

    for subject in ancestors:
        subject_chromosomes = Chromosome.objects.filter(subject=subject)
        subject_genes = []

        for chromosome in subject_chromosomes:
            subject_genes_value = decode_chromosome_value(
                Gene.objects.filter(chromosome=chromosome),
                life_model.function,
                life_model.precision,
                chromosome.size)
            subject_genes.append(subject_genes_value)
        function_value = get_formula_by_name(life_model.function.name)(subject_genes[0], subject_genes[1])
        calculated.append((function_value, subject))

    return [item[1] for item in sorted(calculated, key=lambda x: x[0])[:settings['group_size']]]


def tournament_selection(life_model, ancestors):
    selected = []
    return selected


def roulette_selection(life_model, ancestors):
    selected = []
    return selected


def select_from_population(life_model, ancestors):
    if life_model.selection.type == 'BEST':
        return best_of_selection(life_model, ancestors)
    elif life_model.selection.type == 'TOURNAMENT':
        return tournament_selection(life_model, ancestors)
    elif life_model.selection.type == 'ROULETTE':
        return roulette_selection(life_model, ancestors)

    return False


def chromosome_binary_to_number(genes):
    gene_value = [str(value.allel) for value in sorted(genes, key=lambda x: x.locus)]
    return float(int("".join(gene_value), 2))


def decode_chromosome_value(genes, function, precision, chromosome_size):
    return round(function.domain_minimum \
                 + chromosome_binary_to_number(genes) \
                 * ((function.domain_maximum - function.domain_minimum)
                    / (2 ** chromosome_size - 1)), int(precision))


def calculate_chromosome_function_value():
    return True
