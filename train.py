from game_nn import Game_NN
from genetic_algorithm import GeneticAlgorithm
import pickle
import numpy as np

ga = GeneticAlgorithm(population_size=5, input_size=6, hidden_size1=10, hidden_size2=10, output_size=4)

for generation in range(100):
    print(f"Generation: {generation}")
    fitness_scores = []
    for nn in ga.population:
        game = Game_NN(nn,5)
        game.run()
        fitness_scores.append(game.points)
        print("Points:", game.points)
    print("Fitness Scores:", fitness_scores)
    ga.evolve(fitness_scores, mutation_rate=0.2, tournament_size=3)

best_nn = ga.population[np.argmax(fitness_scores)]
pickle.dump(best_nn, open("best_nn.pkl", "wb"))

