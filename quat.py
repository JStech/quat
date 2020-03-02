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
        return "{} + {}i + {}j + {}k".format(self.q[3], self.q[0], self.q[1], self.q[2])

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
        return all(self.q[i] == other.q[i] for i in range(4))

    def nearly_equal(self, other):
        return all(abs(self.q[i] - other.q[i])<1e-6 for i in range(4))
