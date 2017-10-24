# -*- coding: utf-8 -*-
#
# World class file. A world is composed of:
#    - an initial number of flies and moths
#    - a set of laws that control the relation between its creatures
#    - how its creatures interact with each other for each time step (day)
#    - a support structure that allows the data of each time step to be saved
#      and later visualised
#
# Its main objective is to be able to:
#    - simulate the interaction of its creatures for a given number of steps
#    - be able to perform multiple simulations (not only once)

import numpy as np
import pandas as pd

from simul.creatures import Creature
from simul.creatures import Moth
from simul.creatures import Fly


class WonderfulWorld:

    def __init__(self, n_moths, n_flies, universe, fil=None, mil=None):

        self.universe = universe
        self.instant = 0

        self.n_moths = n_moths
        self.n_flies = n_flies

        # indexes the universe applied to the world to be the one
        # globally applied to all creatures
        Creature.universe = universe

        # initializes the simulation variables
        self.creatures = {Moth: [], Fly: []}
        self.children = {Moth: [], Fly: []}

        # initializes the data-saving variables
        self.data_log = pd.DataFrame(data=None, index=None, columns=self.universe.df_columns)
        self.iteration_data = {Moth: [], Fly: []}
        self.initial_lifespan = {Fly: fil, Moth: mil}

    #
    # initializes the world with:
    #     - uniform distributions for the initial ages of moths and flies
    #       with limits defined by the universe
    #     - resets the current instant
    #     -
    def initialize_world(self):
        self.instant = 0

        # reset the list of caterpillars, if it wasn't already empty
        del Moth.caterpillars[:]

        # initializes:
        #    - ages based on a uniform distribution (for the moths)
        #       ''           2 living days before their death (implemented
        #                    internally, for the flies)
        #    - genders following the universe's male/female ratios
        self.creatures = {
            Moth: [Moth(0, age=np.random.randint(low=self.universe.initial_age_min[Moth],
                                                 high=self.universe.initial_age_max[Moth] + 1),
                        initial_lifespan=self.initial_lifespan[Moth])
                   for _ in range(self.n_moths)],
            Fly: [Fly(0, age=np.random.randint(low=self.universe.initial_age_min[Fly],
                                               high=self.universe.initial_age_max[Fly] + 1),
                      initial_lifespan=self.initial_lifespan[Fly])
                  for _ in range(self.n_flies)]
        }

        # resets the newborn creatures arrays
        self.children = {Moth: [], Fly: []}

        # initializes the output log with the first
        # values for the creatures' features
        self.reset_iteration_log()
        self.initialize_log()
        self.save_iteration_log()

    #
    # kills the current creature. Previously, it automatically removed the
    # killed creature from the creatures list. But, that messed up the creature
    # processing, so we removed it and we clean up the fields only after the day ended
    # (we clean up the creatures lists only after we finished processing all creatures)
    @staticmethod
    def kill(creature):
        creature.kill()

    #
    # same thing that occurred with the creature killing method. We add the newborn
    # creatures only after we process all creatures from the current iteration.
    # Until then, the children is saved on a holding structure, the 'children' lists
    def procreate(self, creature):
        children = creature.children(gen=(self.instant + 1))
        self.children[type(creature)] += children
        # self.creatures[type(creature)] += children

        # we update our iteration data (that we want to visualise when the simulation
        # ends) with these new numbers
        self.iteration_data[type(creature)]['parents'] += 1
        self.iteration_data[type(creature)]['newborn'] += len(children)

    #
    # Checks if a creature should randomly die. If yes, kills it and
    # updates the iteration data. Returns a boolean variable indicating
    # whether the creature actually died or not
    def random_death(self, creature):
        if creature.random_death():
            self.iteration_data[type(creature)]['randomly_killed'] += 1
            self.kill(creature)
            return True
        else:
            return False

    #
    # Checks if a creature should die of old age. If yes, kills it and
    # updates the iteration data. Returns a boolean variable indicating
    # whether the creature actually died or not
    def old_age_death(self, creature):
        if creature.old_age_death():
            self.iteration_data[type(creature)]['old_age_killed'] += 1
            self.kill(creature)
            return True
        else:
            return False

    #
    # calculates the chances of a predation happening. It takes into
    # account the ratio (#caterpillars / #flies) multiplied by a
    # predefined (on the universe) coefficient
    def predation_happens(self):
        if self.creatures[Fly]:
            return np.random.uniform() < (self.universe.predation_coefficient *
                                          len(Moth.caterpillars) / len(self.creatures[Fly]))
        else:
            return False

    #
    # predation method. All of the verifications have been already
    # made and a predation is imminent on our system. We updated
    # the output data, sort out one of the caterpillars (there will
    # always be at least one, since the number of caterpillars goes into
    # the predation verification) and we kill it.
    #
    # Afterwards, we procreate the fly that just performed the predation.
    def predation(self, fly):
        self.iteration_data[Fly]['predation'] += 1
        self.iteration_data[Moth]['dead'] += 1

        # get the lucky bastard (caterpillars) by its horns
        lucky_caterpillar = Moth.caterpillars[np.random.randint(low=0,
                                                                high=len(Moth.caterpillars))]

        # kill 'em
        self.kill(lucky_caterpillar)

        # new baby flies are born
        self.procreate(fly)

    # Checks what happened on the transition between the previous instant
    # (yesterday) and the current instant (today).
    def single_step(self):

        # we reset the iteration log and update the current instant
        self.reset_iteration_log()
        self.instant = self.instant + 1

        # fly stuff:
        #    > random death
        #    > death by old age
        #        - with its last breath, it parasited a moth
        #          (or not, we roll the dice to check)
        #    > nothing happens bean stew (increment age)
        for fly in self.creatures[Fly]:
            if not self.random_death(fly):
                if self.old_age_death(fly):
                    if fly.can_procreate():
                        if self.predation_happens():
                            self.predation(fly)
                else:
                    fly.increment_age()
            self.log_creature(fly)

        # update the flies and remove the moth corpses from the field before
        # checking on them
        self.update_list(Fly)
        self.update_list(Moth)

        # moth stuff:
        #    > see if it died randomly
        #    > see if died of old age
        #        - if it was female and fertile, procreates on death
        #    > nothing happens bean stew (increment age)
        for moth in self.creatures[Moth]:
            if not self.random_death(moth):
                if self.old_age_death(moth):
                    if moth.can_procreate():
                        self.procreate(moth)
                else:
                    moth.increment_age()
            self.log_creature(moth)
        self.update_list(Moth)

        self.save_iteration_log()

    # removes the dead and insert the newborn creatures on the lists
    def update_list(self, creature_type):
        self.creatures[creature_type][:] = [creature for creature in self.creatures[creature_type] if
                                            creature.is_alive()] + self.children[creature_type]
        self.children[creature_type] = []

    # save the useful data on a dataframe for each generation
    def log_creature(self, creature):
        self.iteration_data[type(creature)]['living'] += creature.is_alive()
        self.iteration_data[type(creature)]['dead'] += creature.is_dead()
        self.iteration_data[type(creature)]['male'] += creature.gender == 'm'
        self.iteration_data[type(creature)]['female'] += creature.gender == 'f'
        self.iteration_data[type(creature)]['caterpillars'] += creature.is_caterpillar()
        self.iteration_data[type(creature)]['adults'] += creature.is_adult()

    # resets the iteration log
    def reset_iteration_log(self):
        self.iteration_data = {
            Moth: dict.fromkeys(self.universe.recordable_data, 0),
            Fly: dict.fromkeys(self.universe.recordable_data, 0)
        }

    # saves the current iteration's log on the dataframe
    def save_iteration_log(self):
        self.data_log = self.data_log.append(pd.DataFrame(data=[list(self.iteration_data[Moth].values()) +
                                                                list(self.iteration_data[Fly].values())],
                                                          index=[len(self.data_log)],
                                                          columns=self.universe.df_columns))

    #
    # initializes the dataframe by creating it empty, logging in all the creatures
    # and saving on it as its first element
    def initialize_log(self):
        self.data_log = pd.DataFrame(data=None, index=None, columns=self.universe.df_columns)

        for moth in self.creatures[Moth]:
            self.log_creature(moth)
        for fly in self.creatures[Fly]:
            self.log_creature(fly)

    #
    # runs the world with a given number of steps 'end_of_times'
    # by repeatedly executing the 'single_step()' method.
    #
    # Returns the dataframe with the outputs generated from the
    # simulation.
    def run_world(self, end_of_times):

        self.initialize_world()
        for _ in range(end_of_times):
            self.single_step()

        return self.data_log
