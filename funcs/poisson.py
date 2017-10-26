# -*- coding: utf-8 -*-
#
# Python file that implements the Poisson distribution as a function
#

import numpy as np
from math import factorial


def poisson(n, area, p):
    return (((p * area) ** n) * np.exp(-p * area)) / factorial(n)
