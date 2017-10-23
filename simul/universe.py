# -*- coding: utf8 -*-
#
# Holds the set of constants used on the biological laws that our system
# obeys, amongst which:
#    > distributions between male and female gender of each creature
#    > lifespan of each creature
#    > initial lifespan distribution for each creature
#    > fertility ratio for each creature
#    > offspring mean and variance (normal distributions predefined for
#      these distributions)

from simul.creatures import Moth
from simul.creatures import Fly
from itertools import product


class Universe:
    def __init__(self,
                 fmfr, flm, flv, famin, famax, ffr, fom, fov, faa, fea, frd,  # fly parameters
                 mmfr, mlm, mlv, mamin, mamax, mfr, mom, mov, maa, mea, mrd,  # moth parameters
                 predation_coefficient):                                      # other parameters

        self.mf_ratio = {Fly: fmfr, Moth: mmfr}
        self.lifespan_mean = {Fly: flm, Moth: mlm}
        self.lifespan_var = {Fly: flv, Moth: mlv}
        self.initial_age_min = {Fly: famin, Moth: mamin}
        self.initial_age_max = {Fly: famax, Moth: mamax}
        self.fertility_ratio = {Fly: ffr, Moth: mfr}
        self.offspring_mean = {Fly: fom, Moth: mom}
        self.offspring_var = {Fly: fov, Moth: mov}
        self.adult_age = {Fly: faa, Moth: maa}
        self.egg_age = {Fly: fea, Moth: mea}
        self.random_death_chance = {Fly: frd, Moth: mrd}

        self.predation_coefficient = predation_coefficient

        # defines the set of data that we will want to visualize after the simulation.
        # For each type of creature and each iteration
        self.recordable_data = ['living',
                                'dead',
                                'male',
                                'female',
                                'randomly_killed',
                                'old_age_killed',
                                'parents',
                                'adults',
                                'newborn',
                                'predation',
                                'caterpillars'
                                ]
        self.c_types = ['moth-', 'fly-']
        self.df_columns = [(c + d) for c, d in product(self.c_types, self.recordable_data)]
