from game_nn import Game_NN
import pickle

# best_nn = pickle.load(open("prueba1.best_nn.pkl", "rb"))
# best_nn = pickle.load(open("prueba2.best_nn.pkl", "rb"))

best_nn = pickle.load(open("best_nn.pkl", "rb"))

game = Game_NN(best_nn)
game.run()