# -*- coding: utf-8 -*-
#
# Simulation control class implementation. Receives a world, the constant
# costs for flies and caterpillars.
#
# The cost is calculated as
#   $$ C = n_{flies} C_{fly} + C_{caterpillar} \int_{0}^{T} n_caterpillars(t) dt $$
#
# Also receives a plotter object used to create the sequence of incremental average
# populations for each time step - the plotter can generate a sequence of output images
# or a video with that evolution.

import os
import numpy as np
import pandas as pd
import scipy.integrate as integrate

_COST_COLUMNS = ['#flies', '#moths', '#steps', '#simuls', 'cost']
_BAYES_COST_COLUMNS = ['#flies', 'sample_#moth', 'sample_area', 'bayes_cost']


class SimulationControl:

    # receives a world to be simulated and the costs
    #
    # the density_factor attribute indicates the relation between the moth density
    # and probabilities file and the actual number of moths
    # dim[density factor] : hectare (area)
    # density_factor * density : hectare * (n_moths / hectare) = n_moths
    def __init__(self, world, cost_fly, cost_moth, plotter=None, density_factor=10000):
        self.world = world
        self.cost_fly = cost_fly
        self.cost_moth = cost_moth
        self.plotter = plotter
        self.density_factor = density_factor

    #
    # cost function computation, given the output of the
    # 'world.run_world(total_time)' method (a dataframe
    # with all the data)
    def cost(self, data_log):
        moth_function = np.array(data_log[['moth-caterpillars']].values.reshape(len(data_log)), dtype=int)
        return ((self.world.n_flies * self.cost_fly) +
                (self.cost_moth * integrate.simps(moth_function)))

    #
    # executes a batch of simulations given we already have
    # a functioning world.
    #
    # Receives the number of times steps 'simul_time' and
    # the number of simulations 'n_simuls',
    #
    # Returns an averaged log between the logs of all
    # simulations (cost not included)
    #
    # Checks the output_csv parameter to save the simulation data
    # under the directory
    #       output_dir / output_name_{simul_idx}.csv
    #
    # Checks the output_costs parameter to open/create a new costs csv
    # file and save the costs data on it, under the directory
    #       output_dir / output_costs_name_{simul_idx}.csv
    def simulation_batch(self, n_flies, n_moths, simul_time, n_simuls,
                         output_csv='none', output_costs='none',
                         output_dir='outputs', output_name='simul'):

        output_costs_name = output_name + '_cost'

        # creates a directory with the given name if it doesn't already exists
        if (output_csv != 'none') or (output_costs != 'none'):
            if not os.path.exists(output_dir):
                os.mkdir(output_dir)

        # initializes the cost dataframe
        if output_costs != 'none':

            # if there is a costs file saved under the same name, open and use it
            # (append the new results on it)
            if os.path.exists(os.path.join(output_dir, output_costs_name + '.csv')):
                costs_df = pd.read_csv(os.path.join(output_dir, output_costs_name + '.csv'),
                                       index_col=[0])
                costs_idx_offset = len(costs_df)
            else:
                costs_df = pd.DataFrame(columns=_COST_COLUMNS)
                costs_idx_offset = 0

        costs_data = dict.fromkeys(_COST_COLUMNS, [])
        if output_costs == 'all':
            for col in costs_data:
                costs_data[col] = np.zeros(n_simuls + 1)

        if output_costs == 'mean':
            for col in costs_data:
                costs_data[col] = [0]

        snp = max([1, int(np.ceil(np.log10(n_simuls + 1)))])
        avg_simul_log = self.empty_data_log(simul_time + 1)
        for i in range(n_simuls):

            # current simulation dataframe results
            curr_df = self.world.run_world(n_flies, n_moths, simul_time)

            # if output saving mode is set to 'all', save these results
            if output_csv == 'all':
                curr_df.to_csv(os.path.join(output_dir,
                                            output_name + ('_{0:0{1}}.csv'.format(i, snp))))

            if output_costs == 'all':
                costs_data['#moths'][i] = self.world.n_moths
                costs_data['#flies'][i] = self.world.n_flies
                costs_data['#steps'][i] = simul_time
                costs_data['#simuls'][i] = 1
                costs_data['cost'][i] = self.cost(curr_df)

            avg_simul_log = avg_simul_log + curr_df

            if self.plotter is not None:
                self.plotter.save_image(avg_simul_log / (i + 1), idx=i)

        avg_simul_log = avg_simul_log / n_simuls

        if output_csv != 'none':
            avg_simul_log.to_csv(os.path.join(output_dir, output_name + '_mean.csv'))

        if output_costs != 'none':
            costs_data['#moths'][-1] = self.world.n_moths
            costs_data['#flies'][-1] = self.world.n_flies
            costs_data['#steps'][-1] = simul_time
            costs_data['#simuls'][-1] = n_simuls
            costs_data['cost'][-1] = self.cost(avg_simul_log)
            costs_df = costs_df.append(pd.DataFrame(data=costs_data,
                                                    index=range(costs_idx_offset,
                                                                costs_idx_offset + len(costs_data['#moths'])),
                                                    columns=_COST_COLUMNS))
            costs_df.to_csv(os.path.join(output_dir, output_costs_name + '.csv'))

        return avg_simul_log

    #
    # Initializes an empty dataframe with the length of the simulation time
    # and with a number of columns equal to the number of saved parameters
    # (defined on the universe, referenced by the world object)
    def empty_data_log(self, elems):
        return pd.DataFrame(data=np.zeros([elems, len(self.world.universe.df_columns)],
                                          dtype=int),
                            index=range(elems),
                            columns=self.world.universe.df_columns)

    # runs simulation batches with the initial #moths and #flies defined on a
    # dataframe passed as argument
    def run_some_batches(self, initial_populations, simul_time, n_simuls,
                         output_csv='none', output_costs='none',
                         output_dir='outputs', output_name='simul'
                         ):

        for _, initial_pop in initial_populations.iterrows():
            print('running batch for #flies={}, #moths={}'.format(initial_pop['#flies'], initial_pop['#moths']))
            self.simulation_batch(initial_pop['#flies'], initial_pop['#moths'], simul_time,  n_simuls,
                                  output_csv=output_csv, output_costs=output_costs,
                                  output_dir=output_dir, output_name=output_name)
