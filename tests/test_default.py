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
steps = 50
n_simuls = 10
#nf = 50
#nm = 100

# output csv file generation params
output_csv_dir = 'outputs'
output_csv_name = 'simul_results'
output_csv = 'mean'     # can be 'all', 'mean' or 'none'
output_costs = 'mean'  # same as above, 'all', 'mean' or 'none'

# data files
densities_file = os.path.join('..', 'data', 'Densidades.csv')
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

sample_n_moths = 96
sample_area = 315
# n_flies_list = [0,1500, 3000, 4500, 6000]

# flies list declaration
fly_step = 1500
fly_max = 40000
n_flies_list = list(range(0, fly_max, fly_step))
print(n_flies_list)

success, cost = sc.bayes_cost_function(pd.read_csv(densities_file), sample_n_moths, sample_area, n_flies_list,
                                       pd.read_csv(os.path.join(output_csv_dir, output_csv_name + '_cost.csv'),
                                                   index_col=[0]))
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
    cost.to_csv(initial_pops_file)
