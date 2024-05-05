import random

# Define the items and their characteristics
objects = [
    {"cost": 2, "duration": 10, "granularity": "D", "c": "c1"},  # c1
    {"cost": 3, "duration": 5, "granularity": "D", "c": "c2"},  # c2
    {"cost": 5, "duration": 15, "granularity": "D", "c": "c3"},  # c3
    {"cost": 7, "duration": 7, "granularity": "D", "c": "c4"},  # c4
    {"cost": 1, "duration": 6, "granularity": "I", "c": "c5"},  # c5
    {"cost": 4, "duration": 18, "granularity": "I", "c": "c6"},  # c6
    {"cost": 1, "duration": 3, "granularity": "I", "c": "c7"}   # c7
]

maximum_cost = 10  # Maximum cost allowed

# Define the genetic algorithm parameters
population_size = 100
chromosome_length = len(objects)
mutation_rate = 0.1
generations = 100

# Define the fitness function
def fitness(individual):
    total_duration = 0
    total_cost = 0
    for i in range(chromosome_length):
        if individual[i]:
            total_duration += objects[i]["duration"]
            total_cost += objects[i]["cost"]
    
    if total_cost > maximum_cost:
        return 0
    else:
        return total_duration

# Initialize the population
population = [[random.randint(0, 1) for _ in range(chromosome_length)] for _ in range(population_size)]

def genetic_algorithm():
    global population
    # Genetic algorithm loop
    for generation in range(generations):
        # Evaluate the fitness of each individual
        fitness_scores = [fitness(individual) for individual in population]

        # Select the fittest individuals
        selected_individuals = [population[i] for i in sorted(range(population_size), key=lambda x: fitness_scores[x], reverse=True)[:population_size//2]]

        # Create the next generation
        next_generation = []
        for _ in range(population_size//2):
            # Select two parents
            parent1 = random.choice(selected_individuals)
            parent2 = random.choice(selected_individuals)

            # Perform crossover
            crossover_point = random.randint(1, chromosome_length - 1)
            child1 = parent1[:crossover_point] + parent2[crossover_point:]
            child2 = parent2[:crossover_point] + parent1[crossover_point:]

            # Mutate the children
            if random.random() < mutation_rate:
                child1 = [1 - gene for gene in child1]
            if random.random() < mutation_rate:
                child2 = [1 - gene for gene in child2]

            # Add the children to the next generation
            next_generation.append(child1)
            next_generation.append(child2)

        # Replace the population with the next generation
        population = next_generation
    return population

pop = genetic_algorithm()
# Find the best solution in the final population
best_solution = max(pop, key=fitness)
best_fitness = fitness(best_solution)

# Print the best solution
combination = []
print("Best solution:")
for i in range(chromosome_length):
    if best_solution[i]:
        combination.append(objects[i]['c'])
        print(f"Item: Cost={objects[i]['cost']}, Duration={objects[i]['duration']}, Granularity={objects[i]['granularity']}")
print(f"Total duration: {best_fitness}")
total_cost = sum(objects[i]['cost'] for i in range(chromosome_length) if best_solution[i])
print(f"Total cost: {total_cost}")
print(f"Best Combinations: {combination}")