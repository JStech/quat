#!/usr/bin/env python
import unittest
from context import quat
Q = quat.Quat

class TestBasic(unittest.TestCase):

    def test_init(self):
        q0 = Q()
        assert q0.q == [0, 0, 0, 1]
        q1 = Q([1, 2, 3, 4])
        assert q1.q == [1, 2, 3, 4]
        q2 = Q(x=.1, y=.2, z=.3, w=.4)
        assert q2.q == [.1, .2, .3, .4]
        q3 = Q(1.1, 2.2, 3.3, 4.4)
        assert q3.q == [1.1, 2.2, 3.3, 4.4]

    def test_add(self):
        q1 = Q([1, 2, 3, 4])
        q2 = Q(x=.1, y=.2, z=.3, w=.4)
        assert(q1 + q2 == Q([1.1, 2.2, 3.3, 4.4]))
        assert(q1 + 3 == Q([1, 2, 3, 7]))
        assert(3 + q2 == Q([.1, .2, .3, 3.4]))

    def test_sub(self):
        q1 = Q([1, 2, 3, 4])
        q2 = Q(x=.1, y=.2, z=.3, w=.4)
        assert(q1 - q2 == Q([0.9, 1.8, 2.7, 3.6]))
        assert(3 - q1 == -Q([1, 2, 3, 1]))

    def test_mult(self):
        q1 = Q([1, 2, 3, 4])
        q2 = Q(x=.1, y=.2, z=.3, w=.4)
        assert((q1*q2).nearly_equal(Q(w=0.2, x=0.8, y=1.6, z=2.4)))

if __name__ == '__main__':
    unittest.main()
