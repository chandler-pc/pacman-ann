import random
import numpy as np
from app.neural_network import NeuralNetwork

# Clase que implementa el algoritmo genético
class GeneticAlgorithm:
    def __init__(self, population_size, input_size, hidden_size1, hidden_size2, output_size, mutation_rate=0.05, regularization_strength=0.01):
        self.population_size = population_size
        self.input_size = input_size
        self.hidden_size1 = hidden_size1
        self.hidden_size2 = hidden_size2
        self.output_size = output_size
        self.mutation_rate = mutation_rate
        self.regularization_strength = regularization_strength
        self.population = [NeuralNetwork(input_size, hidden_size1, hidden_size2, output_size) for _ in range(population_size)]

    def mutate(self, nn):
        for layer in nn.get_weights():
            for i in range(layer.shape[0]):
                for j in range(layer.shape[1]):
                    if random.random() < self.mutation_rate:
                        layer[i][j] += np.random.randn()

    def crossover(self, parent1, parent2):
        child = NeuralNetwork(self.input_size, self.hidden_size1, self.hidden_size2, self.output_size)
        for layer1, layer2, layer_child in zip(parent1.get_weights(), parent2.get_weights(), child.get_weights()):
            rows, cols = layer1.shape
            if random.random() > 0.5:  # Decide si cruzar en filas o columnas
                crossover_point = random.randint(0, rows - 1)
                for i in range(crossover_point):
                    for j in range(cols):
                        layer_child[i][j] = layer1[i][j]
                for i in range(crossover_point, rows):
                    for j in range(cols):
                        layer_child[i][j] = layer2[i][j]
            else:
                crossover_point = random.randint(0, cols - 1)
                for i in range(rows):
                    for j in range(crossover_point):
                        layer_child[i][j] = layer1[i][j]
                for i in range(rows):
                    for j in range(crossover_point, cols):
                        layer_child[i][j] = layer2[i][j]
        return child

    def apply_regularization(self, nn):
        for layer in nn.get_weights():
            layer -= self.regularization_strength * layer

    def evolve(self, fitness_scores, tournament_size=3):
        new_population = []
        # Elitismo: mantener los mejores individuos
        elite_size = int(0.1 * self.population_size)
        elite_indices = np.argsort(fitness_scores)[-elite_size:]
        print("Elite indices:", elite_indices) # Imprimir los índices de los mejores individuos
        elite_individuals = [self.population[i] for i in elite_indices]
        
        new_population.extend(elite_individuals)

        for _ in range(self.population_size - elite_size):
            parent1 = self.select(fitness_scores, tournament_size) # Selección de padres
            parent2 = self.select(fitness_scores, tournament_size) # Selección de padres
            child = self.crossover(parent1, parent2) # Cruce para combinar información genética
            self.mutate(child) # Mutación para introducir variabilidad
            self.apply_regularization(child) # Regularización para evitar overfitting
            new_population.append(child) # Agregar hijo a la nueva población
            
        # Aplicar regularización L2 a la nueva población
        for nn in new_population:
            self.apply_regularization(nn)

        self.population = new_population

    def select(self, fitness_scores, tournament_size):
        tournament_indices = random.sample(range(len(self.population)), tournament_size)
        best_index = max(tournament_indices, key=lambda idx: fitness_scores[idx])
        return self.population[best_index]