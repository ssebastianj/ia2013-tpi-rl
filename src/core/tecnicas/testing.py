#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import numba
import sys
import timeit

sys.path.append(os.path.abspath(os.path.join(os.pardir, '..', 'src')))

from core.tecnicas.egreedy import EGreedy, Greedy
from core.tecnicas.softmax import Softmax


def main():
    vecinos = [(0, 0), (1, 1), (2, 2), (3, 3)]

    eg = EGreedy(0.5, 0.01, 2)
    obtener_accion = numba.autojit()(eg.obtener_accion)
    obtener_accion(eg.obtener_accion, vecinos)

if __name__ == '__main__':
    print timeit.timeit(main, number=10000)
    print timeit.timeit(main, number=10000)
    print timeit.timeit(main, number=10000)
