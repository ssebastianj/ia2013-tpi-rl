#!/usr/bin/env python
# ! -*- coding: utf-8 -*-

# Author: Juanjo Conti
# http://www.juanjoconti.com.ar/2007/02/28/lista-circular-en-python/


class ListaCircular(list):
    u"""
    Lista circular doblemente enlazada

    Fuente: http://www.juanjoconti.com.ar/2007/02/28/lista-circular-en-python/
    """
    def __init__(self, *a, **kw):
        super(ListaCircular, self).__init__(*a, **kw)
        self.position = 0

    def current(self):
        return self[self.position]

    def next(self, n=1):
        self.position = (self.position + n) % len(self)
        return self[self.position]

    def prev(self, n=1):
        return self.next(-n)


if __name__ == '__main__':
    import unittest

    class Prueba(unittest.TestCase):
        def setUp(self):
            self.l = ListaCircular([1, 2, 3, 15, "www", 'u'])

        def testArrancaDeCero(self):
            self.assertEqual(self.l.current(), 1)

        def testTomaElPasoComoParametroOpcional(self):
            self.assertEqual(self.l.next(4), "www")
            self.assertEqual(self.l.next(), 'u')

        def testTomaPasoNegativo(self):
            self.assertEqual(self.l.next(-2), "www")

        def testTomaPasoQueDaUnParDeVueltas(self):
            self.assertEqual(self.l.next(8), 3)

        def testSePortaIgualParaAtrasYParaAdelante(self):
            self.assertEqual(self.l.prev(), 'u')
            self.assertEqual(self.l.prev(-6), 'u')

        def testNoItems(self):
            self.assertRaises(Exception, ListaCircular([]).next)

        def testInstanciarSinParametros(self):
            self.assertEquals(ListaCircular(), ListaCircular([]))

    unittest.main()
