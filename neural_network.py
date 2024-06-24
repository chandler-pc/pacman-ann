import numpy as np

class NeuralNetwork:
    def __init__(self, input_size, hidden_size1, hidden_size2, output_size):
        self.input_size = input_size
        self.hidden_size1 = hidden_size1
        self.hidden_size2 = hidden_size2
        self.output_size = output_size
        
        self.weights_input_hidden1 = np.random.randn(self.input_size, self.hidden_size1) * np.sqrt(2.0 / self.input_size)
        self.weights_hidden1_hidden2 = np.random.randn(self.hidden_size1, self.hidden_size2) * np.sqrt(2.0 / self.hidden_size1)
        self.weights_hidden2_output = np.random.randn(self.hidden_size2, self.output_size) * np.sqrt(2.0 / self.hidden_size2)
    
    def softmax(self, x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum(axis=0)
    
    def relu(self, x):
        return np.maximum(0, x)
    
    def forward(self, inputs):
        hidden1 = self.relu(np.dot(inputs, self.weights_input_hidden1))
        hidden2 = self.relu(np.dot(hidden1, self.weights_hidden1_hidden2))
        output = self.softmax(np.dot(hidden2, self.weights_hidden2_output))
        return output
    
    def predict(self, inputs):
        return self.forward(inputs)
