# -*- coding: utf-8 -*-
#
# Python file that implements the Poisson distribution as a function
#

import numpy as np
from math import factorial


def poisson(n, area, p):
    if n <= 150:
        return (((p * area) ** n) * np.exp(-p * area)) / factorial(n)
    else:
        return (((p*area/n)**n)*np.exp(-p*area+n))/(np.sqrt(2*np.pi*n))
