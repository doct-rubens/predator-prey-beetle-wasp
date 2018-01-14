# -*- coding: utf-8 -*-
"""
Evaluates the simple cost considering only the 50 first steps of all simulation
files on a given directory
"""
import os
import pandas as pd
from funcs.init_default import init_default

exec_dir = 2
simul_results_dir = 'final-outputs_bayes_{}'.format(exec_dir)
simul_files = [s for s in os.listdir(simul_results_dir) if s[0:5] == 'final']
cost_steps = 200
output_dir = 'simple_costs'
output_file = 'cost_dir{}-{}_steps.csv'.format(exec_dir, cost_steps)

u, w, sc, my_plotter = init_default()
costs_df = sc.simple_cost(simul_results_dir, simul_files, cost_steps=cost_steps)

costs_df.to_csv(os.path.join(output_dir, output_file))
