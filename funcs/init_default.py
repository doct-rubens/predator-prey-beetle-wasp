# -*- coding: utf-8 -*-
#
# Function that initializes a default:
#     > universe
#     > world
#     > simulationControl
#     > plotter
# with optionally definable parameters

from simul.universe import Universe
from simul.world import WonderfulWorld
from simul.control import SimulationControl
from media.plotter import Plotter
import numpy as np


def init_default():
    # set the pseudo-random number generator with a fixed seed
    np.random.seed(42)

    #######################################################
    # ########### UNIVERSE INITIALISATION #################
    #######################################################
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
    fly_params = {'mfr': 0.3, 'lm': 24, 'lv': 4, 'amin': 22, 'amax': 22,
                  'fr': 1.0, 'om': 28, 'ov': 19, 'aa': 15, 'ee': 9, 'rd': 0.05}

    # moth universe laws parameters
    moth_params = {'mfr': 0.5, 'lm': 70, 'lv': 2, 'amin': 0, 'amax': 65,
                   'fr': 1.0, 'om': 60, 'ov': 20, 'aa': 63, 'ee': 10, 'rd': 0.04}

    # other parameters:
    #     pc        - predation coefficient
    other_params = {'pc': 4.0}

    # universe instantiation
    u = Universe(*fly_params.values(), *moth_params.values(), *other_params.values())

    #######################################################
    # ############ WORLD INITIALISATION ###################
    #######################################################
    # fly and moth initial lifespans (world dependent)
    fil = 1
    mil = None

    # world instantiation
    w = WonderfulWorld(u, fil=fil, mil=mil)

    #######################################################
    # ############ PLOTTER INITIALISATION #################
    #######################################################
    # number of simulation steps and number of simulations
    n_simuls = 1

    # image generation params
    title = 'test simulation'
    parent_path = 'output_images'
    path = 'test_simulation'
    columns = ['moth-living', 'fly-living']

    # plotter instantiation
    my_plotter = Plotter(title, path, columns, n_simuls, parent_path=parent_path)

    #######################################################
    # ############ CONTROL INITIALISATION #################
    #######################################################
    # default costs:
    costs = {'fly': 0.0027, 'moth': 0.005}

    # simul control instantiation
    sc = SimulationControl(w, *costs.values(), plotter=my_plotter)

    return u, w, sc, my_plotter
