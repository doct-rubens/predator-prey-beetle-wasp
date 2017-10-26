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


def init_default():
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
    fly_params = {'mfr': 0.3, 'lm': 20, 'lv': 3, 'amin': 17, 'amax': 17,
                  'fr': 1.0, 'om': 10, 'ov': 2, 'aa': 10, 'ee': 4, 'rd': 0.05}

    # moth universe laws parameters
    moth_params = {'mfr': 0.5, 'lm': 70, 'lv': 10, 'amin': 0, 'amax': 65,
                   'fr': 1.0, 'om': 0, 'ov': 0, 'aa': 60, 'ee': 15, 'rd': 0.03}

    # other parameters:
    #     pc        - predation coefficient
    other_params = {'pc': 1.0}

    # universe instantiation
    u = Universe(*fly_params.values(), *moth_params.values(), *other_params.values())

    #######################################################
    # ############ WORLD INITIALISATION ###################
    #######################################################
    # fly and moth initial lifespans (world dependent)
    fil = None
    mil = None

    # world instantiation
    w = WonderfulWorld(u, fil=fil, mil=mil)

    #######################################################
    # ############ PLOTTER INITIALISATION #################
    #######################################################
    # number of simulation steps and number of simulations
    n_simuls = 2

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
    costs = {'fly': 20.0, 'moth': 12.0}

    # simul control instantiation
    sc = SimulationControl(w, *costs.values(), plotter=my_plotter)

    return u, w, sc, my_plotter
