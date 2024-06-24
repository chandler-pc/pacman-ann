from game_nn import Game_NN
from genetic_algorithm import GeneticAlgorithm
import pickle
import numpy as np

population_size = 15

num_generations = 5
training_time = 5  # segundos

best_population = []
best_fitness_scores = []

ga = GeneticAlgorithm(population_size=population_size, input_size=6, hidden_size1=10, hidden_size2=10, output_size=4)

for generation in range(num_generations):
    print(f"Generation: {generation}")
    fitness_scores = []
    for nn in ga.population:
        game = Game_NN(nn,training_time)
        game.run()
        fitness_scores.append(game.points)
        print("Points:", game.points)
    print("Fitness Scores:", fitness_scores)
    
    # elitismo para mantener los mejores individuos de la generación anterior
    # if generation > 0:
    #     avg_fitness = np.mean(fitness_scores)
    #     new_population = [ga.population[i] for i in range(len(fitness_scores)) if fitness_scores[i] >= avg_fitness]
    #     num_to_fill = ga.population_size - len(new_population)

    #     # Penalizar la generación anterior
    #     penalized_previous_fitness_scores = [score - 1 for score in ga.previous_fitness_scores]

    #     # Rellenar el resto con los mejores individuos de la generación anterior penalizada
    #     sorted_indices_previous = np.argsort(penalized_previous_fitness_scores)[::-1]  # Orden descendente
    #     best_from_previous = [ga.previous_population[i] for i in sorted_indices_previous[:num_to_fill]]
    #     new_population.extend(best_from_previous)
        
    #     # Actualizar la población actual con las mejores de ambas generaciones
    #     ga.population = new_population

    #     # Actualizar los puntajes de fitness
    #     fitness_scores = [fitness_scores[i] for i in range(len(fitness_scores)) if fitness_scores[i] >= avg_fitness]
    #     fitness_scores.extend([penalized_previous_fitness_scores[i] for i in sorted_indices_previous[:num_to_fill]])
    
    ga.evolve(fitness_scores, mutation_rate=0.1, tournament_size=5)

index = np.argmax(fitness_scores)
print("Best fitness scores:", fitness_scores[index])
print("Best population:", index)
best_nn = ga.population[index]
with open("best_nn.pkl", "wb") as f:
    pickle.dump(best_nn, f)
