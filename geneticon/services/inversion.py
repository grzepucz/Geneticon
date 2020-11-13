import random

from geneticon.models import Chromosome, Gene


def inverse(subject, inversion_probability):
    chromosomes = Chromosome.objects.filter(subject=subject)
    for chromosome in chromosomes:
        if random.random() <= inversion_probability:
            pivot = random.sample(set(range(1, chromosome.size+1)), 2)
            lower_edge = min(pivot)
            higher_edge = max(pivot)
            genes = Gene.objects.filter(chromosome=chromosome, locus__gte=lower_edge, locus__lte=higher_edge)
            indexes = list(reversed([gene.locus for gene in genes]))
            for i in range(len(genes)):
                genes[i].locus = indexes[i]
                genes[i].save()

    return subject
