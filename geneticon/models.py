from datetime import datetime
from django.db import models


class OptimizationMethod(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    formula = models.Func()
    domain_minimum = models.FloatField(default=0)
    domain_maximum = models.FloatField(default=0)
    body = models.CharField(max_length=250, default='')
    pass

    def __str__(self):
        return self.name


class Population(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    size = models.BigIntegerField(default=0)
    create_date = models.DateField(default=datetime.now())
    pass

    def __str__(self):
        return self.name


# Settings are in JSON format
class Selection(models.Model):
    choices = [
        ('BEST', 'The best of'),
        ('TOURNAMENT', 'Tournament'),
        ('ROULETTE', 'Roulette')
    ]
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=30, choices=choices)
    settings = models.TextField(null=True)
    pass


class Hybridization(models.Model):
    choices = [
        ('SINGLE', 'Single point'),
        ('DOUBLE', 'Double point'),
        ('TRIPLE', 'Triple point'),
        ('HOMO', 'Homogeneous')
    ]
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=30, choices=choices)
    probability = models.FloatField(default=0)
    pass


class Mutation(models.Model):
    choices = [
        ('EDGE', 'Edge'),
        ('SINGLE', 'Single point'),
        ('DOUBLE', 'Double point')
    ]
    id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=30, choices=choices)
    probability = models.FloatField(default=0)
    pass


class Inversion(models.Model):
    probability = models.FloatField(default=0)
    pass


class Life(models.Model):
    choices = [
        ('MAX', 'Maximum'),
        ('MIN', 'Minimum')
    ]
    id = models.AutoField(primary_key=True)
    population = models.OneToOneField(Population, on_delete=models.CASCADE)
    epochs = models.IntegerField(default=10)
    selection = models.OneToOneField(Selection, on_delete=models.CASCADE)
    hybridization = models.OneToOneField(Hybridization, on_delete=models.CASCADE)
    mutation = models.OneToOneField(Mutation, on_delete=models.CASCADE)
    inversion = models.OneToOneField(Inversion, on_delete=models.CASCADE)
    elite_strategy = models.FloatField(default=0)
    precision = models.IntegerField(default=0)
    function = models.ForeignKey(OptimizationMethod, on_delete=models.CASCADE)
    problem = models.CharField(max_length=3, default='MIN')


class Epoch(models.Model):
    number = models.IntegerField(default=1)
    life = models.ForeignKey(Life, on_delete=models.CASCADE)
    generation_time = models.FloatField(default=0)
    pass


class Subject(models.Model):
    name = models.CharField(max_length=30)
    population = models.ForeignKey(Population, on_delete=models.CASCADE)
    epoch = models.ForeignKey(Epoch, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Chromosome(models.Model):
    id = models.AutoField(primary_key=True)
    size = models.BigIntegerField(default=0)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    pass


class Gene(models.Model):
    id = models.AutoField(primary_key=True)
    allel = models.IntegerField(default=1)
    locus = models.IntegerField(default=1)
    chromosome = models.ForeignKey(Chromosome, on_delete=models.CASCADE)
    pass

    def __str__(self):
        return str(self.locus)
