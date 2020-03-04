import math

class Quat:
    def __init__(self, *args, **kwargs):
        if len(args) == 0:
            if all(k in kwargs.keys() for k in "wxyz"):
                self.q = [kwargs['x'], kwargs['y'], kwargs['z'], kwargs['w']]
            elif len(kwargs)==0:
                self.q = [0, 0, 0, 1]
        elif len(args) == 1:
            if len(args[0]) == 4 and all(map(lambda x: type(x) in (float, int), args[0])):
                self.q = list(map(float, args[0]))
            else:
                raise ValueError("Invalid input--I can't make a quaternion from this")
        elif len(args) == 4 and all(map(lambda x: type(x) in (float, int), args)):
            self.q = list(map(float, args))
        else:
            raise ValueError("Invalid input--I can't make a quaternion from this")

    def w(self): return self.q[3]
    def x(self): return self.q[0]
    def y(self): return self.q[1]
    def z(self): return self.q[2]

    def __repr__(self):
        return "({}i + {}j + {}k + {})".format(self.x(), self.y(), self.z(), self.w())

    def __str__(self):
        return self.__repr__()

    def __neg__(self):
        return Quat([-self.q[i] for i in range(4)])

    def __add__(self, other):
        if type(other) == Quat:
            return Quat([self.q[i] + other.q[i] for i in range(4)])
        else:
            return Quat(self.q[0:3] + [self.q[3] + other])

    def __radd__(self, other):
        return self + other

    def __mul__(a, b):
        if type(b) == Quat:
            return Quat(
                x = a.w()*b.x() + a.x()*b.w() + a.y()*b.z() - a.z()*b.y(),
                y = a.w()*b.y() + a.y()*b.w() + a.z()*b.x() - a.x()*b.z(),
                z = a.w()*b.z() + a.z()*b.w() + a.x()*b.y() - a.y()*b.x(),
                w = a.w()*b.w() - a.x()*b.x() - a.y()*b.y() - a.z()*b.z(),
                )
        else:
            return Quat([b*self.q[i] for i in range(4)])

    def __sub__(self, other):
        return self + -other

    def __rsub__(self, other):
        return -self + other

    def __eq__(self, other):
        return (all( self.q[i] == other.q[i] for i in range(4)) or
                all(-self.q[i] == other.q[i] for i in range(4)))

    def nearly_equal(self, other, epsilon=1e-6):
        return (all(abs(self.q[i] - other.q[i])<epsilon for i in range(4)) or
                all(abs(self.q[i] + other.q[i])<epsilon for i in range(4)))

    def conj(self):
        return Quat(w=self.w(), x=-self.x(), y=-self.y(), z=-self.z())

    def norm(self):
        return sum(x**2 for x in self.q)**.5

    def normalize(self):
        n = self.norm()
        self.q = [x/n for x in self.q]

    @staticmethod
    def from_rot_matrix(m):
        t = sum(m[i][i] for i in range(3))
        if t>0:
            S = 2*(t+1)**.5
            return Quat(
                    w = S/4,
                    x = (m[2][1] - m[1][2])/S,
                    y = (m[0][2] - m[2][0])/S,
                    z = (m[1][0] - m[0][1])/S)
        elif (m[0][0] > m[1][1]) and (m[0][0] > m[2][2]):
            S = 2*(1 + m[0][0] - m[1][1] - m[2][2])**.5
            return Quat(
                    w = (m[2][1] - m[1][2]) / S,
                    x = 0.25 * S,
                    y = (m[0][1] + m[1][0]) / S,
                    z = (m[0][2] + m[2][0]) / S)
        elif m[1][1] > m[2][2]:
            S = 2*(1.0 + m[1][1] - m[0][0] - m[2][2])**.5
            return Quat(
                    w = (m[0][2] - m[2][0]) / S,
                    x = (m[0][1] + m[1][0]) / S,
                    y = 0.25 * S,
                    z = (m[1][2] + m[2][1]) / S)
        else:
            S = 2*(1.0 + m[2][2] - m[0][0] - m[1][1])**.5
            return Quat(
                    w = (m[1][0] - m[0][1]) / S,
                    x = (m[0][2] + m[2][0]) / S,
                    y = (m[1][2] + m[2][1]) / S,
                    z = 0.25 * S)

    def to_rot_matrix(self):
        s = self.norm()**-2
        qr = self.w(); qi = self.x(); qj = self.y(); qk = self.z()
        return [[ 1 - 2*s*(qj**2 + qk**2),     2*s*(qi*qj - qk*qr),     2*s*(qi*qk + qj*qr)],
                [     2*s*(qi*qj + qk*qr), 1 - 2*s*(qi**2 + qk**2),     2*s*(qj*qk - qi*qr)],
                [     2*s*(qi*qk - qj*qr),     2*s*(qj*qk + qi*qr), 1 - 2*s*(qi**2 + qj**2)]]

    @staticmethod
    def from_axis_angle(axis, angle):
        norm = sum(e**2 for e in axis)**.5
        axis = [e/norm for e in axis]
        assert(abs(sum(e**2 for e in axis)**.5 - 1) < 1e-6)
        return Quat(
                w = math.cos(angle/2),
                x = math.sin(angle/2)*axis[0],
                y = math.sin(angle/2)*axis[1],
                z = math.sin(angle/2)*axis[2])

    def to_axis_angle(self):
        norm = sum(e**2 for e in self.q[:3])**.5
        axis = [e/norm for e in self.q[:3]]
        angle = 2*math.acos(self.q[3])
        return (axis, angle)

    @staticmethod
    def from_ypr(yaw, pitch, roll):
        cy = math.cos(yaw/2); cp = math.cos(pitch/2); cr = math.cos(roll/2)
        sy = math.sin(yaw/2); sp = math.sin(pitch/2); sr = math.sin(roll/2)
        return Quat([cy*cp*sr - sy*sp*cr,
                    cy*sp*cr + sy*cp*sr,
                    sy*cp*cr - cy*sp*sr,
                    cy*cp*cr + sy*sp*sr])

    def to_ypr(self):
        w = self.w(); x = self.x(); y = self.y(); z = self.z();
        roll  = math.atan2(2*(w*x + y*z), 1 - 2*(x**2 + y**2))
        pitch = math.asin(2*(w*y - x*z))
        yaw   = math.atan2(2*(w*z + x*y), 1 - 2*(y**2 + z**2))
        return (yaw, pitch, roll)

    def log(self):
        theta = math.acos(self.q[3])
        v = [theta*e/math.sin(theta) for e in self.q[:3]]
        return Quat(v + [0.])

    def exp(self):
        theta = sum(e**2 for e in self.q[:3])**.5
        v = [e/theta for e in self.q[:3]]
        return Quat([math.sin(theta)*e for e in v] + [math.cos(theta)])
