from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
import datetime
from .forms import PopulationForm
from .services.configuration import save_form_data, sample_configuration
from .models import Population, Life


def home(request):
    return render(request, 'home.html', {
        'date_value': datetime.datetime.now(),
    }, content_type='text/html')


def configuration(request):
    if request.method == 'POST':
        form = PopulationForm(request.POST)
        if form.is_valid():
            life_id = save_form_data(form)
            return HttpResponseRedirect('/life?life_id=' + str(life_id))
    else:
        form = PopulationForm()
    return render(request, 'configuration/configuration.html', {
        'population_form': form
    }, content_type='text/html')


def population(request):
    print(request.GET.get('population_id'))
    obj = get_object_or_404(Population, id=request.GET.get('population_id'))
    print(obj.name)
    return render(request, 'population/population.html', {
        'population': obj
    }, content_type='text/html')


def life(request):
    life_model = get_object_or_404(Life, id=request.GET.get('life_id'))
    return render(request, 'life/life.html', {
        'life': life_model
    }, content_type='text/html')


def preconfigure(request):
    sample_configuration(request)
