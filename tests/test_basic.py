#!/usr/bin/env python
import sys

print(sys.path)

import quat

q1 = quat.Quat([1, 2, 3, 4])
q2 = quat.Quat([.1, .2, .3, .4])

print(q1 + q2)
print(q1 + 3)
print(3 + q2)
