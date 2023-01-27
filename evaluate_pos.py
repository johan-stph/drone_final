import time

from djitellopy import Tello
import numpy as np

pid = [0.4, 0.4, 0]
fbRange = [6200, 6800]
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
        error = x - w // 2
        speed = pid[0] * error + pid[1] * (error - pError)
        speed = int(np.clip(speed, -100, 100))
        print(area)
        if area >= fbRange[0]:
            self.send_command(-5, speed)
            self.send_land()
        elif area != 0:
            fb = 5
        if x == 0:
            speed = 0
            error = 0
        self.send_command(fb, speed)
        return error

    def send_command(self, fb, speed):
        self.tello.send_rc_control(0, fb, 0, speed)

    def send_land(self):
        self.tello.land()
        raise KeyboardInterrupt("Drone has landed")
