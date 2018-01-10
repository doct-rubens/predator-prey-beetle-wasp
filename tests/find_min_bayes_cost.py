# -*- coding: utf-8 -*-
"""
Opens a bayes cost file and saves on another file the dataframe with only the minimal
costs for each tuple ['sample_#nmoths', 'sample_area']
"""
import os
from funcs.min_bayes_cost import min_bayes_cost

parent = 'outputs'
input_bayes_cost = 'simul_results_bayes_cost.csv'
output_bayes_cost = 'simul_results_bayes_cost_min.csv'

output_costs = min_bayes_cost(simul_directory=parent, costs_file=input_bayes_cost,
                              output_file=output_bayes_cost)

output_costs.to_csv(os.path.join(parent, output_bayes_cost))
