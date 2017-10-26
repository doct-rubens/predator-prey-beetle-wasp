# -*- coding: utf-8 -*-
#
# Basic testing script that creates a sample
#     > universe
#     > world
#     > plotter
#     > simulation control
# with the default initialisation function and performs some operations

import matplotlib.pyplot as plt
from funcs.init_default import init_default

# simulation batch parameters
steps = 300
n_simuls = 3
nf = 50
nm = 100

# output csv file generation params
output_csv_dir = 'outputs'
output_csv_name = 'simul_results'
output_csv = 'all'     # can be 'all', 'mean' or 'none'
output_costs = 'all'  # same as above, 'all', 'mean' or 'none'

u, w, sc, my_plotter = init_default()

# run a couple of simulation batches based on the missing
# values based on an external dataframe
df = sc.run_some_batches(nf, nm, steps, n_simuls,
                         output_csv=output_csv,
                         output_costs=output_costs,
                         output_dir=output_csv_dir,
                         output_name=output_csv_name
                         )
df[['moth-living', 'fly-living']].plot()
plt.show()
