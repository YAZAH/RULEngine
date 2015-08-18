from .Game.Ball import Ball
from .Game.Field import Field
from .Game.Game import Game
from .Game.Player import Player
from .Game.Referee import Referee
from .Game.Team import Team
from .Util.constant import PLAYER_PER_TEAM
import rule
import time
import serial
from serial_protocol import serial_protocol
import os
import math

serial_ports = [port for port in os.listdir('/dev') if port.startswith("ttyUSB")]
print(serial_ports)

ser = serial.Serial('/dev/' + serial_ports[0], 115200)

protocol = serial_protocol()

def convertPositionToSpeed(player, x, y, theta):
    current_theta = player.pose.orientation
    current_x = player.pose.position.x
    current_y = player.pose.position.y
    theta_direction = theta - current_theta
    if theta_direction >= math.pi:
        theta_direction -= 2 * math.pi
    elif theta_direction <= -math.pi:
        theta_direction += 2*math.pi

    theta_speed = 2 if abs(theta_direction) > 0.2 else 0.4
    new_theta = theta_speed if theta_direction > 0 else -theta_speed

    direction_x = x - current_x
    direction_y = y - current_y
    norm = math.hypot(direction_x, direction_y)
    speed = 1 if norm >= 750 else 0
    if norm:
      direction_x /= norm
      direction_y /= norm
    angle = math.atan2(direction_y, direction_x)
    cosangle = math.cos(math.radians(-current_theta))
    sinangle = math.sin(math.radians(-current_theta))
    new_x = (direction_x * cosangle - direction_y * sinangle) * speed
    new_y = (direction_y * cosangle + direction_x * sinangle) * speed

    return new_x, new_y, new_theta

def create_teams():
    blue_players = []
    yellow_players = []
    for i in range(PLAYER_PER_TEAM):
        bPlayer = Player(i, False)
        yPlayer = Player(i, True)
        blue_players.append(bPlayer)
        yellow_players.append(yPlayer)
    blue_team = Team(blue_players, False)
    yellow_team = Team(yellow_players, True)
    return blue_team, yellow_team


def create_ball():
    ball = Ball()
    return ball


def create_field():
    ball = create_ball()
    field = Field(ball)
    return field


def create_referee():
    referee = Referee()
    return referee


def create_game(strategy):
    blue_team, yellow_team = create_teams()
    field = create_field()
    referee = create_referee()
    blue_team_strategy = strategy(field, referee, blue_team, yellow_team)
    # yellow_team_strategy = WorstStrategy(field, referee, yellow_team, blue_team)

    game = Game(field, referee, blue_team, yellow_team, blue_team_strategy)

    return game


def update_game_state(game, engine):
    referee_commands = engine.grab_referee_commands()
    if referee_commands:
        referee_command = referee_commands[0]
        game.update_game_state(referee_command)


def update_players_and_ball(game, engine):
    vision_frames = engine.grab_vision_frames()
    if vision_frames:
        vision_frame = vision_frames[0]
        game.update_players_and_ball(vision_frame)


def update_strategies(game):
    game.update_strategies()


def send_robot_commands(game, engine):
    commands = game.get_commands()
    for command in commands:
        #robot_command = command.to_robot_command()
        if command.is_speed_command:
          x,y = (0,0)
        else:
          position = command.pose.position
          x, y, theta = convertPositionToSpeed(command.player, position.x, position.y, 0)     
          x, y = -y, x

        sercommand = bytearray(protocol.createSpeedCommand(x, y, 0, 0))
        print(x,y)
        ser.write(sercommand)
        #engine.send_robot_command(robot_command)



def start_game(strategy):

    engine = rule.Rule()

    visionPlugin = rule.VisionPlugin("224.5.23.2", 10005, "VisionPlugin");
    refereePlugin = rule.RefereePlugin("224.5.23.1", 10003, "RefereePlugin");
    navigatorPlugin = rule.UDPNavigatorPlugin(20011, "127.0.0.1", "UDPNavigatorPlugin");
    engine.install_plugin(visionPlugin)
    engine.install_plugin(refereePlugin)
    engine.install_plugin(navigatorPlugin)

    engine.start()

    game = create_game(strategy)

    while True:  # TODO: Replace with a loop that will stop when the game is over
        time.sleep(0.03)
        if ser.inWaiting():
            print(ser.read())
        update_game_state(game, engine)
        update_players_and_ball(game, engine)
        update_strategies(game)
        send_robot_commands(game, engine)

    engine.stop()
