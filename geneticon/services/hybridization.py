import math
import random
import string

from geneticon.models import Subject, Chromosome, Gene
from .mutation import mutate
from .inversion import inverse


def create_subjects(reflect_offspring):
    offspring = []
    for parent in reflect_offspring:
        clone = Subject(name=parent.name, population=parent.population, generation=parent.generation+1)
        clone.save()
        for parent_chromosome in Chromosome.objects.filter(subject=parent):
            chromosome = Chromosome(size=parent_chromosome.size, subject=clone)
            chromosome.save()
            for parent_gene in Gene.objects.filter(chromosome=parent_chromosome):
                gene = Gene(allel=parent_gene.allel, locus=parent_gene.locus, chromosome=chromosome)
                gene.save()
        offspring.append(clone)
    return offspring


def create_offspring(life_model, parents, generation):
    offspring = []
    if life_model.elite_strategy > 0:
        offspring = create_subjects(parents[:math.ceil(life_model.elite_strategy * len(parents))])

    for index in range(len(parents)):
        subject = parents[index]
        if random.random() < life_model.hybridization.probability:
            subject = crossover(parents, index, life_model, generation)
        if random.random() < life_model.mutation.probability:
            print('zmutowano!')
            print(subject)
            subject = mutate(life_model.mutation.type, subject)
        if random.random() < life_model.inversion.probability:
            subject = inverse(subject)
        offspring.append(subject)

    return offspring


def get_non_self_random_index(range_end, index):
    rand = random.randint(0, range_end-1)
    while rand == index:
        rand = random.randint(0, range_end-1)
    return rand


def single_crossover(chromosomes, partner_chromosomes, life_model, generation):
    new_subject = Subject()
    new_subject.name = ''.join(random.choice(string.ascii_lowercase) for j in range(10))
    new_subject.generation = generation
    new_subject.population = life_model.population
    new_subject.save()

    for chromosome_index in range(len(chromosomes)):
        new_chromosome = Chromosome(size=chromosomes[chromosome_index].size, subject=new_subject)
        new_chromosome.save()
        genes_x = Gene.objects.filter(chromosome=chromosomes[chromosome_index]).order_by('locus')
        genes_y = Gene.objects.filter(chromosome=partner_chromosomes[chromosome_index]).order_by('locus')
        pivot = random.randint(0, chromosomes[chromosome_index].size)

        for gene_index in range(len(genes_x)):
            new_gene = Gene()
            if gene_index < pivot:
                new_gene.allel = genes_x[gene_index].allel
                new_gene.locus = genes_x[gene_index].locus
            else:
                new_gene.allel = genes_y[gene_index].allel
                new_gene.locus = genes_y[gene_index].locus
            new_gene.chromosome = new_chromosome
            new_gene.save()
    return new_subject


def crossover(parents, index, life_model, generation):
    partner_index = get_non_self_random_index(len(parents), index)
    partner = parents[partner_index]
    chromosomes = Chromosome.objects.filter(subject=parents[index])
    partner_chromosomes = Chromosome.objects.filter(subject=partner)

    if life_model.hybridization.type == 'SINGLE':
        return single_crossover(chromosomes, partner_chromosomes, life_model, generation)

    return False
