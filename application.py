import djitellopy
import cv2

import evaluate_pos
from finding.findpad import find_img

tello = djitellopy.Tello()
cap = cv2.VideoCapture(0)
cmd = evaluate_pos.CommandOrder(tello)
w, h = 360, 240


def provide_img(drone_active: bool):
    img = tello.get_frame_read().frame if drone_active else cap.read()[1]
    return cv2.resize(img, (w, h))


def run_game_loop(drone: bool, run_detection: bool = True, should_send_commands: bool = True):
    error = 0
    cmd.initialize()
    while True:
        img = provide_img(drone)
        if img is None:
            continue
        if run_detection:
            img, info = find_img(img)
            if should_send_commands:
                error = cmd.order_command(info, error)

        cv2.imshow("Output", img)
        cv2.waitKey(1)


def setup_drone():
    tello.connect()
    tello.streamon()


def main(drone=False):
    drone = True
    if drone:
        setup_drone()

    run_game_loop(drone)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        cmd.send_land()
