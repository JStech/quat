#!/usr/bin/env python
import unittest
from context import quat
Q = quat.Quat

class TestOperators(unittest.TestCase):
    def setUp(self):
        self.q0 = Q()
        self.q1 = Q([1, 2, 3, 4])
        self.q2 = Q(x=.1, y=.2, z=.3, w=.4)
        self.q3 = Q(1.1, 2.2, 3.3, 4.4)

    def test_init(self):
        assert self.q0.q == [0, 0, 0, 1]
        assert self.q1.q == [1, 2, 3, 4]
        assert self.q2.q == [.1, .2, .3, .4]
        assert self.q3.q == [1.1, 2.2, 3.3, 4.4]
        assert (self.q1.w() == 4 and self.q1.x() == 1 and
                self.q1.y() == 2 and self.q1.z() == 3)

    def test_add(self):
        assert(self.q1 + self.q2 == Q([1.1, 2.2, 3.3, 4.4]))
        assert(self.q1 + 3 == Q([1, 2, 3, 7]))
        assert(3 + self.q2 == Q([.1, .2, .3, 3.4]))

    def test_sub(self):
        assert(self.q1 - self.q2 == Q([0.9, 1.8, 2.7, 3.6]))
        assert(3 - self.q1 == -Q([1, 2, 3, 1]))

    def test_mult(self):
        assert((self.q1*self.q2).nearly_equal(Q(w=0.2, x=0.8, y=1.6, z=2.4)))

    def test_conj(self):
        assert(self.q1.conj() == Q(x=-1, y=-2, z=-3, w=4))

    def test_norm(self):
        assert(abs(self.q1.norm() - 30.0**.5) < 1e-9)

    def test_normalize(self):
        self.q1.normalize()
        assert(abs(self.q1.q[i] - (i+1)/30.0**.5 < 1e-9) for i in range(4))

if __name__ == '__main__':
    unittest.main()
