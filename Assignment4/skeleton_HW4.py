# Filename: HW4_skeleton.py
# Author: Christian Knoll, Florian Kaum
# Edited: May, 2018
import random

import numpy as np
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import scipy.stats as stats
from scipy.misc import derivative

from scipy.stats import multivariate_normal


# --------------------------------------------------------------------------------
# Assignment 4
def main():
    # choose the scenario
    # scenario = 1  # all anchors are Gaussian
    # scenario = 2    # 1 anchor is exponential, 3 are Gaussian
    # scenario = 3  # all anchors are exponential

    Fx_list = np.zeros((3, 2000))
    x_list = np.zeros((3, 2000))
    for scenario in range(1, 4):

        # specify position of anchors
        p_anchor = np.array([[5, 5], [-5, 5], [-5, -5], [5, -5]])
        nr_anchors = np.size(p_anchor, 0)

        # position of the agent for the reference mearsurement
        p_ref = np.array([[0, 0]])
        # true position of the agent (has to be estimated)
        p_true = np.array([[2, -4]])
        #    p_true = np.array([[2,-4])

        plot_anchors_and_agent(nr_anchors, p_anchor, p_true, p_ref)

        # load measured data and reference measurements for the chosen scenario
        data, reference_measurement = load_data(scenario)

        # get the number of measurements
        assert (np.size(data, 0) == np.size(reference_measurement, 0))
        nr_samples = np.size(data, 0)

        # 1) ML estimation of model parameters
        # TODO
        params = parameter_estimation(reference_measurement, nr_anchors, p_anchor, p_ref)

        # 2) Position estimation using least squares
        # TODO
        if scenario == 2:
            exponential = True
        else:
            exponential = False

        pls_estimation = position_estimation_least_squares(data, nr_anchors, p_anchor, p_true, exponential, scenario)

        if (scenario == 3):
            # TODO: don't forget to plot joint-likelihood function for the first measurement

            # 3) Postion estimation using numerical maximum likelihood
            # TODO
            position_estimation_numerical_ml(data, nr_anchors, p_anchor, params, p_true)

            # 4) Position estimation with prior knowledge (we roughly know where to expect the agent)
            # TODO
            # specify the prior distribution
            prior_mean = p_true
            prior_cov = np.eye(2)
            position_estimation_bayes(data, nr_anchors, p_anchor, prior_mean, prior_cov, params, p_true)

        error = []
        for idx in range(0, nr_samples):
            error.append(
                np.sqrt((pls_estimation[idx, 0] - p_true[0][0]) ** 2 + (pls_estimation[idx, 1] - p_true[0][1]) ** 2))
        Fx, x = ecdf(error)
        Fx_list[scenario - 1, :] = Fx
        x_list[scenario - 1, :] = x

    for scenario in range(0, 3):
        plt.plot(x_list[scenario, :], Fx_list[scenario, :], label=('Scenario ' + str(scenario + 1)))

    plt.xlabel("x")
    plt.ylabel("Fx")
    plt.legend()
    plt.title('CDF')
    plt.show()


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
def parameter_estimation(reference_measurement, nr_anchors, p_anchor, p_ref):
    """ estimate the model parameters for all 4 anchors based on the reference measurements, i.e., for anchor i consider reference_measurement[:,i]
    Input:
        reference_measurement... nr_measurements x nr_anchors
        nr_anchors... scalar
        p_anchor... position of anchors, nr_anchors x 2
        p_ref... reference point, 2x2 """

    alpha = 1e-3
    params = np.zeros([1, nr_anchors])
    nr_samples = np.size(reference_measurement, 0)

    for i in range(0, nr_anchors):
        r_ref = np.linalg.norm(p_ref - p_anchor[i, :])

        normaltest = stats.normaltest(reference_measurement[:, i])
        pvalue = normaltest[1]

        # check whether a given anchor is Gaussian or exponential
        if pvalue > alpha:
            # normal
            sigma_sqrt = (np.linalg.norm(reference_measurement[:, i] - r_ref) ** 2) / nr_samples
            params[:, i] = sigma_sqrt
        else:
            # exponential
            lambda0 = nr_samples / np.sum(reference_measurement[:, i] - r_ref)
            params[:, i] = lambda0

    print("Params: ", params)

    return params


# --------------------------------------------------------------------------------
def position_estimation_least_squares(data, nr_anchors, p_anchor, p_true, use_exponential, scenario):
    """estimate the position by using the least squares approximation. 
    Input:
        data...distance measurements to unkown agent, nr_measurements x nr_anchors
        nr_anchors... scalar
        p_anchor... position of anchors, nr_anchors x 2 
        p_true... true position (needed to calculate error) 2x2 
        use_exponential... determines if the exponential anchor in scenario 2 is used, bool"""

    if use_exponential:
        p_anchor = np.delete(p_anchor, 0, axis=0)
        data = np.delete(data, 0, axis=1)
        nr_anchors = 3

    nr_samples = np.size(data, 0)

    # TODO set parameters
    # tol = ...  # tolerance
    # max_iter = ...  # maximum iterations for GN

    tol = 0.00001  # tolerance value to terminate, scalar"""
    max_iter = 10  # maximum number of iterations, scalar
    pls_estimates = np.zeros((nr_samples, 2))

    # TODO estimate position for  i in range(0, nr_samples)
    # least_squares_GN(p_anchor,p_start, r, max_iter, tol)
    for i in range(0, nr_samples):
        p_start = np.random.uniform(-5, 5, (2,))
        r = data[i, :]
        least_squares_gn = least_squares_GN(p_anchor, p_start, r, max_iter, tol)
        pls_estimates[i] = least_squares_gn

    # TODO calculate error measures and create plots----------------
    # The mean and variance of the position estimation error ||PLS - P||.
    np_abs = np.abs(pls_estimates - p_true)
    mean = np.mean(np_abs)
    var = np.var(np_abs)
    mean_x = np.mean(pls_estimates[:, 0])
    mean_y = np.mean(pls_estimates[:, 1])
    mu = np.array([mean_x, mean_y])
    cov = np.cov(np.transpose(pls_estimates))

    plt.scatter(pls_estimates[:, 0], pls_estimates[:, 1])

    xmin = np.min(pls_estimates[:, 0])
    xmax = np.max(pls_estimates[:, 0])
    ymin = np.min(pls_estimates[:, 1])
    ymax = np.max(pls_estimates[:, 1])

    print("Mean: ", mean)
    print("Var: ", var)

    # Scatter plots of the estimated positions. Fit a two-dimensional Gaussian distribution
    # to the point cloud of estimated positions and draw its contour lines. You can use the
    # provided function plot_gauss_contour(mu,cov,xmin,xmax,ymin,ymax,title).
    # Do the estimated positions look Gaussian?
    # Input:
    #   mu... mean vector, 2x1
    #   cov...covariance matrix, 2x2
    #   xmin,xmax... minimum and maximum value for width of plot-area, scalar
    #   ymin,ymax....minimum and maximum value for height of plot-area, scalar
    #   title... title of the plot (optional), string"""

    title = "Scenario " + str(scenario)

    plot_gauss_contour(mu, cov, xmin, xmax, ymin, ymax, title)

    return pls_estimates


# --------------------------------------------------------------------------------
def position_estimation_numerical_ml(data, nr_anchors, p_anchor, lambdas, p_true):
    """ estimate the position by using a numerical maximum likelihood estimator
    Input:
        data...distance measurements to unkown agent, nr_measurements x nr_anchors
        nr_anchors... scalar
        p_anchor... position of anchors, nr_anchors x 2
        lambdas... estimated parameters (scenario 3), nr_anchors x 1
        p_true... true position (needed to calculate error), 2x2 """
    # TODO

    left = min(p_anchor[1, :])
    right = max(p_anchor[1, :])
    top = max(p_anchor[2, :])
    bottom = min(p_anchor[2, :])
    step = 0.05

    x = left
    y = bottom

    j_l = np.zeros((10 * 20, 10 * 20))
    for x_cord in range(-5, 5):
        for y_cord in range(-5, 5):
            prop = np.zeros(nr_anchors)
            x_i = p_anchor[:, 0]
            y_i = p_anchor[:, 1]
            d = np.sqrt(np.power(x_i - x, 2) + (np.power(y_i - y, 2)))

            enum = enumerate(zip(data[0, :], d))
            for i, (r_i, d_i) in enum:
                if r_i >= d_i:
                    prop[i] = lambdas[0, i] * np.exp(-lambdas[0, i]) * (r_i - d_i)
                else:
                    prop[i] = 0

                j_l[x_cord, y_cord] = np.prod(prop)
                y += step

            x += step
            y = left

    xmin = np.min(j_l[:, 0])
    xmax = np.max(j_l[:, 0])
    ymin = np.min(j_l[:, 1])
    ymax = np.max(j_l[:, 1])
    j_l_max = np.argmax(j_l)

    print("jLmax ", j_l_max)
    print("ymin: ", ymin, "  xmin: ", xmin)
    print("xmax: ", xmax, "  ymax: ", ymax)

    plot_anchors_and_agent(nr_anchors, p_anchor, p_true, j_l)


# --------------------------------------------------------------------------------
def position_estimation_bayes(data, nr_anchors, p_anchor, prior_mean, prior_cov, lambdas, p_true):
    """ estimate the position by accounting for prior knowledge that is specified by a bivariate Gaussian
    Input:
         data...distance measurements to unkown agent, nr_measurements x nr_anchors
         nr_anchors... scalar
         p_anchor... position of anchors, nr_anchors x 2
         prior_mean... mean of the prior-distribution, 2x1
         prior_cov... covariance of the prior-dist, 2x2
         lambdas... estimated parameters (scenario 3), nr_anchors x 1
         p_true... true position (needed to calculate error), 2x2 """
    # TODO
    pass


# --------------------------------------------------------------------------------
def least_squares_GN(p_anchor, p_start, r: np.ndarray, max_iter, tol):
    """ apply Gauss Newton to find the least squares solution
    Input:
        p_anchor... position of anchors, nr_anchors x 2
        p_start... initial position, 2x1
        r... distance_estimate, nr_anchors x 1
        max_iter... maximum number of iterations, scalar
        tol... tolerance value to terminate, scalar"""

    entries = r.size
    for iteration in range(0, max_iter):
        jr = np.zeros((entries, 2))
        d = np.zeros((entries,))
        x = p_start[0]
        y = p_start[1]

        for i in range(0, entries):
            # x − xi /dist((xi − x)² + (yi − y)²)
            x_i = p_anchor[i, 0]
            y_i = p_anchor[i, 1]
            # x − xi / dist((xi − x)² + (yi − y)²)
            dist = np.sqrt(np.power(x_i - x, 2) + np.power(y_i - y, 2))
            d[i] = dist
            jr[i, 0] = (x_i - x) / dist  # TODO why x_i - x
            # y − yi / dist((xi − x)² + (yi − y)²
            jr[i, 1] = (y_i - y) / dist  # TODO why y_i - y

        matmul_inv = np.matmul(np.transpose(jr), jr)
        inv = np.linalg.inv(matmul_inv)
        matmul_factor1 = np.matmul(inv, np.transpose(jr))
        matmul_factor2 = r - d
        matmul_product = np.matmul(matmul_factor1, matmul_factor2)
        p_start = p_start - matmul_product
        estimated_position = np.linalg.norm(matmul_product)
        if estimated_position < tol:
            break

    return p_start


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------------------
def plot_gauss_contour(mu, cov, xmin, xmax, ymin, ymax, title="Title"):
    """ creates a contour plot for a bivariate gaussian distribution with specified parameters

    Input:
      mu... mean vector, 2x1
      cov...covariance matrix, 2x2
      xmin,xmax... minimum and maximum value for width of plot-area, scalar
      ymin,ymax....minimum and maximum value for height of plot-area, scalar
      title... title of the plot (optional), string"""

    # npts = 100
    delta = 0.025
    x = np.arange(xmin, xmax, delta)
    y = np.arange(ymin, ymax, delta)
    X, Y = np.meshgrid(x, y)
    Z = mlab.bivariate_normal(X, Y, np.sqrt(cov[0][0]), np.sqrt(cov[1][1]), mu[0], mu[1], cov[0][1])
    plt.plot([mu[0]], [mu[1]], 'r+')  # plot the mean as a single point
    CS = plt.contour(X, Y, Z)
    plt.clabel(CS, inline=1, fontsize=10)
    plt.title(title)
    plt.show()
    return


# --------------------------------------------------------------------------------
def ecdf(realizations):
    """ computes the empirical cumulative distribution function for a given set of realizations.
    The output can be plotted by plt.plot(x,Fx)

    Input:
      realizations... vector with realizations, Nx1
    Output:
      x... x-axis, Nx1
      Fx...cumulative distribution for x, Nx1"""
    x = np.sort(realizations)
    Fx = np.linspace(0, 1, len(realizations))
    return Fx, x


# --------------------------------------------------------------------------------
def load_data(scenario):
    """ loads the provided data for the specified scenario
    Input:
        scenario... scalar
    Output:
        data... contains the actual measurements, nr_measurements x nr_anchors
        reference.... contains the reference measurements, nr_measurements x nr_anchors"""
    data_file = 'measurements_' + str(scenario) + '.data'
    ref_file = 'reference_' + str(scenario) + '.data'

    data = np.loadtxt(data_file, skiprows=0)
    reference = np.loadtxt(ref_file, skiprows=0)

    return (data, reference)


# --------------------------------------------------------------------------------
def plot_anchors_and_agent(nr_anchors, p_anchor, p_true, p_ref=None):
    """ plots all anchors and agents
    Input:
        nr_anchors...scalar
        p_anchor...positions of anchors, nr_anchors x 2
        p_true... true position of the agent, 2x1
        p_ref(optional)... position for reference_measurements, 2x1"""
    # plot anchors and true position
    plt.axis([-6, 6, -6, 6])
    for i in range(0, nr_anchors):
        plt.plot(p_anchor[i, 0], p_anchor[i, 1], 'bo')
        plt.text(p_anchor[i, 0] + 0.2, p_anchor[i, 1] + 0.2, r'$p_{a,' + str(i) + '}$')
    plt.plot(p_true[0, 0], p_true[0, 1], 'r*')
    plt.text(p_true[0, 0] + 0.2, p_true[0, 1] + 0.2, r'$p_{true}$')
    if p_ref is not None:
        plt.plot(p_ref[0, 0], p_ref[0, 1], 'r*')
        plt.text(p_ref[0, 0] + 0.2, p_ref[0, 1] + 0.2, '$p_{ref}$')
    plt.xlabel("x/m")
    plt.ylabel("y/m")
    plt.show()
    pass


# --------------------------------------------------------------------------------
# --------------------------------------------------------------------------------
if __name__ == '__main__':
    main()
