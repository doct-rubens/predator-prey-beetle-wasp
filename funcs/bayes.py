# -*- coding: utf-8 -*-
#
# Python file that will implement the Bayes cost function
# on the funcs subpackage.
#
# Receives as arguments:
# A       : area (float)
# n_moths : number of moths (int)
# n_flies : number of flies (int)
# cost    : cost without bayes (dataframe, has the 'n_flies' and the 'n_moths' columns)
# dens_moths       : list with moth densities
# prob_dens_moths : list with moth density probabilities
#
# If the cost dataframe has several different rows for the same n_moths
# and n_flies, it uses only the last one (expected to be the more 'recent' one)
#
# The interface for calling this function is responsible for the verification if the
# dataframes have all required values

from .poisson import poisson


def bayes_cost(dens_moths, prob_dens_moths, sample_n_moths, sample_area, n_flies, density_factor, costs):
    cost_b = 0
    norm_factor = 0
    for idx in range(len(dens_moths)):
        local_prob = poisson(sample_n_moths, sample_area, dens_moths[idx]) * prob_dens_moths[idx]
        cost_b += local_prob * costs[(costs['#moths'] == int(dens_moths[idx] * density_factor)) &
                                     (costs['#flies'] == n_flies)]['cost'].iloc[-1]
        norm_factor += local_prob

    return cost_b / norm_factor
