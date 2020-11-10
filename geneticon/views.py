import simplejson as json
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from .forms import PopulationForm
from .services.configuration import save_form_data, sample_configuration
from .services.generation import get_generation, create_generation
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


def life(request, life_id):
    life_model = get_object_or_404(Life, id=life_id)
    generations = []

    for i in range(life_model.epochs):
        generation = get_generation(life_model, i + 1)
        if not generation:
            break
        generations.append(generation)

    return render(request, 'life/life.html', {
        'life': life_model,
        'generations': generations
    }, content_type='text/html')


def epoch_analyze(request, life_id, epoch_number):
    life_model = get_object_or_404(Life, id=life_id)
    if epoch_number > life_model.epochs:
        return HttpResponse(status=400, content=False)
    if not Subject.objects.filter(population=life_model.population, generation=epoch_number).exists():
        create_generation(life_model, epoch_number)
    generation = get_generation(life_model, epoch_number)

    return render(request, 'epoch/epoch.html', {
        'generation': generation
    }, content_type='text/xml')
    # return HttpResponse(content=json.loads(generation), content_type='application/json', status=200)


def life_analysis(request, life_id):
    life_model = get_object_or_404(Life, id=life_id)
    generation = get_generation(life_model)

    return render(request, 'life/life.html', {
        'life': life_model
    }, content_type='text/html')


def preconfigure(request):
    sample_configuration(request)


def armageddon(request, life_id):
    Life.objects.filter(id=life_id).delete()
    return HttpResponse(content=True, status=200)
