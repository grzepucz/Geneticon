from django import forms
from .models import OptimizationMethod, Selection, Hybridization, Mutation, Inversion, Population
from django.core.validators import MaxValueValidator, MinValueValidator


class PopulationForm(forms.Form):
    population_size = forms.IntegerField(label='Population size', required=True)
    population_name = forms.CharField(label='Population name', required=True)

    methods = [(model.id, model.name) for model in OptimizationMethod.objects.all()]
    optimization_function = forms.ChoiceField(
        label='Optimize function',
        required=True,
        widget=forms.Select,
        choices=methods
    )
    epochs_number = forms.IntegerField(label='Epochs number')
    selection_type = forms.ChoiceField(
        label='Selection type',
        required=True,
        widget=forms.Select,
        choices=Selection.choices)
    selection_settings = forms.CharField(label='Selection settings in JSON format. Use schema from description')

    hybridization_type = forms.ChoiceField(
        label='Hybridization type',
        required=True,
        widget=forms.Select,
        choices=Hybridization.choices)
    hybridization_probability = forms.FloatField(
        label='Hybridization probability in range 0 - 1',
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)])

    mutation_type = forms.ChoiceField(
        label='Mutation type',
        required=True,
        widget=forms.Select,
        choices=Mutation.choices)
    mutation_probability = forms.FloatField(
        label='Mutation probability in range 0 - 1',
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)])

    inversion_probability = forms.FloatField(
        label='Inversion probability in range 0 - 1',
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)])

    elite_strategy = forms.FloatField(
        label='Elite strategy as percent in range 0-1',
        required=True,
        validators=[MinValueValidator(0), MaxValueValidator(1)])
