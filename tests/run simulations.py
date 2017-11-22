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
nf = 6000
nm = 2500

# output csv file generation params
output_csv_dir = 'outputs'
output_csv_name = 'simul_results'
output_csv = 'mean'     # can be 'all', 'mean' or 'none'
output_costs = 'mean'  # same as above, 'all', 'mean' or 'none'

# data files
densities_file = os.path.join('..', 'data', 'Densidades.csv')
initial_pops_file = os.path.join('..', 'data', 'my_initial_pops.csv')

# lines from the initial_pops_file that must be used to run
# simulations - [lower_bound, upper_bound (not included)]
# example: initial_pops_lines = [0, 3] will make the program run
# simulation for lines 0 and 1 only (2 in total)
initial_pops_lines = [200, 400]

u, w, sc, my_plotter = init_default()

# run a couple of simulation batches based on the missing
# values based on an external dataframe
sc.run_some_batches(pd.read_csv(initial_pops_file),
                    steps, n_simuls,
                    lines=initial_pops_lines,   # lines from file that must be executed
                    output_csv=output_csv,
                    output_costs=output_costs,
                    output_dir=output_csv_dir,
                    output_name=output_csv_name
                    )
