# -*- coding: utf-8 -*-
#
# Python file that will implement the Bayes cost function
# on the funcs subpackage.
#
# Receives two arguments:
#    - distr_file : path to the file with the distribution data.
#    - simul_file : path to the file with the costs from the
#                   simulations
#    - A        : Area evaluated
#    - n_moths  : number of moths on the sample
#    - n_wasps  : initial number of wasps


def bayes_cost(distr_file, simul_file):

    # 1. save the moth densities on a list (or df) 'ro'

    # 2. for r in ro:

    #      2.1. evaluate the simple cost C(r, n_wasps) (it must be on the simul_file)
    #      2.2. evaluate Poisson(r | n_moths, A)
    #      2.3. take the product
    #      2.4. cumulatively add

    # 3. end

    pass
