# -*- coding: utf-8 -*-
#
# Almost the same as the 'test_default' script, but executing
# it for all values of 'n' and 'A', read from the 'AmostragemBrocas.csv'
# file

import pandas as pd
import os
from funcs.init_default import init_default
from simul.control import _BAYES_COST_COLUMNS

# simulation batch parameters
steps = 50
n_simuls = 10

# output csv file generation params
output_csv_dir = 'outputs'
output_csv_name = 'simul_results'
output_csv = 'mean'     # can be 'all', 'mean' or 'none'
output_costs = 'mean'  # same as above, 'all', 'mean' or 'none'

# data files
densities_file = os.path.join('..', 'data', 'Densidades.csv')
initial_pops_file = os.path.join('..', 'data', 'my_initial_pops.csv')
samples_file = os.path.join('..', 'data', 'AmostragemBrocas.csv')

u, w, sc, my_plotter = init_default()

# open the samples data file and initialize an empty dataframe
samples_data = pd.read_csv(samples_file)
final_df = pd.DataFrame(data=[], columns=_BAYES_COST_COLUMNS)

# definition of the list with initial number of flies
# that must be used to calculate the simulations
n_flies_list = [0, 1500]

# iterates over the possible values for sample_n_moths and sample_area
for _, samples_tuple in samples_data.iterrows():
    print(samples_tuple['n'], samples_tuple['A'])
    success, cost = sc.bayes_cost_function(pd.read_csv(densities_file), samples_tuple['n'], samples_tuple['A'],
                                           n_flies_list,
                                           pd.read_csv(os.path.join(output_csv_dir, output_csv_name + '_cost.csv'),
                                                       index_col=[0]))

    if success:
        bayes_cost_file = os.path.join(output_csv_dir, output_csv_name + '_bayes_cost.csv')
        print('bayes cost calculated for n={} and A={}'.format(samples_tuple['n'], samples_tuple['A']))
        final_df = final_df.append(cost)

    else:
        print('no success on calculating the bayes costs;')
        print('the following simulations are missing:')
        print(cost)
        print("saving these missing initial populations on file '{}'".format(initial_pops_file))
        cost.to_csv(initial_pops_file)


# save results on external file
bayes_cost_file = os.path.join(output_csv_dir, output_csv_name + '_bayes_cost.csv')
final_df.to_csv(bayes_cost_file)
