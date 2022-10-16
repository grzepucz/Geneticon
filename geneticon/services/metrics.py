import statistics

from geneticon.models import Epoch


def create_data_plot_attributes(generation):
    data_x = []
    data_y = []
    data_z = []
    for subject, subject_genes, function_value in generation:
        for index in range(len(subject_genes)):
            if index == 0:
                data_x.append(subject_genes[index][1])
            if index == 1:
                data_y.append(subject_genes[index][1])
        data_z.append(function_value)
    return [data_x, data_y, data_z]


def get_statistics(generation):
    function_values = [function_value for (subject, subject_genes, function_value) in generation]
    if len(function_values) == 1:
        return [function_values[0], 0]
    mean = statistics.mean(function_values)
    deviation = statistics.stdev(function_values)
    return [mean, deviation]


def get_epoch_numbers(life_id):
    return [(epoch.number, epoch.number) for epoch in Epoch.objects.filter(life_id=life_id)]
