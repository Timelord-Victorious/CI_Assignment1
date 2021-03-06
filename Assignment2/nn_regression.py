import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.neural_network.multilayer_perceptron import MLPRegressor
import matplotlib.pyplot as plt

from nn_regression_plot import plot_mse_vs_neurons, plot_mse_vs_iterations, plot_learned_function, \
    plot_mse_vs_alpha, plot_bars_early_stopping_mse_comparison

ACTIVATION = 'logistic'

"""
Computational Intelligence TU - Graz
Assignment 2: Neural networks
Part 1: Regression with neural networks

This file contains functions to train and test the neural networks corresponding the the questions in the assignment,
as mentioned in comments in the functions.
Fill in all the sections containing TODO!
"""

__author__ = 'bellec,subramoney'


def calculate_mse(nn, x, y):
    """
    Calculate the mean squared error on the training and test data given the NN model used.
    :param nn: An instance of MLPRegressor or MLPClassifier that has already been trained using fit
    :param x: The data
    :param y: The targets
    :return: Training MSE, Testing MSE
    """
    ## TODO - done
    return mean_squared_error(y, nn.predict(x))


def ex_1_1_a(x_train, x_test, y_train, y_test):
    """
    Solution for exercise 1.1 a)
    Remember to set alpha to 0 when initializing the model
    :param x_train: The training dataset
    :param x_test: The testing dataset
    :param y_train: The training targets
    :param y_test: The testing targets
    :return:
    """

    ## TODO - done
    # using 8 hidden neurons
    n_h = [2, 8, 40]

    for i in n_h:
        # use random state for a fixed split - guarantees always same output (200 seems beautiful)
        nn = MLPRegressor(activation='logistic', solver='lbfgs', alpha=0.0, hidden_layer_sizes=(i,), max_iter=200,
                          random_state=200)
        nn.fit(x_train, y_train)

        pred_train_y = nn.predict(x_train)
        pred_test_y = nn.predict(x_test)

        plot_learned_function(n_h, x_train, y_train, pred_train_y, x_test, y_test, pred_test_y)


def ex_1_1_b(x_train, x_test, y_train, y_test):
    """
    Solution for exercise 1.1 b)
    Remember to set alpha to 0 when initializing the model
    :param x_train: The training dataset
    :param x_test: The testing dataset
    :param y_train: The training targets
    :param y_test: The testing targets
    :return:
    """

    ## TODO - done
    n_h = 8
    train_array = np.zeros(10)
    test_array = np.zeros(10)
    for i in range(0, 10):
        nn = MLPRegressor(activation='logistic', solver='lbfgs', alpha=0.0, hidden_layer_sizes=(n_h,), max_iter=200,
                          random_state=i)
        nn.fit(x_train, y_train)
        test_array[i] = calculate_mse(nn, x_test, y_test)
        train_array[i] = calculate_mse(nn, x_train, y_train)

    print("MEAN:\n", np.mean(train_array))
    print("Standard derivation:\n", np.std(train_array))
    print("Train MSE:\n", train_array)
    print("Test MSE:\n", test_array)


def ex_1_1_c(x_train, x_test, y_train, y_test):
    """
    Solution for exercise 1.1 c)
    Remember to set alpha to 0 when initializing the model
    Use max_iter = 10000 and tol=1e-8
    :param x_train: The training dataset
    :param x_test: The testing dataset
    :param y_train: The training targets
    :param y_test: The testing targets
    :return:
    """

    ## TODO
    n_h = [1, 2, 3, 4, 6, 8, 12, 20, 40]
    train_array = np.zeros((9, 10))
    test_array = np.zeros((9, 10))

    for n in n_h:
        for i in range(0, 10):
            index = n_h.index(n)
            nn = MLPRegressor(tol=1e-8, activation='logistic', solver='lbfgs', alpha=0.0,
                              hidden_layer_sizes=(n_h[index],),
                              max_iter=10000, random_state=i)

            nn.fit(x_train, y_train)
            train_array[index][i] = calculate_mse(nn, x_train, y_train)
            test_array[index][i] = calculate_mse(nn, x_test, y_test)

            y_pred_train = nn.predict(x_train)
            y_pred_test = nn.predict(x_test)

            if n == 1:
                plot_learned_function(n, x_train, y_train, y_pred_train, x_test, y_test, y_pred_test)

    plot_mse_vs_neurons(np.array(train_array), np.array(test_array), n_h)


def ex_1_1_d(x_train, x_test, y_train, y_test):
    """
    Solution for exercise 1.1 b)
    Remember to set alpha to 0 when initializing the model
    Use n_iterations = 10000 and tol=1e-8
    :param x_train: The training dataset
    :param x_test: The testing dataset
    :param y_train: The training targets
    :param y_test: The testing targets
    :return:
    """

    ## TODO - done
    n_h = [2, 8, 40]

    iterations = 10000
    train_array = np.zeros((3, iterations))
    test_array = np.zeros((3, iterations))

    #solver = 'adam'
    #solver = 'lbfgs'
    #solver = 'sgd'

    for n in n_h:
        nn = MLPRegressor(tol=1e-8, activation='logistic', solver='adam', alpha=0.0, hidden_layer_sizes=(n,),
                          max_iter=1, random_state=0, warm_start=True)

        for i in range(0, iterations):
            index = n_h.index(n)
            nn.fit(x_train, y_train)
            train_array[index][i] = calculate_mse(nn, x_train, y_train)
            test_array[index][i] = calculate_mse(nn, x_test, y_test)

    plot_mse_vs_iterations(train_array, test_array, iterations, n_h)


def ex_1_2_a(x_train, x_test, y_train, y_test):
    """
    Solution for exercise 1.2 a)
    Remember to set alpha to 0 when initializing the model
    :param x_train: The training dataset
    :param x_test: The testing dataset
    :param y_train: The training targets
    :param y_test: The testing targets
    :return:
    """
    ## TODO - done
    n_h = 40
    test_array = np.zeros((11, 10))
    train_array = np.zeros((11, 10))
    alphas = [pow(10, i) for i in range(-8, 3)]

    for alpha in alphas:
        for j in range(0, 10):
            index = alphas.index(alpha)
            nn = MLPRegressor(activation='logistic', solver='lbfgs', alpha=alpha, hidden_layer_sizes=(n_h,),
                              max_iter=200, random_state=j)

            nn.fit(x_train, y_train)
            test_array[index][j] = calculate_mse(nn, x_test, y_test)
            train_array[index][j] = calculate_mse(nn, x_train, y_train)

    plot_mse_vs_alpha(train_array, test_array, alphas)


def ex_1_2_b(x_train, x_test, y_train, y_test):
    """
    Solution for exercise 1.2 b)
    Remember to set alpha and momentum to 0 when initializing the model
    :param x_train: The training dataset
    :param x_test: The testing dataset
    :param y_train: The training targets
    :param y_test: The testing targets
    :return:
    """

    ## TODO

    np.random.shuffle(x_train)
    np.random.shuffle(y_train)

    x_train_half_size = int(len(x_train) / 2)
    y_train_half_size = int(len(y_train) / 2)
    x_valid = x_train[x_train_half_size:]
    x_train = x_train[:x_train_half_size]

    y_valid = y_train[y_train_half_size:]
    y_train = y_train[:y_train_half_size]

    n = 40
    alpha = pow(10, -3)
    iteration = 2000
    random_seed = 10
    max_iter = 20

    mse_test = np.zeros((iteration, random_seed))
    mse_valid = np.zeros((iteration, random_seed))

    mse_last_iter = []
    mse_min_valid = []
    mse_ideal_min_test = []

    for seed in range(0, random_seed):
        nn = MLPRegressor(alpha=alpha, activation=ACTIVATION, solver='lbfgs', hidden_layer_sizes=(n,),
                          max_iter=max_iter, random_state=seed, momentum=False)

        mse = 0
        for i in range(0, iteration):
            nn.fit(x_train, y_train)
            mse = calculate_mse(nn, x_test, y_test)
            mse_test[i][seed] = mse
            mse_valid[i][seed] = calculate_mse(nn, x_valid, y_valid)

        mse_last_iter.append(mse)
        mse_min_valid.append(np.min(mse_valid[seed]))
        mse_ideal_min_test.append(np.min(mse_test[seed]))

    plot_bars_early_stopping_mse_comparison(mse_last_iter, mse_min_valid, mse_ideal_min_test)


def ex_1_2_c(x_train, x_test, y_train, y_test):
    """
    Solution for exercise 1.2 c)
    :param x_train:
    :param x_test:
    :param y_train:
    :param y_test:
    :return:
    """
    ## TODO

    np.random.shuffle(x_train)
    np.random.shuffle(y_train)

    x_train_half_size = int(len(x_train) / 2)
    y_train_half_size = int(len(y_train) / 2)
    x_valid = x_train[x_train_half_size:]
    x_train = x_train[:x_train_half_size]

    y_valid = y_train[y_train_half_size:]
    y_train = y_train[:y_train_half_size]

    n = 40
    alpha = pow(10, -3)
    iteration = 100
    random_seed = 10
    max_iter = 20

    mse_test = np.zeros((iteration, random_seed))
    mse_valid = np.zeros((iteration, random_seed))
    mse_train = np.zeros((iteration, random_seed))

    mse_test_early_stopping = []
    mse_train_early_stopping = []
    mse_valid_early_stopping = []

    nn = MLPRegressor(alpha=alpha, activation=ACTIVATION, solver='lbfgs', hidden_layer_sizes=(n,),
                      max_iter=max_iter, momentum=False)

    for seed in range(0, random_seed):
        nn.random_state = seed

        for i in range(0, iteration):
            nn.fit(x_train, y_train)
            mse_test[i][seed] = calculate_mse(nn, x_train, y_train)
            mse_train[i][seed] = calculate_mse(nn, x_test, y_test)
            mse_valid[i][seed] = calculate_mse(nn, x_valid, y_valid)

        early_stopping = mse_valid[:, seed]
        early_stopping_index = np.argmin(early_stopping)
        mse_test_early_stopping.append(mse_train[early_stopping_index, seed])
        mse_train_early_stopping.append(mse_test[early_stopping_index, seed])
        mse_valid_early_stopping.append(mse_valid[early_stopping_index, seed])

    mse_test_mean = np.mean(mse_test_early_stopping)
    mse_test_standard_deviation = np.std(mse_test_early_stopping)

    mse_train_mean = np.mean(mse_train_early_stopping)
    mse_train_standard_deviation = np.std(mse_train_early_stopping)

    mse_valid_mean = np.mean(mse_valid_early_stopping)
    mse_valid_standard_deviation = np.std(mse_valid_early_stopping)

    optimal_seed = np.argmin(mse_valid_early_stopping)
    mse_test_optimal = np.argmin(mse_test_early_stopping)
    mse_train_optimal = np.argmin(mse_train_early_stopping)
    mse_valid_optimal = np.argmin(mse_valid_early_stopping)

    print("Mean Square Error Test: ")
    print("Mean: " + str(mse_test_mean))
    print("Standard deviation: " + str(mse_test_standard_deviation))

    print()
    print("Mean Square Error Training: ")
    print("Mean: " + str(mse_train_mean))
    print("Standard deviation: " + str(mse_train_standard_deviation))

    print()
    print("Mean Square Error Validation: ")
    print("Mean: " + str(mse_valid_mean))
    print("Standard deviation: " + str(mse_valid_standard_deviation))

    print("\n")
    print("Optimal seed: ", optimal_seed)
    print("Training MSE with optimal seed: " + str(mse_test_optimal))
    print("Testing MSE with optimal seed:  " + str(mse_train_optimal))
    print("Validation with optimal seed:   " + str(mse_valid_optimal))
