# Generated by Django 2.2.12 on 2020-11-07 15:57

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chromosome',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('size', models.BigIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Hybridization',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('SINGLE', 'Single point'), ('DOUBLE', 'Double point'), ('TRIPLE', 'Triple point'), ('HOMO', 'Homogeneous')], max_length=30)),
                ('probability', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Inversion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('probability', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Mutation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('EDGE', 'Edge'), ('SINGLE', 'Single point'), ('DOUBLE', 'Double point')], max_length=30)),
                ('probability', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='OptimizationMethod',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('domain_minimum', models.FloatField(default=0)),
                ('domain_maximum', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Population',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('size', models.BigIntegerField(default=0)),
                ('create_date', models.DateField(default=datetime.datetime(2020, 11, 7, 15, 57, 5, 973171))),
            ],
        ),
        migrations.CreateModel(
            name='Selection',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('BEST', 'The best of'), ('TOURNAMENT', 'Tournament'), ('ROULETTE', 'Roulette')], max_length=30)),
                ('settings', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('population', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geneticon.Population')),
            ],
        ),
        migrations.CreateModel(
            name='Life',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('epochs', models.IntegerField(default=10)),
                ('elite_strategy', models.FloatField(default=0)),
                ('function', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geneticon.OptimizationMethod')),
                ('hybridization', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='geneticon.Hybridization')),
                ('inversion', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='geneticon.Inversion')),
                ('mutation', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='geneticon.Mutation')),
                ('population', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='geneticon.Population')),
                ('selection', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='geneticon.Selection')),
            ],
        ),
        migrations.CreateModel(
            name='Gene',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('allel', models.IntegerField(default=1)),
                ('locus', models.IntegerField(default=0)),
                ('chromosome', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geneticon.Chromosome')),
            ],
        ),
        migrations.AddField(
            model_name='chromosome',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='geneticon.Subject'),
        ),
    ]