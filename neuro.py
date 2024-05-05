import random
import numpy as np

# Problem definition
population_size = 50
mutation_rate = 0.1
generations = 50

objects = [
    {"cost": 2, "duration": 10, "granularity": "D","c": "c1"},
    {"cost": 3, "duration": 5, "granularity": "D","c": "c2"},
    {"cost": 5, "duration": 15, "granularity": "D","c": "c3"},
    {"cost": 7, "duration": 7, "granularity": "D","c": "c4"},
    {"cost": 1, "duration": 6, "granularity": "I","c": "c5"},
    {"cost": 4, "duration": 18, "granularity": "I","c": "c6"},
    {"cost": 1, "duration": 3, "granularity": "I","c": "c7"},
]

maximum_cost = 10
chromosome_length = len(objects)

# Neural Network Parameters
input_size = chromosome_length
hidden_size = 7
output_size = 1

# Genetic Algorithm Functions
def create_individual():
    return np.random.randint(2, size=input_size*hidden_size + hidden_size*output_size)

def decode_individual(individual):
    input_hidden_weights = individual[:input_size*hidden_size].reshape(input_size, hidden_size)
    hidden_output_weights = individual[input_size*hidden_size:].reshape(hidden_size, output_size)
    return input_hidden_weights, hidden_output_weights

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def evaluate_individual(individual):
    combination = []
    input_hidden_weights, hidden_output_weights = decode_individual(individual)
    total_duration = 0
    total_cost = 0
    for obj in range(len(objects)):
        activation = sigmoid(np.dot(objects[obj]["cost"], input_hidden_weights[:, obj]) + np.dot(objects[obj]["duration"], hidden_output_weights[:, 0]))

        if activation[obj] > 0.5:
            total_duration += objects[obj]["duration"]
            total_cost += objects[obj]["cost"]
            combination.append(objects[obj]["c"])
    return total_duration, total_cost, combination

def mutate(individual):
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

def crossover(parent1, parent2):
    crossover_point = random.randint(0, len(parent1))
    child1 = np.concatenate((parent1[:crossover_point], parent2[crossover_point:]))
    child2 = np.concatenate((parent2[:crossover_point], parent1[crossover_point:]))
    return child1, child2

def selection(population):
    sorted_population = sorted(population, key=lambda x: evaluate_individual(x))
    selected = sorted_population[:int(len(sorted_population)/2)]
    return selected

def genetic_algorithm():
    solution = 0
    population = [create_individual() for _ in range(population_size)]

    for _ in range(generations):
        selected_population = selection(population)
        new_population = selected_population[:]

        while len(new_population) < population_size:
            parent1, parent2 = random.sample(selected_population, 2)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.append(child1)
            new_population.append(child2)

        population = new_population
        # Evaluate only individuals with 1 i.e. truthy values...
    for individual in population:
        new_individuals = [i for i in individual if i>0]
        total_duration, total_cost, combination = evaluate_individual(individual)
        # print(f"Total Cost: {total_cost}, Total Duration: {total_duration}")
        if total_cost <= maximum_cost and total_cost>0 and  total_duration>0:
            print(solution, "eme solution")
            # print("Individual:", individual)
            print("Total duration:", total_duration)
            print("Total cost:", total_cost)
            print(f"Combination: {combination}")
            solution += 1

# Run the genetic algorithm
genetic_algorithm()
