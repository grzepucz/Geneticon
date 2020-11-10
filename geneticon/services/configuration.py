import inspect
import json
from django.http import HttpResponse
from geneticon.models import OptimizationMethod, Population, Selection, Hybridization, Mutation, Inversion, Life
from .functions import bohachevsky_formula, booth_formula
from .generation import create_subjects


def save_form_data(form):
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
    create_subjects(population, function, precision)

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

    return life.id


def create_sample_configuration():
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

    selection = Selection(id=1, type='TOURNAMENT', settings=json.JSONEncoder().encode({'group_size': 4}))
    selection.save()

    mutation = Mutation(id=1, type='EDGE', probability=0.1)
    mutation.save()

    hybridization = Hybridization(id=1, type='SINGLE', probability=0.8)
    hybridization.save()

    inversion = Inversion(id=1, probability=0.1)
    inversion.save()

    population = Population(id=1, name='Test', size=12)
    population.save()

    function = OptimizationMethod.objects.get(id=1)
    precision = 4
    create_subjects(population, function, precision)

    life = Life(population=population,
                epochs=20,
                selection=selection,
                hybridization=hybridization,
                mutation=mutation,
                inversion=inversion,
                elite_strategy=0.3,
                function=booth)
    life.save()


def sample_configuration(request):
    create_sample_configuration()
    return HttpResponse(200)
