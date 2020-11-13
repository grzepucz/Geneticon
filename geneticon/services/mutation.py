import random
from geneticon.models import Chromosome, Gene


def edge_mutation(chromosomes, mutation_probability):
    for chromosome in chromosomes:
        if random.random() <= mutation_probability:
            locus = 1 if random.random() > 0.5 else chromosome.size
            gene = Gene.objects.get(chromosome=chromosome, locus=locus)
            gene.allel = 0 if gene.allel == 1 else 1
            gene.save()


def single_mutation(chromosomes, mutation_probability):
    for chromosome in chromosomes:
        if random.random() <= mutation_probability:
            locus = random.choice(range(1, chromosome.size+1))
            gene = Gene.objects.get(chromosome=chromosome, locus=locus)
            gene.allel = 0 if gene.allel == 1 else 1
            gene.save()


def multiple_mutation(chromosomes, points, mutation_probability):
    for chromosome in chromosomes:
        if random.random() <= mutation_probability:
            locus = random.sample(set(range(1, chromosome.size+1)), points)
            for i in range(points):
                gene = Gene.objects.get(chromosome=chromosome, locus=locus[i])
                gene.allel = 0 if gene.allel == 1 else 1
                gene.save()


def mutate(subject, mutation_type, mutation_probability):
    chromosomes = Chromosome.objects.filter(subject=subject)
    if mutation_type == 'EDGE':
        edge_mutation(chromosomes, mutation_probability)
    if mutation_type == 'SINGLE':
        single_mutation(chromosomes, mutation_probability)
    if mutation_type == 'DOUBLE':
        multiple_mutation(chromosomes, 2, mutation_probability)

    return subject
