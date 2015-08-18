import rule
import math
from ..Util.Pose import Pose, Position
#from ..Game.Player import Player
from ..Game.Team import Team
from ..Util.area import *
from ..Util.geometry import *
from ..Util.constant import *


class _Command(object):
    """  Object which format standard command to Strategy """
    def __init__(self, player):
        # Parameters Assertion
        #assert(isinstance(player, Player)), '_Command.Player should be Player object (not {})'.format(type(player))

        self.player = player
        self.dribble = True
        self.dribble_speed = 10
        self.kick = False
        self.kick_speed = 0
        self.is_speed_command = False
        self.pose = Pose()
        self.is_yellow = player.is_yellow

    def to_robot_command(self):
        robot_command = rule.RobotCommand()
        robot_command.is_team_yellow = self.is_yellow
        robot_command.dribble = self.dribble
        robot_command.dribble_speed = self.dribble_speed
        robot_command.kick = self.kick
        robot_command.kick_speed = self.kick_speed
        robot_command.robot_id = self.player.id
        robot_command.stop = self.is_speed_command
        robot_command.pose.coord.x = self.pose.position.x
        robot_command.pose.coord.y = self.pose.position.y
        robot_command.pose.orientation = self.pose.orientation * math.pi / 180

        return robot_command


# class SetSpeed(_Command):
#     def __init__(self, player, team, pose):
#         # Parameters Assertion
#         assert(isinstance(player, Player))
#         assert(isinstance(team, Team))
#         assert(isinstance(pose, Pose))
#
#         super().__init__(player, team)
#         self.is_speed_command = True
#         pose.orientation = pose.orientation * 180 / math.pi
#         if m.sqrt(pose.position.x ** 2 + pose.position.y ** 2) <= KICK_MAX_SPD :
#             self.pose = pose
#         else:
#             agl = m.radians(theta(pose.position.x, pose.position.y))
#             dst = KICK_MAX_SPD
#             x = dst * m.cos(agl)
#             y = dst * m.sin(agl)
#             self.pose = Pose(Position(x, y), convertAngle180(pose.orientation))


class MoveTo(_Command):
    """ Command which move player to another position """
    def __init__(self, player, position):
        # Parameters Assertion
        #assert(isinstance(player, Player))
        assert(isinstance(position, Position))

        super().__init__(player)
        self.pose.position = stayInsideSquare(position,
                                              FIELD_Y_TOP,
                                              FIELD_Y_BOTTOM,
                                              FIELD_X_LEFT,
                                              FIELD_X_RIGHT)
        self.pose.orientation = cvt_angle_180(player.pose.orientation)


class Rotate(_Command):
    """ Command which rotate player on its position """
    def __init__(self, player, orientation):
        # Parameters Assertion
        #assert(isinstance(player, Player))
        assert(isinstance(orientation, (int, float)))

        super().__init__(player)
        self.pose.orientation = cvt_angle_180(orientation)
        self.pose.position = stayInsideSquare(player.pose.position,
                                              FIELD_Y_TOP,
                                              FIELD_Y_BOTTOM,
                                              FIELD_X_LEFT,
                                              FIELD_X_RIGHT)


class MoveToAndRotate(_Command):
    """ Command which move and rotate player to another position """
    def __init__(self, player, pose):
        # Parameters Assertion
        #assert(isinstance(player, Player))
        assert(isinstance(pose, Pose))

        super().__init__(player)
        position = stayInsideSquare(pose.position,
                                    FIELD_Y_TOP,
                                    FIELD_Y_BOTTOM,
                                    FIELD_X_LEFT,
                                    FIELD_X_RIGHT)
        self.pose = Pose(position, cvt_angle_180(pose.orientation))


class Kick(_Command):
    """ Command which activate player kicker on its position """
    def __init__(self, player, kick_speed=5):
        # Parameters Assertion
        #assert(isinstance(player, Player))
        assert(isinstance(kick_speed, (int, float)))
        assert(0 <= kick_speed <= 8)

        super().__init__(player)
        self.kick = True
        self.kick_speed = kick_speed
        self.is_speed_command = True
        self.pose = player.pose


class Stop(_Command):
    """ Command which stop player on its position """
    def __init__(self, player):
        # Parameters Assertion
        #assert(isinstance(player, Player))

        super().__init__(player)
        self.is_yellow = player.is_yellow
        self.is_speed_command = True
        self.pose = Pose()
