import time

from djitellopy import Tello

pid = [0.4, 0.4, 0]
fbRange = [10000, 7500]
w, h = 360, 240

FORWARD = 10
UP = 5
DOWN = 20
RIGHT = 10
LEFT = 10


class CommandOrder:
    def __init__(self, tello: Tello):
        self.tello = tello

    def initialize(self):
        self.tello.takeoff()
        print("BATTERY", self.tello.get_battery())

        self.tello.send_rc_control(0, 0, 8, 0)
        time.sleep(2.2)
        print("Höhe ist:", self.tello.get_height())

    def order_command(self, info):
        area = info[1]
        x, y = info[0]
        fb = 0
        right_left_error = x - (w // 2)
        height = y - (h // 2)
        lr = 0
        ud = 0

        if right_left_error > 0:
            lr = min(RIGHT, int(right_left_error // 10))
        elif right_left_error < 0:
            lr = -min(LEFT, int(-right_left_error // 10))

        if height > 0:
            ud = -DOWN
        elif height < 0:
            ud = UP

        print(area)
        if area >= fbRange[0]:
            self.send_command(fb=10)
            time.sleep(0.6)
            self.send_land()
        elif area != 0:
            fb = 20 if area < 1000 else FORWARD
        if x == 0:
            lr = 0
            ud = 0
        self.send_command(fb=fb, ud=ud, lr=lr)

    def send_command(self, fb=0, ud=0, speed=0, lr=0):

        self.tello.send_rc_control(lr, fb, ud, speed)
        print("HEIGHT", self.tello.get_height())

    def send_land(self):
        self.tello.land()
        raise KeyboardInterrupt("Drone has landed")

    def search(self):
        self.tello.send_command_with_return("cw 30")
