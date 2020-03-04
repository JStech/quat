#!/usr/bin/env python
import unittest
from context import quat
from math import pi
Q = quat.Quat

class TestArithmetic(unittest.TestCase):
    def test_from_rot_matrix(self):
        q = Q.from_rot_matrix([
            [  0.6169186, -0.4967616,  0.6104419],
            [  0.1902965,  0.8467674,  0.4967616],
            [ -0.7636744, -0.1902965,  0.6169186]
            ])
        assert(q.nearly_equal(Q(-0.1957247, 0.3914493, 0.1957247, 0.8775826)))
        q = Q.from_rot_matrix([
            [  0.6381832, -0.5852745,  0.5001760],
            [ -0.5001760, -0.8090841, -0.3085563],
            [  0.5852745, -0.0532606, -0.8090841]
            ])
        assert(q.nearly_equal(Q([0.9022682, -0.3007561, 0.3007561, 0.0707372])))
        q = Q.from_rot_matrix([
            [ -0.6652457, -0.6422671, -0.3807114],
            [ -0.6899294,  0.3339017,  0.6422671],
            [ -0.2853868,  0.6899294, -0.6652457]
            ])
        assert(q.nearly_equal(Q(-0.4080742, 0.8161484, 0.4080742, -0.0291995)))
        q = Q.from_rot_matrix([
            [ -0.8555594,  0.2386672, -0.4594083],
            [  0.3322741, -0.4273534, -0.8408109],
            [ -0.3970037, -0.8720132,  0.2863233]
            ])
        assert(q.nearly_equal(Q(0.2671473, 0.5342946, -0.8014418, -0.0291995)))

    def test_to_rot_matrix(self):
        q = Q(-0.42081594255051263, -0.16224240404611412, -0.19536081106265424,
                -0.8708762818710836)
        m = [[ 0.8710238, -0.2038342,  0.4469554],
                [ 0.4768412,  0.5695051, -0.6695420],
                [-0.1180678,  0.7963138,  0.5932490]]
        mm = q.to_rot_matrix()
        assert(all(all(abs(m[i][j] - mm[i][j]) < 1e-3 for i in range(3))
            for j in range(3)))

    def test_from_axis_angle(self):
        q = Q.from_axis_angle([0.3713907, -0.557086, 0.7427814], 1.4)
        assert(q.nearly_equal(Q(0.2392564, -0.3588847, 0.4785129, 0.7648422 )))

    def test_to_axis_angle(self):
        (axis, angle) = Q(0.2392564, -0.3588847, 0.4785129, 0.7648422).to_axis_angle()
        assert abs(angle - 1.4) < 1e-6
        assert all(abs(axis[i] - [0.3713907, -0.557086, 0.7427814][i]) < 1e-6 for i in range(3))

    def test_from_ypr(self):
        q = Q.from_ypr(.2, .3, .4)
        assert(q.nearly_equal(Q(0.1808356, 0.1653388, 0.0672043, 0.9671841)))

    def test_to_ypr(self):
        (yaw, pitch, roll) = Q(0.1808356, 0.1653388, 0.0672043, 0.9671841).to_ypr()
        assert(abs(yaw - 0.2) < 1e-6 and abs(pitch - 0.3) < 1e-6 and abs(roll - 0.4) < 1e-6)

    def test_log(self):
        q = Q(2, 3, 4, 1)
        q.normalize()
        assert q.log().nearly_equal(Q(0.5152, 0.7728, 1.0304, 0), 1e-4)

    def test_exp(self):
        v = [1, 2, 3]
        n = sum(e**2 for e in v)**.5
        theta = pi/3
        v = [theta*e/n for e in v]
        q = Q(v + [0.])
        assert abs(q.exp().norm() - 1) < 1e-6
        assert q.exp().log().nearly_equal(q)
        assert abs(q.exp().w() - 0.5) < 1e-6

if __name__ == '__main__':
    unittest.main()
