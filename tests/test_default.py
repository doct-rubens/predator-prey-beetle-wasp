# -*- coding: utf-8 -*-
#
# Basic testing script that creates a sample
#     > universe
#     > world
#     > plotter
#     > simulation control
# with the default initialisation function and performs some operations

import pandas as pd
import os
from funcs.init_default import init_default

# simulation batch parameters
steps = 10
n_simuls = 3
nf = 50
nm = 100

# output csv file generation params
output_csv_dir = 'outputs'
output_csv_name = 'simul_results'
output_csv = 'mean'     # can be 'all', 'mean' or 'none'
output_costs = 'mean'  # same as above, 'all', 'mean' or 'none'

# data files
densities_file = os.path.join('..', 'data', 'my_densities.csv')
initial_pops_file = os.path.join('..', 'data', 'my_initial_pops.csv')

u, w, sc, my_plotter = init_default()

# run a couple of simulation batches based on the missing
# values based on an external dataframe
# sc.run_some_batches(pd.read_csv(initial_pops_file),
#                    steps, n_simuls,
#                    output_csv=output_csv,
#                    output_costs=output_costs,
#                    output_dir=output_csv_dir,
#                    output_name=output_csv_name
#                    )

# bayes cost function testing
sample_n_moths = 12
sample_area = 120
n_flies_list = [500, 1000, 1500]
success, cost = sc.bayes_cost_function(pd.read_csv(densities_file), sample_n_moths, sample_area, n_flies_list,
                                       pd.read_csv(os.path.join(output_csv_dir, output_csv_name + '_cost.csv')))
if success:
    bayes_cost_file = os.path.join(output_csv_dir, output_csv_name + '_bayes_cost.csv')
    print('bayes cost calculated!')
    print("results saved on file '{}'".format(bayes_cost_file))
    cost.to_csv(bayes_cost_file)
else:
    print('no success on calculating the bayes cost;')
    print('the following simulations are missing:')
    print(cost)
    print("saving these missing initial populations on file '{}'".format(initial_pops_file))
