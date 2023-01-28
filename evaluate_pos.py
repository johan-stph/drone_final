import time

from djitellopy import Tello
import numpy as np

pid = [0.4, 0.4, 0]
fbRange = [10000, 7500]
w, h = 360, 240


class CommandOrder:
    def __init__(self, tello: Tello):
        self.tello = tello

    def initialize(self):
        self.tello.takeoff()
        self.tello.send_rc_control(0, 0, 25, 0)
        time.sleep(2.2)
        print("Höhe ist:", self.tello.get_height())

    def order_command(self, info, pError):
        area = info[1]
        x, y = info[0]
        fb = 0
        error = x - (w // 2)
        height = y - (h // 2)
        # speed = pid[0] * error + pid[1] * (error - pError)
        # speed = int(np.clip(speed, -100, 100))
        lr = 0
        ud = 0

        if error > 0:
            lr = 5
        elif error < 0:
            lr = -5

        if height > 0:
            ud = -5
        elif height < 0:
            ud = 5

        print(area)
        if area >= fbRange[0]:
            self.send_command(fb=10)
            time.sleep(0.1)
            self.send_land()
        elif area != 0:
            fb = 5
        if x == 0:
            lr = 0
            ud = 0
            speed = 0
            error = 0
        self.send_command(fb=fb, ud=ud, lr=lr)
        return error

    def send_command(self, fb=0, ud=0, speed=0, lr=0):
        self.tello.send_rc_control(lr, fb, ud, speed)

    def send_land(self):
        self.tello.land()
        raise KeyboardInterrupt("Drone has landed")
