# -*- coding: utf-8 -*-
"""
Takes as input a directory with the simulation results and returns the minimal bayes cost
ordered by the number of flies, for each group of simulations with same number of moths.

"""
import pandas as pd
import os


def min_bayes_cost(simul_directory='outputs', costs_file='simul_results_bayes_cost.csv',
                   output_file='outputs_bayes_min'):
    df = pd.read_csv(os.path.join(simul_directory, costs_file), index_col=0)
    min_df = pd.DataFrame(columns=['#flies', 'sample_#moth', 'sample_area', 'bayes_cost'])

    tuples = df[['sample_#moth', 'sample_area']].drop_duplicates()
    for _, t in tuples.iterrows():
        curr_df = df[(df['sample_#moth'] == t['sample_#moth']) & (df['sample_area'] == t['sample_area'])]
        min_df = min_df.append(curr_df[curr_df['bayes_cost'] == curr_df['bayes_cost'].min()])

    min_df.to_csv(os.path.join(simul_directory, output_file))
    return min_df
