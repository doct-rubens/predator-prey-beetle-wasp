# -*- coding: utf8 -*-
#
# Defines the creatures class. It implements the storage and
# access to the basic features of our creatures. They are:
#    > gender (init=distribution)
#    > alive (init=true)
#    > age (init=distribution or 0)
#    > offspring (init=0)
#    > fertility (init=distribution)
#
# Two subclasses inherit from the main 'Creature' class, 'Moth'
# and 'Fly'. Only those subclasses are used on the world, never
# a generalized creature (instance of the 'Creature' class).

import numpy as np


class Creature:

    # defines a static universe, common to all creatures. It is initialized
    # at the same time the world is initialized.
    universe = None

    # a new creature is created.
    # we set the:
    #    - gender (with a uniform distribution specified by the universe)
    #    - fertility (same as above)
    #    - lifespan (yes, we say how much the creature will live when its
    #      born. Determinism rulez)
    #    - age (coming in as an argument, will be zero most of the time
    #      (for the newborn creatures) except the world initialization,
    #      where the ages might be different).
    #    - alive (control variable to know if a creature is alive or not)
    def __init__(self, gen, age=0, initial_lifespan=None):
        self.gender = 'm' if (np.random.uniform() < self.universe.mf_ratio[type(self)]) else 'f'
        self.fertility = True if (np.random.uniform() < self.universe.fertility_ratio[type(self)]) else False
        self.lifespan = max([1, int(np.round(np.random.normal(loc=self.universe.lifespan_mean[type(self)],
                                                              scale=self.universe.lifespan_var[type(self)])))])
        if initial_lifespan is None:
            self.age = age
        else:
            self.age = self.lifespan - initial_lifespan
        self.alive = True
        self.generation = gen
        self.offspring = 0

    # uses the age of consent defined at the universe to decide
    # if the creature is an adult.
    #
    # Returns a boolean value:
    #    - True, if it is an adult
    #    - False, if its not
    def is_adult(self):
        return (self.age >= self.universe.adult_age[type(self)]) and (self.is_alive())

    #
    # Returns a boolean value:
    #    - True, if it is an egg
    #    - False, if its not
    # In particular, for the flies, egg_period ~ larvae_period
    def is_egg(self):
        return self.age <= self.universe.egg_age[type(self)]

    # Checks gender-related information and returns a boolean value
    # that indicates whether the creature can procreate or not:
    #    - True, if it can procreate
    #    - False, if not
    def can_procreate(self):
        return (self.gender == 'f') and self.fertility

    # Returns a list of children with the same type as its parent (either
    # Fly or Moth, one of the subclasses).
    def children(self, gen):
        ncs = max([0, int(np.round(np.random.normal(loc=self.universe.offspring_mean[type(self)],
                                                    scale=self.universe.offspring_var[type(self)])))])
        return [type(self)(gen=gen, age=0) for _ in range(ncs)]

    # increments the current age
    def increment_age(self):
        self.age = self.age + 1

    # kills the creature
    def kill(self):
        self.alive = False

    # checks if the creature is alive or not. Returns a boolean value
    def is_alive(self):
        return self.alive is True

    # checks if the creature is dead or not. Returns a boolean value.
    def is_dead(self):
        return self.alive is False

    # implements the static version of the Moth 'is_caterpillar()' method, so
    # it can be called also for flies.
    def is_caterpillar(self):
        return False

    # checks if the creature died randomly. If it did,
    # updates its 'alive' attribute.
    #
    # returns if a random death occurred (True) or not (False)
    def random_death(self):
        if np.random.uniform(low=0.0, high=1.0) < self.universe.random_death_chance[type(self)]:
            self.alive = False
            return True
        else:
            return False

    # checks if an old death occurred. If it occurred, updates
    # the 'alive' attribute of the creature.
    #
    # returns if an old age death actually occurred (True) or
    # not (False)
    def old_age_death(self):
        if self.age > self.lifespan:
            self.alive = False
            return True
        else:
            return False


# Implements the class definition for flies. Doesn't have any 'particularities',
# per se, but the typification acquired from the usage of different subclasses is
# extremely useful
class Fly(Creature):
    pass


# Implements the class definition for moths. Has the particularity of the
# caterpillar verifications and references
class Moth(Creature):

    # initializes a static list of caterpillars, that will hold references
    # to the Moth objects that are actual caterpillars
    caterpillars = []

    def __init__(self, gen, age=0, initial_lifespan=None):
        super().__init__(gen, age=age, initial_lifespan=initial_lifespan)

        # after the same creation used on the super class, we also verify if
        # the Moth that was just created is a caterpillar and if it is, we
        # add its reference to the static caterpillars list
        if self.is_caterpillar():
            self.caterpillars.append(self)

    # Checks if the current creature is a caterpillar. Returns a boolean value,
    #    - True, if it is a caterpillar
    #    - False, if not
    def is_caterpillar(self):
        return ((self.universe.egg_age[type(self)] < self.age) and
                (self.age < self.universe.adult_age[type(self)]))

    # Increments the age of the current moth. Additionally, verifies if its
    # "caterpillar status" changed. If it did, we either insert or remove
    # it from the static caterpillars reference list
    def increment_age(self):
        was_caterpillar = self.is_caterpillar()
        self.age = self.age + 1
        now_is_caterpillar = self.is_caterpillar()

        # was, but now its too old and it isn't anymore
        if was_caterpillar and not now_is_caterpillar:
            self.caterpillars.remove(self)

        # wasn't, but got older and achieve legal caterpillar age
        if not was_caterpillar and now_is_caterpillar:
            self.caterpillars.append(self)

            # if it was and still is, do nothing
            # if it wasn't and still isn't, also do nothing

    # Kills the current moth. Since specially caterpillars are known to be
    # killed in the wild by vicious flies, we also verify if the killed creature
    # was a caterpillar and, if it was, we also remove it from the static
    # caterpillars reference list
    def kill(self):
        self.alive = False
        if self.is_caterpillar():
            self.caterpillars.remove(self)
