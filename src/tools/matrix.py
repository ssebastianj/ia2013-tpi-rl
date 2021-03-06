#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Autor: http://mybravenewworld.wordpress.com/2010/09/19/print-tabular-data-nicely-using-python/


def matrix_to_string(matrix, header=None):
    """
    Returns a pretty and aligned string representation of a NxM matrix.

    This representation can be used to print any tabular data, such as
    database results. It works by scanning the lengths of each element
    in each column and determining the format string dynamically.

    :param matrix: Matrix representation (list with N rows and M elements).
    :param header: Optional tuple or list with header elements to be displayed.
    """
    if type(header) is list:
        header = tuple(header)
    lengths = []
    if header:
        for column in header:
            lengths.append(len(column))
    for row in matrix:
        for column in row:
            i = row.index(column)
            column = str(column)
            cl = len(column)
            try:
                ml = lengths[i]
                if cl > ml:
                    lengths[i] = cl
            except IndexError:
                lengths.append(cl)

    lengths = tuple(lengths)
    format_string = ""
    for length in lengths:
        format_string += "%-" + str(length) + "s "
    format_string += "\n"

    matrix_str = ""
    if header:
        matrix_str += format_string % header
    for row in matrix:
        matrix_str += format_string % tuple(row)

    return matrix_str
