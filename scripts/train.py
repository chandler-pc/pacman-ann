import os
import datetime
import pickle
import numpy as np
import matplotlib.pyplot as plt
from app.game_nn import Game_NN
from app.genetic_algorithm import GeneticAlgorithm

# Ejecutar algoritmo genético
def run_genetic_algorithm(population_size, input_size, hidden_size1, hidden_size2, output_size, generations, tournament_size):
    
    ga = GeneticAlgorithm(population_size, input_size, hidden_size1, hidden_size2, output_size)
    metrics = []
    
    for generation in range(generations):
        print(f"Generation: {generation}")
        fitness_scores = []
        for nn in ga.population:
            game = Game_NN(nn, 10)
            game.run()
            fitness_scores.append(game.points)
            print("Points:", game.points)
        print("Fitness Scores:", fitness_scores)
        # Guardar las métricas de la generación actual
        metrics.append(fitness_scores)  
        # Evolucionar la población
        ga.evolve(fitness_scores, tournament_size)

    # Guardar la mejor red neuronal
    save_best_nn(ga, fitness_scores, 'best_nn.pkl')
    save_metrics_graph(metrics)

# Guardar la mejor red neuronal y crear una copia de respaldo
def save_best_nn(ga, fitness_scores, name_file='best_nn.pkl'):
    build_dir = 'build'
    backup_dir = os.path.join(build_dir, 'backups')

    # Crear directorios si no existen
    os.makedirs(build_dir, exist_ok=True)
    os.makedirs(backup_dir, exist_ok=True)

    best_nn = ga.population[np.argmax(fitness_scores)]
    best_nn_path = os.path.join(build_dir, name_file)
    with open(best_nn_path, 'wb') as f:
        pickle.dump(best_nn, f)

    # Crear una copia de respaldo con la fecha y hora actual
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
    backup_path = os.path.join(backup_dir, f'{timestamp}.{name_file}')
    with open(backup_path, 'wb') as f:
        pickle.dump(best_nn, f)

    print(f"Best model saved to {best_nn_path} and backup created at {backup_path}")

def save_metrics_graph(metrics):
    build_dir = 'build'
    metrics_dir = os.path.join(build_dir, 'metrics')

    os.makedirs(metrics_dir, exist_ok=True)

    # Preparar los datos para el gráfico
    avg_fitness = [np.mean(scores) for scores in metrics]
    max_fitness = [np.max(scores) for scores in metrics]
    min_fitness = [np.min(scores) for scores in metrics]

    generations = range(len(metrics))

    # Crear el gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(generations, avg_fitness, label='Average Fitness')
    plt.plot(generations, max_fitness, label='Max Fitness')
    plt.plot(generations, min_fitness, label='Min Fitness')
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Fitness Over Generations')
    plt.legend()
    plt.grid(True)

    # Guardar el gráfico como imagen
    metrics_path = os.path.join(metrics_dir, 'fitness_metrics.png')
    plt.savefig(metrics_path)

    print(f"Metrics graph saved to {metrics_path}")

def main():
    # Parámetros del algoritmo genético
    population_size = 100 # Número de individuos en la población
    input_size = 6 # Número de entradas
    hidden_size1 = 16 # Número de neuronas en la primera capa oculta
    hidden_size2 = 8 # Número de neuronas en la segunda capa oculta
    output_size = 4 # Número de salidas
    generations = 10 # Número de generaciones
    tournament_size = 20  # Tamaño del torneo

    # Ejecutar algoritmo genético
    run_genetic_algorithm(population_size, input_size, hidden_size1, hidden_size2, output_size, generations, tournament_size)

if __name__ == "__main__":
    main()