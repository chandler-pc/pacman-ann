import random
import numpy as np
from neural_network import NeuralNetwork

class GeneticAlgorithm:
    def __init__(self, population_size, input_size, hidden_size1, hidden_size2, output_size):
        self.population_size = population_size
        self.input_size = input_size
        self.hidden_size1 = hidden_size1
        self.hidden_size2 = hidden_size2
        self.output_size = output_size
        self.population = [NeuralNetwork(input_size, hidden_size1, hidden_size2, output_size) for _ in range(population_size)]
    
    def mutate(self, nn, mutation_rate):
        for i in range(nn.weights_input_hidden1.shape[0]):
            for j in range(nn.weights_input_hidden1.shape[1]):
                if random.random() < mutation_rate:
                    nn.weights_input_hidden1[i][j] += np.random.randn()
        
        for i in range(nn.weights_hidden1_hidden2.shape[0]):
            for j in range(nn.weights_hidden1_hidden2.shape[1]):
                if random.random() < mutation_rate:
                    nn.weights_hidden1_hidden2[i][j] += np.random.randn()
        
        for i in range(nn.weights_hidden2_output.shape[0]):
            for j in range(nn.weights_hidden2_output.shape[1]):
                if random.random() < mutation_rate:
                    nn.weights_hidden2_output[i][j] += np.random.randn()
    
    def crossover(self, parent1, parent2):
        child = NeuralNetwork(self.input_size, self.hidden_size1, self.hidden_size2, self.output_size)
        
        for i in range(parent1.weights_input_hidden1.shape[0]):
            for j in range(parent1.weights_input_hidden1.shape[1]):
                if random.random() > 0.5:
                    child.weights_input_hidden1[i][j] = parent1.weights_input_hidden1[i][j]
                else:
                    child.weights_input_hidden1[i][j] = parent2.weights_input_hidden1[i][j]
        
        for i in range(parent1.weights_hidden1_hidden2.shape[0]):
            for j in range(parent1.weights_hidden1_hidden2.shape[1]):
                if random.random() > 0.5:
                    child.weights_hidden1_hidden2[i][j] = parent1.weights_hidden1_hidden2[i][j]
                else:
                    child.weights_hidden1_hidden2[i][j] = parent2.weights_hidden1_hidden2[i][j]
        
        for i in range(parent1.weights_hidden2_output.shape[0]):
            for j in range(parent1.weights_hidden2_output.shape[1]):
                if random.random() > 0.5:
                    child.weights_hidden2_output[i][j] = parent1.weights_hidden2_output[i][j]
                else:
                    child.weights_hidden2_output[i][j] = parent2.weights_hidden2_output[i][j]
        
        return child
    
    def evolve(self, fitness_scores, mutation_rate=0.2):
        new_population = []
        for i in range(self.population_size):
            parent1 = self.select(fitness_scores)
            parent2 = self.select(fitness_scores)
            child = self.crossover(parent1, parent2)
            self.mutate(child, mutation_rate)
            new_population.append(child)
        self.population = new_population
    
    def select(self, fitness_scores):
        total_fitness = sum(fitness_scores)
        pick = random.uniform(0, total_fitness)
        current = 0
        for i, nn in enumerate(self.population):
            current += fitness_scores[i]
            if current > pick:
                return nn
