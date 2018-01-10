# -*- coding: utf-8 -*-
#
# Basic testing script that creates a sample
#     > universe
#     > world
#     > plotter
#     > simulation control
# with the default initialisation function and performs some operations

import pandas as pd
import matplotlib.pyplot as plt
import os
from funcs.init_default import init_default

# simulation batch parameters
steps = 200
n_simuls = 1
nf = 100
nm = 2

# output csv file generation params
output_csv_dir = 'outputs'
output_csv_name = 'simul_results'
output_csv = 'mean'     # can be 'all', 'mean' or 'none'
output_costs = 'mean'  # same as above, 'all', 'mean' or 'none'

# data files
densities_file = os.path.join('..', 'data', 'Densidades.csv')
initial_pops_file = os.path.join('..', 'data', 'my_initial_pops.csv')
initial_pops_lines = [0, 1]

u, w, sc, my_plotter = init_default()

# run a couple of simulation batches based on the missing
# values based on an external dataframe
df = sc.simulation_batch(nf, nm, steps, n_simuls,
                         output_csv=output_csv,
                         output_costs=output_costs,
                         output_dir=output_csv_dir,
                         output_name=output_csv_name
                         )


df[['moth-living', 'fly-living', 'fly-predation']].plot()
plt.show()
