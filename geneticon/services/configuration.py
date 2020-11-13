import inspect
import json
import time

from django.http import HttpResponse
from geneticon.models import OptimizationMethod, Population, Selection, Hybridization, Mutation, Inversion, Life, Epoch
from .functions import bohachevsky_formula, booth_formula
from .generation import create_subjects


def save_form_data(form):
    start_time = time.time()

    selection = Selection(
        type=form.data['selection_type'],
        settings=form.data['selection_settings']
    )
    selection.save()

    mutation = Mutation(
        type=form.data['mutation_type'],
        probability=form.data['mutation_probability']
    )
    mutation.save()

    hybridization = Hybridization(
        type=form.data['hybridization_type'],
        probability=form.data['hybridization_probability']
    )
    hybridization.save()

    inversion = Inversion(probability=form.data['inversion_probability'])
    inversion.save()

    population = Population(
        name=form.data['population_name'],
        size=form.data['population_size']
    )
    population.save()

    function = OptimizationMethod.objects.get(id=form.data['optimization_function'])
    precision = form.data['precision']

    life = Life(population=population,
                epochs=form.data['epochs_number'],
                selection=selection,
                hybridization=hybridization,
                mutation=mutation,
                inversion=inversion,
                elite_strategy=form.data['elite_strategy'],
                precision=precision,
                function=function)
    life.save()
    epoch = Epoch(life=life, number=1)
    epoch.save()

    create_subjects(population, function, precision, epoch)
    epoch.generation_time = time.time() - start_time
    epoch.save()

    return life.id


def create_methods():
    bohachevsky = OptimizationMethod(
        id=1,
        domain_minimum=-100,
        domain_maximum=100,
        body='(x1^2) + (2 * (x2^2)) - (0.3 * cos(3 * pi * x1)) - (0.4 * cos(4 * pi * x2))',
        name='Bohachevsky')
    bohachevsky.formula = inspect.getsource(bohachevsky_formula)
    bohachevsky.save()

    booth = OptimizationMethod(
        id=2,
        body='(x1 + 2 * x2 - 7)^2 + (2 * x1 + x2 - 5)^2',
        domain_minimum=-10,
        domain_maximum=10,
        name='Booth')
    booth.formula = inspect.getsource(booth_formula)
    booth.save()


def sample_configuration(request):
    create_methods()
    return HttpResponse(200)
