import os
import pickle
from app.game_nn import Game_NN

def load_best_nn(name_file='best_nn.pkl'):
    build_dir = 'build'
    best_nn_path = os.path.join(build_dir, name_file)
    return pickle.load(open(best_nn_path, "rb"))

def main():
    best_nn = load_best_nn('best_nn.pkl')
    game = Game_NN(best_nn)
    game.run()
    
if __name__ == "__main__":
    main()
