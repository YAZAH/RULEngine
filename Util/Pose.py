from ..Util.Position import Position


class Pose(object):
    """  Container of position and orientation """
    def __init__(self, position=Position(), orientation=0.0):
        assert(isinstance(position, Position)), 'position should be Position object.'
        assert(isinstance(orientation, (int, float))), 'orientation should be int or float value.'
        
        orientation = orientation % 360

        self.position = position
        self.orientation = orientation

    def __str__(self):
        return '[{}, theta={}]'.format(self.position, self.orientation)

    def __eq__(self, other):
        assert(isinstance(other, Pose)), 'eq operator should be Pose object.'
        return self.orientation == other.orientation and self.position == other.position

    def copy(self):
        return Pose(self.position.copy(), self.orientation)
