![Geneticon](geneticon.png?raw=true "Geneticon")

# Genetic algorithms implementation
Implementation of genetic algorithms in python3 by finding minimal values of chosen multivariable functions. You can configure selection method, crossover type and probability, mutation type and probability, inversion probability and elite strategy percentage. Also You can and should set epoch numbers, precision of numbers after comma and group_size, different for selected selection method.

If configuration exists You can iterate through each generations or 'live' the life to iterate n-times till find only one result or exceed epoch limit number.

In configuration form You should pass json object {"group_size": x} where x has different meanings:
- Best of selection: number of subjects chosen from population to reproduce.
- Tournament: number of subjects in one group, chosen from population to reproduce.
- Roulette: number of subjects chosen from population to reproduce.
## Stack:
- Python3
- Django
- SASS
### Python external libraries
- statistics

# Run
## Local
```
pip3 install -r requirements.txt
python3 manage.py runserver
```
## Docker
```
docker-compose up
```

Server is listening on http://127.0.0.1:8000/
Before You start to use this project, request http://127.0.0.1:8000/preconfigure endpoint. It is required for creating and saving OptimizationMethod objects, which represent functions to optimize.

# Metrics
You can view some metrics in generated population generation. Extend epoch row and click "generate metrics" button to see 3D plot and view mean and standard distributor for current generation.