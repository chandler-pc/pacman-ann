import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size1, hidden_size2, output_size, dropout_rate=0.5):
        self.input_size = input_size
        self.hidden_size1 = hidden_size1
        self.hidden_size2 = hidden_size2
        self.output_size = output_size
        self.dropout_rate = dropout_rate
        
        # Inicialización He para los pesos
        self.weights_input_hidden1 = self.he_initialization(self.input_size, self.hidden_size1)
        self.weights_hidden1_hidden2 = self.he_initialization(self.hidden_size1, self.hidden_size2)
        self.weights_hidden2_output = self.he_initialization(self.hidden_size2, self.output_size)

    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)

    def relu(self, x):
        return np.maximum(0, x)

    def dropout(self, x, rate):
        mask = np.random.binomial(1, 1 - rate, size=x.shape)
        return x * mask

    def batch_norm(self, x):
        mean = np.mean(x, axis=0)
        variance = np.var(x, axis=0)
        return (x - mean) / np.sqrt(variance + 1e-8)

    def forward(self, inputs):
        hidden1 = self.relu(np.dot(inputs, self.weights_input_hidden1))
        hidden1 = self.batch_norm(hidden1)
        hidden1 = self.dropout(hidden1, self.dropout_rate)

        hidden2 = self.relu(np.dot(hidden1, self.weights_hidden1_hidden2))
        hidden2 = self.batch_norm(hidden2)
        hidden2 = self.dropout(hidden2, self.dropout_rate)

        output = self.softmax(np.dot(hidden2, self.weights_hidden2_output))
        return output

    def predict(self, inputs):
        return self.forward(inputs)
    
    def get_weights(self):
        return [self.weights_input_hidden1, self.weights_hidden1_hidden2, self.weights_hidden2_output]

    def he_initialization(self, input_size, output_size):
        return np.random.randn(input_size, output_size) * np.sqrt(2.0 / input_size)