#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os
import sys
import timeit

sys.path.append(os.path.abspath(os.path.join('..', '..')))

from core.tecnicas.softmax import Softmax

def test():
    s = Softmax(10, 0, 0)
    vecinos = {(1,1): 1, (2,2): 2, (3,3): 3, (4,4): 4}
    s.obtener_accion(vecinos)


if __name__ == '__main__':
    print timeit.timeit(test, number=1000)
    print timeit.timeit(test, number=1000)
    print timeit.timeit(test, number=1000)
