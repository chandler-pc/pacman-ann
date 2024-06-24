import random
import numpy as np
from neural_network import NeuralNetwork

# Clase que implementa el algoritmo genético
class GeneticAlgorithm:
    
    # Constructor de la clase
    # Parámetros:
    # population_size: tamaño de la población
    # input_size: tamaño de la capa de entrada
    # hidden_size1: tamaño de la primera capa oculta
    # hidden_size2: tamaño de la segunda capa oculta
    # output_size: tamaño de la capa de salida
    def __init__(self, population_size, input_size, hidden_size1, hidden_size2, output_size):
        self.population_size = population_size
        self.input_size = input_size
        self.hidden_size1 = hidden_size1
        self.hidden_size2 = hidden_size2
        self.output_size = output_size
        self.population = [NeuralNetwork(input_size, hidden_size1, hidden_size2, output_size) for _ in range(population_size)]
        self.best_individuals = []
    
    # Método que muta la red neuronal
    # No se realizan cambios
    def mutate(self, nn, mutation_rate):
        # Itera sobre todas las filas de los pesos entre la capa de entrada y la primera capa oculta
        for i in range(nn.weights_input_hidden1.shape[0]):
            # Itera sobre todas las columnas de los pesos entre la capa de entrada y la primera capa oculta
            for j in range(nn.weights_input_hidden1.shape[1]):
                # Si un numero aleatorio es menor que la tasa de mutacion
                if random.random() < mutation_rate:
                    # Se realiza la mutación en el peso
                    nn.weights_input_hidden1[i][j] += np.random.randn()
        
        # Itera sobre todas las filas de los pesos entre la primera capa oculta y la segunda capa oculta
        for i in range(nn.weights_hidden1_hidden2.shape[0]):
            # Itera sobre todas las columnas de los pesos entre la primera capa oculta y la segunda capa oculta
            for j in range(nn.weights_hidden1_hidden2.shape[1]):
                # Si un numero aleatorio es menor que la tasa de mutacion
                if random.random() < mutation_rate:
                    # Se realiza la mutación en el peso
                    nn.weights_hidden1_hidden2[i][j] += np.random.randn()
        
        # Itera sobre todas las filas de los pesos entre la segunda capa oculta y la capa de salida
        for i in range(nn.weights_hidden2_output.shape[0]):
            # Itera sobre todas las columnas de los pesos entre la segunda capa oculta y la capa de salida
            for j in range(nn.weights_hidden2_output.shape[1]):
                # Si un numero aleatorio es menor que la tasa de mutacion
                if random.random() < mutation_rate:
                    # Se realiza la mutación en el peso
                    nn.weights_hidden2_output[i][j] += np.random.randn()
                    

    # Método que realiza el cruce de dos redes neuronales
    # def crossover(self, parent1, parent2):
    #     child = NeuralNetwork(self.input_size, self.hidden_size1, self.hidden_size2, self.output_size)
    #     for i in range(parent1.weights_input_hidden1.shape[0]):
    #         for j in range(parent1.weights_input_hidden1.shape[1]):
    #             if random.random() > 0.5:
    #                 child.weights_input_hidden1[i][j] = parent1.weights_input_hidden1[i][j]
    #             else:
    #                 child.weights_input_hidden1[i][j] = parent2.weights_input_hidden1[i][j]
    #     for i in range(parent1.weights_hidden1_hidden2.shape[0]):
    #         for j in range(parent1.weights_hidden1_hidden2.shape[1]):
    #             if random.random() > 0.5:
    #                 child.weights_hidden1_hidden2[i][j] = parent1.weights_hidden1_hidden2[i][j]
    #             else:
    #                 child.weights_hidden1_hidden2[i][j] = parent2.weights_hidden1_hidden2[i][j]
    #     for i in range(parent1.weights_hidden2_output.shape[0]):
    #         for j in range(parent1.weights_hidden2_output.shape[1]):
    #             if random.random() > 0.5:
    #                 child.weights_hidden2_output[i][j] = parent1.weights_hidden2_output[i][j]
    #             else:
    #                 child.weights_hidden2_output[i][j] = parent2.weights_hidden2_output[i][j]
    #     return child
    
    # Método de cruce de un solo punto
    # Mejoras:
    # - Preserva patrones de los padres: Mantiene segmentos completos de pesos de los padres
    # - Explotacion de patrones existentes: Mantiene segmentos ya explorados de los padres
    # - Exploración de nuevos patrones: Introduce variabilidad en la descendencia
    # - Reduce la complejidad del algoritmo: Simplifica el cruce de los pesos de la red neuronal
    def crossover(self, parent1, parent2):
        # Crea un hijo con las mismas dimensiones que los padres
        child = NeuralNetwork(self.input_size, self.hidden_size1, self.hidden_size2, self.output_size)
        
        # Selecciona un punto de cruce al azar
        point = random.randint(0, parent1.weights_input_hidden1.size)
        
        # Aplana los pesos de la capa de entrada a la primera capa oculta de los padres
        flat1 = parent1.weights_input_hidden1.flatten()
        flat2 = parent2.weights_input_hidden1.flatten()
        child_flat = np.concatenate([flat1[:point], flat2[point:]])
        child.weights_input_hidden1 = child_flat.reshape(parent1.weights_input_hidden1.shape)

        point = random.randint(0, parent1.weights_hidden1_hidden2.size)
        flat1 = parent1.weights_hidden1_hidden2.flatten()
        flat2 = parent2.weights_hidden1_hidden2.flatten()
        child_flat = np.concatenate([flat1[:point], flat2[point:]])
        child.weights_hidden1_hidden2 = child_flat.reshape(parent1.weights_hidden1_hidden2.shape)

        point = random.randint(0, parent1.weights_hidden2_output.size)
        flat1 = parent1.weights_hidden2_output.flatten()
        flat2 = parent2.weights_hidden2_output.flatten()
        child_flat = np.concatenate([flat1[:point], flat2[point:]])
        child.weights_hidden2_output = child_flat.reshape(parent1.weights_hidden2_output.shape)

        return child

    # Método que evoluciona la población
    # Mejorar con elitismo
    def evolve(self, fitness_scores, mutation_rate=0.2, tournament_size=3):
        new_population = []
        
        # Generar nuevos individuos mediante cruce y mutación para llenar la población
        while len(new_population) < self.population_size:
            parent1 = self.select(fitness_scores, tournament_size)
            parent2 = self.select(fitness_scores, tournament_size)
            child = self.crossover(parent1, parent2)
            self.mutate(child, mutation_rate)
            new_population.append(child)
        
        # Almacenar la población y los puntajes de fitness de la generación actual
        self.previous_population = self.population
        self.previous_fitness_scores = fitness_scores

        # Reemplazar la población actual con la nueva población
        self.population = new_population
    
    # Método de selección por torneo
    def select(self, fitness_scores, tournament_size):
        # Selecciona 'tournament_size' individuos al azar de la población
        tournament_indices = random.sample(range(len(self.population)), tournament_size)
        # Encuentra el individuo con el mejor fitness en el torneo
        best_index = tournament_indices[0]
        for idx in tournament_indices:
            if fitness_scores[idx] > fitness_scores[best_index]:
                best_index = idx
        # Devuelve el mejor individuo del torneo
        return self.population[best_index]

    # # Método de seleccion por ruleta
    # def select(self, fitness_scores):
    #     # Selecciona la suma total de los fitness
    #     total_fitness = sum(fitness_scores)
    #     # Selecciona un número aleatorio entre 0 y la suma total de los fitness
    #     pick = random.uniform(0, total_fitness)
    #     # Initializa una suma acumulada de los fitness
    #     current = 0
    #     # Por cada individuo en la población
    #     for i, nn in enumerate(self.population):
    #         # Suma el fitness del individuo actual al acumulado
    #         current += fitness_scores[i]
    #         # Si la suma acumulada es mayor al número aleatorio
    #         if current > pick:
    #             # Devuelve el individuo actual
    #             return nn
