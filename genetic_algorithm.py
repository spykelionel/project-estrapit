import random

from problem_definition import chromosome_length, objects, population_size, maximum_cost, generations, mutation_rate

# Fonction de création d'un individu (chromosome) aléatoire
def create_individual():
    s1=[random.randint(0, 1) for _ in range(chromosome_length-3)]
    s2=[random.randint(0, 1) for _ in range(3)]
        
    while (s1.count(1)==0 or s2.count(1)==0):
        s1=[random.randint(0, 1) for _ in range(chromosome_length-3)]
        s2=[random.randint(0, 1) for _ in range(3)]
    
    return s1+s2
        
# Fonction d'évaluation d'un individu en calculant sa valeur totale et son poids total
def performance(individual,):
    #total_duration = 0
    total_cost = 0
    for i in range(chromosome_length):
        total_cost += objects[i]["cost"]*individual[i]
    return total_cost

def fitness(individual):
    
    return performance(individual)/performance([1, 1, 1, 1, 1, 1, 1])

def evaluate_individual(individual,):
    total_duration = 0
    total_cost = 0
    all_indexes = [] 
    for j in range(chromosome_length) : 
        if individual[j] == 1 : 
            all_indexes.append(j)
    for l in range(len(all_indexes)):
        total_duration += objects[all_indexes[l]]["duration"]
        total_cost += objects[all_indexes[l]]["cost"]
    
    return total_duration, total_cost

def maximum(ind1,ind2,):
    cost_ind1=0
    cost_ind2=0
    for i in range(chromosome_length):               
            cost_ind1 += objects[i]["cost"]*ind1[i]               
            cost_ind2 += objects[i]["cost"]*ind2[i]
    
    if (cost_ind1>=cost_ind2):
        return ind1
    else:
        return ind2
 
# Fonction de sélection des meilleurs individus (tournoi binaire)
def selection(population):
    population2=population[int(population_size/2):]
    selected = []
    for _ in range(int(len(population2))):
        tournament = random.sample(population2, 2)
        # tournament = random.sample(population2, 2) # Same s above!
        selected.append(maximum(tournament[0],tournament[1]))
        #max(tournament, key=lambda x: x[0]))
    return selected

# Fonction de croisement (crossover) à un point entre deux individus
def crossover(parent1, parent2,crossover_point):
    #crossover_point = random.randint(1, chromosome_length - 1)
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    return child1, child2

def multi_point_crossover(parent1, parent2,crossover_points):
    #crossover_point = random.randint(1, chromosome_length - 1)
    for i in range(len(crossover_points)):
        parent1,parent2 =crossover(parent1, parent2,crossover_points[i])
    return parent1, parent2
# Fonction de mutation d'un individu (inversion d'un bit)

def mutate(individual):
    for i in range(chromosome_length):
        if random.random() < mutation_rate:
            individual[i] = 1 - individual[i]
    return individual

# Algorithme génétique pour résoudre le problème du sac à dos
def genetic_algorithm():
    solution=0
    # Génération de la population initiale
    population = [create_individual() for _ in range(population_size)]

    for _ in range(generations):
     
        # Sélection des meilleurs individus (tri par valeur totale décroissante)
        population = sorted(population, key=lambda x: evaluate_individual(x), reverse=True)
        selected_population = selection(population)
        new_population = population[:int(population_size/2)]

        while len(new_population) < population_size:
            # Sélection de deux parents aléatoires parmi la population sélectionnée
           
            parent1, parent2 = random.sample(selected_population, 2)
            crossover_point = random.randint(1, chromosome_length - 1)
            child1, child2 = crossover(parent1, parent2,crossover_point)
            mutate(child1)
            mutate(child2)
            new_population.append(child1)
            new_population.append(child2)
            

        # Remplacement de l'ancienne population par la nouvelle génération
        population = new_population
    
    meilleur_cost=0
    meilleur_val=0
    
    for k in range(len(population)):
        
        valu=0
        w=0
        s01=population[k][:chromosome_length-3]
        s02=population[k][chromosome_length-3:]
       
        if not (s01.count(1)==0 or s02.count(1)==0 ):      
            eval_v,eval_w=evaluate_individual(population[k])
            if(eval_w>0):
                
                for i in range(chromosome_length): 
                    #print("chromosom")
                    #print(i)
                    w += objects[i]["cost"]*population[k][i]
                    valu += objects[i]["duration"]*population[k][i]
   
                if (w<=maximum_cost):
                    print(solution,"eme solution")
                    #print("individual",population[k])
                    so=""
                    for o in range(len(population[k])):                  
                        if (population[k][o]==1):
                            so=so+"C"+str(o)+""
                    print(so)    
                    print("total duration :", valu)
                    print("Cout total  :", w)
                    solution=solution+1
    best_individual=[meilleur_val,meilleur_cost]
    return best_individual,population
