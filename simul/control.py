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

import numpy as np
import pandas as pd
import scipy.integrate as integrate


class SimulationControl:

    # receives a world to be simulated and the costs
    def __init__(self, world, cost_fly, cost_moth, plotter=None):
        self.world = world
        self.cost_fly = cost_fly
        self.cost_moth = cost_moth
        self.plotter = plotter

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
    # If a plotter was sent to the simulation control, generates
    # output images and/or a video according to the plotter settings
    def simulation_batch(self, simul_time, n_simuls):
        avg_simul_log = self.empty_data_log(simul_time + 1)
        for i in range(n_simuls):
            avg_simul_log = avg_simul_log + self.world.run_world(simul_time)

            if self.plotter is not None:
                self.plotter.save_image(avg_simul_log / (i + 1), idx=i)

        return avg_simul_log / n_simuls

    #
    # Initializes an empty dataframe with the length of the simulation time
    # and with a number of columns equal to the number of saved parameters
    # (defined on the universe, referenced by the world object)
    def empty_data_log(self, elems):
        return pd.DataFrame(data=np.zeros([elems, len(self.world.universe.df_columns)],
                                          dtype=int),
                            index=range(elems),
                            columns=self.world.universe.df_columns)
