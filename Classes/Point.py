class Point:
    @classmethod
    def copy(cls, point):
        return Point(point.x, point.y)
        
    @classmethod
    def fromtuple(cls, tup):
        return cls(tup[0], tup[1])

    def astuple(self):
        return (self.x, self.y)

    def move(self, tup):
        self.x = lst[0]
        self.y = lst[1]
        if __name__ == "__main__":
            print('{0} -> {1} :: (Move[{2},{3}])'.format(old, self, lst[0], lst[1]))

    # Do not translate this point to origin unless it is to be rotated upon.
    def translate(self, lst):
        old = Point.copy(self)
        self.x += lst[0]
        self.y += lst[1]
        if __name__ == "__main__":
            print('{0} -> {1} :: (Translate[{2},{3}])'.format(old, self, lst[0], lst[1]))

    def rotate(self, theta):        
        rad = math.radians(theta)
        s = math.sin(rad)
        c = math.cos(rad)
        x = self.x
        y = self.y
        self.x = x * c - y * s
        self.y = x * s + y * c
        if __name__ == "__main__":
            print('{0} -> {1} :: (Rotate {2})'.format(Point(x,y), self, theta))
        
    def __init__(self, x, y):
        self.x = x
        self.y = y
            
    def __repr__(self):
        return "<Point( x:{0:7.2f}, y:{1:7.2f})>".format(self.x,self.y)
        
    def __str__(self):
        return "({0:7.2f}, {1:7.2f})".format(self.x, self.y)
        
