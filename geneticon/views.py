from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from .forms import PopulationForm
from .services.configuration import save_form_data, sample_configuration
from .services.generation import get_generation
from .models import Population, Life, Subject, Chromosome, Gene


def configuration(request):
    if request.method == 'POST':
        form = PopulationForm(request.POST)
        if form.is_valid():
            life_id = save_form_data(form)
            return HttpResponseRedirect('/life/' + str(life_id))
    else:
        form = PopulationForm()
    return render(request, 'configuration/configuration.html', {
        'population_form': form
    }, content_type='text/html')


def population(request):
    obj = get_object_or_404(Population, id=request.GET.get('population_id'))
    return render(request, 'population/population.html', {
        'population': obj
    }, content_type='text/html')


def life(request, life_id):
    life_model = get_object_or_404(Life, id=life_id)
    generations = []

    for i in range(life_model.epochs):
        generation = get_generation(life_model, i + 1)
        if not generation:
            break
        generations.append(generation)

    print(generations)
    return render(request, 'life/life.html', {
        'life': life_model,
        'generations': generations
    }, content_type='text/html')


def life_analyze(request, life_id):
    life_model = get_object_or_404(Life, id=life_id)
    generation = get_generation(life_model)

    return render(request, 'life/life.html', {
        'life': life_model
    }, content_type='text/html')


def preconfigure(request):
    sample_configuration(request)
