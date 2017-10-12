# -*- coding: utf-8 -*-
#
# Basic testing script that creates a sample universe and world
# with a predefined set of parameters and executes a simulation batch

import numpy as np
import matplotlib.pyplot as plt
from simul.universe import Universe
from simul.world import WonderfulWorld
from simul.control import SimulationControl
from media.plotter import Plotter

# reset the random generator seed (obtain same results for
# debugging purposes)
np.random.seed(50)

# beetle universe laws:
#     mfr        - male/female ratio - male probability
#     lm, lv     - lifespan (mean and var, normal distribution)
#     amin, amax - initial population age (age, min and max)
#     fr         - fertility ratio
#     om, ov     - offspring mean and variance (normal distribution)
#     aa         - adult age (aa, equal or higher is adult)
#     ee         - egg age (ea, less or equal is egg)
#     rd         - random death (chance)
# fly universe laws parameters
fly_params = {'mfr': 0.3, 'lm': 20, 'lv': 3, 'amin': 17, 'amax': 17,
              'fr': 1.0, 'om': 0, 'ov': 0, 'aa': 10, 'ee': 4, 'rd': 0.05}

# moth universe laws parameters
moth_params = {'mfr': 0.5, 'lm': 70, 'lv': 10, 'amin': 0, 'amax': 65,
               'fr': 1.0, 'om': 0, 'ov': 0, 'aa': 60, 'ee': 15, 'rd': 0.03}

# other parameters:
#     pc        - predation coefficient
other_params = {'pc': 1.0}

# default costs:
costs = {'fly': 20.0, 'moth': 12.0}

# initial number of flies and moths
nf = 100
nm = 100

# number of simulation steps and number of simulations
steps = 100
n_simuls = 2

# image generation params
title = 'test simulation'
parent_path = 'output_images'
path = 'test_simulation'
#'living','dead','male','female','randomly_killed','old_age_killed','parents','newborn','predation','caterpillars'
columns = ['moth-living', 'fly-living', 'fly-newborn', 'moth-female','moth-male']

# output csv file generation params
output_csv_dir = 'outputs'
output_csv_name = 'simul_results'
output_csv = 'none'     # can be 'all', 'mean' or 'none'
output_costs = 'all'  # same as above, 'all', 'mean' or 'none'

# create the classes
my_plotter = Plotter(title, path, columns, n_simuls, parent_path=parent_path)
u = Universe(*fly_params.values(), *moth_params.values(), *other_params.values())
w = WonderfulWorld(nm, nf, u)
s = SimulationControl(w, *costs.values(), plotter=my_plotter)

# run a simulation batch
df = s.simulation_batch(steps, n_simuls,
                        output_csv=output_csv,
                        output_costs=output_costs,
                        output_dir=output_csv_dir,
                        output_name=output_csv_name
                        )
df[['moth-living', 'fly-living','fly-predation', 'fly-newborn', 'moth-newborn']].plot()
plt.show()