class Quat:
    def __init__(self, *args):
        if len(args) == 0:
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

    def __repr__(self):
        return "{} + {}i + {}j + {}k".format(self.q[3], self.q[0], self.q[1], self.q[2])

    def __str__(self):
        return self.__repr__()

    def __add__(self, other):
        if type(other) == Quat:
            return Quat([self.q[i] + other.q[i] for i in range(4)])
        else:
            print(self.q[0:3] + [self.q[3] + other])
            return Quat(self.q[0:3] + [self.q[3] + other])
