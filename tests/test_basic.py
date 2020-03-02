#!/usr/bin/env python
from context import quat
Q = quat.Quat

q1 = Q([1, 2, 3, 4])
q2 = Q(x=.1, y=.2, z=.3, w=.4)

assert(q1 + q2 == Q([1.1, 2.2, 3.3, 4.4]))
assert(q1 + 3 == Q([1, 2, 3, 7]))
assert(3 + q2 == Q([.1, .2, .3, 3.4]))
assert(q1 - q2 == Q([0.9, 1.8, 2.7, 3.6]))
assert((q1*q2).nearly_equal(Q(w=0.2, x=0.8, y=1.6, z=2.4)))
