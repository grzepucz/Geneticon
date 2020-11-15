import time
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PopulationForm
from .services.configuration import save_form_data, sample_configuration
from .services.generation import get_generation, create_generation
from .services.metrics import create_data_plot_attributes, get_statistics, get_epoch_numbers
from .models import Population, Life, Epoch


def home(request):
    lives = []
    for record in Life.objects.all():
        population = Population.objects.get(life=record)
        lives.append((record.id, population.name, record.selection.type, record.function.name, population.create_date))
    return render(request, 'home.html', {
        'lives': lives
    }, content_type='text/html')


def configuration(request):
    if request.method == 'POST':
        form = PopulationForm(request.POST)
        if form.is_valid():
            time_start = time.time()
            life_id = save_form_data(form)
            return HttpResponseRedirect('/life/' + str(life_id) + '?generation_time=' + str(time.time() - time_start))
    else:
        form = PopulationForm()
    return render(request, 'configuration/configuration.html', {
        'population_form': form
    }, content_type='text/html')


def life(request, life_id):
    life_model = get_object_or_404(Life, id=life_id)
    generations = []
    for epoch in Epoch.objects.filter(life=life_model):
        generation = get_generation(life_model, epoch)
        if not generation:
            break
        generations.append((generation, epoch))

    return render(request, 'life/life.html', {
        'life': life_model,
        'generations': generations,
        'result': generations[-1][0][0],
        'generation_time': request.GET.get('generation_time', '')
    }, content_type='text/html')


def epoch_analyze(request, life_id, epoch_number):
    life_model = get_object_or_404(Life, id=life_id)
    if epoch_number > life_model.epochs:
        return HttpResponse(status=400, content=False)
    start_time = time.time()

    if not Epoch.objects.filter(life=life_model, number=epoch_number).exists():
        epoch = Epoch(life=life_model, number=epoch_number)
        epoch.save()
        offspring = create_generation(life_model, epoch)
        epoch.generation_time = round(time.time() - start_time, 4)
        epoch.save() if len(offspring) > 0 else epoch.delete()
    else:
        epoch = Epoch.objects.get(life=life_model, number=epoch_number)
    generation = get_generation(life_model, epoch)
    return render(request, 'epoch/epoch.html', {
        'generation': generation,
        'epoch': epoch,
        'life': life_model
    }, content_type='text/xml')


def preconfigure(request):
    sample_configuration(request)
    return HttpResponse(content=True, status=200)


def armageddon(request, life_id):
    Life.objects.filter(id=life_id).delete()
    return redirect('home')


def epoch_clean(request, life_id, epoch_number):
    Epoch.objects.filter(life=Life.objects.get(id=life_id), number=epoch_number).delete()
    return redirect('life', life_id=life_id)


def epoch_metrics(request, life_id, epoch_number):
    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['epoch_number'] = get_epoch_numbers(life_id, epoch_number)
    #     return kwargs
    life_model = get_object_or_404(Life, id=life_id)
    epoch = Epoch.objects.get(life=life_model, number=epoch_number)
    generation = get_generation(life_model, epoch)

    mean, deviation = get_statistics(generation)
    data_x, data_y, data_z = create_data_plot_attributes(generation)

    return render(request, 'metrics/metrics.html', {
        'life_id': life_id,
        'epoch_number': epoch_number,
        'mean': mean,
        'deviation': deviation,
        'data_x': data_x,
        'data_y': data_y,
        'data_z': data_z
    }, content_type='text/html')
