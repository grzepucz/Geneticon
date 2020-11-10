import random

from geneticon.models import Chromosome, Gene


def edge_mutation(subject):
    chromosomes = Chromosome.objects.filter(subject=subject)
    for chromosome in chromosomes:
        locus = 1 if random.random() > 0.5 else chromosome.size
        gene = Gene.objects.filter(chromosome=chromosome)
        print(locus, len(gene))
        # gene.allel = 0 if gene.allel == 1 else 1
        # gene.save()
    return subject


def mutate(mutation_type, subject):
    if mutation_type == 'EDGE':
        return edge_mutation(subject)
