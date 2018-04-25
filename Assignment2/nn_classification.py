from sklearn.metrics import confusion_matrix, mean_squared_error

from sklearn.neural_network.multilayer_perceptron import MLPClassifier
from nn_classification_plot import plot_hidden_layer_weights, plot_histogram_of_acc
import numpy as np
from sklearn.metrics import confusion_matrix

__author__ = 'bellec,subramoney'

"""
Computational Intelligence TU - Graz
Assignment 2: Neural networks
Part 1: Regression with neural networks

This file contains functions to train and test the neural networks corresponding the the questions in the assignment,
as mentioned in comments in the functions.
Fill in all the sections containing TODO!
"""

ACTIVATION = 'tanh'


def ex_2_1(input2, target2):
    """
    Solution for exercise 2.1
    :param input2: The input from dataset2
    :param target2: The target from dataset2
    :return:
    """
    ## TODO

    nn = MLPClassifier(activation=ACTIVATION, solver='adam', hidden_layer_sizes=(6,), max_iter=200)
    target_ = target2[:, 1]
    nn.fit(input2, target2)
    hidden_layer_weights = nn.coefs_
    print(hidden_layer_weights)
    matrix = confusion_matrix(input2, target2)
    print(matrix)

    plot_hidden_layer_weights(hidden_layer_weights)

def ex_2_2(input1, target1, input2, target2):
    """
    Solution for exercise 2.2
    :param input1: The input from dataset1
    :param target1: The target from dataset1
    :param input2: The input from dataset2
    :param target2: The target from dataset2
    :return:
    """
    ## TODO
    pass
