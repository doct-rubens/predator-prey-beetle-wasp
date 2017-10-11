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
np.random.seed(42)

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
fly_params = {'mfr': 1.0, 'lm': 20, 'lv': 3, 'amin': 14, 'amax': 17,
              'fr': 0.5, 'om': 10, 'ov': 5, 'aa': 10, 'ee': 4, 'rd': 0.0}

# moth universe laws parameters
moth_params = {'mfr': 0.5, 'lm': 20, 'lv': 3, 'amin': 0, 'amax': 0,
               'fr': 0.5, 'om': 6, 'ov': 2, 'aa': 10, 'ee': 5, 'rd': 0.0}

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
n_simuls = 5

# image generation params
title = 'test simulation'
parent_path = 'output_images'
path = 'test_simulation'
columns = ['moth-living', 'fly-living']

# create the classes
my_plotter = Plotter(title, path, columns, n_simuls, parent_path=parent_path)
u = Universe(*fly_params.values(), *moth_params.values(), *other_params.values())
w = WonderfulWorld(nm, nf, u)
s = SimulationControl(w, *costs.values(), plotter=my_plotter)

# run a simulation batch
df = s.simulation_batch(steps, n_simuls)
