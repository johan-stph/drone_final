import djitellopy
import cv2
import numpy as np

import evaluate_pos
from tracking.yunet import YuNet

tello = djitellopy.Tello()
cap = cv2.VideoCapture(0)
cmd = evaluate_pos.CommandOrder(tello)
w, h = 360, 240

model = YuNet(modelPath='tracking/face_detection_yunet_2022mar.onnx',
              inputSize=[320, 320],
              confThreshold=0.9,
              nmsThreshold=0.3,
              topK=5000,
              backendId=cv2.dnn.DNN_BACKEND_OPENCV,
              targetId=cv2.dnn.DNN_TARGET_CPU)

# w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
model.setInputSize([w, h])


def provide_img(drone_active: bool):
    img = tello.get_frame_read().frame if drone_active else cap.read()[1]
    return cv2.resize(img, (w, h))


def run_game_loop(drone: bool, run_detection: bool = True, should_send_commands: bool = True):
    counter = 0
    cmd.initialize()
    while True:
        img = provide_img(drone)
        if img is None:
            continue
        if run_detection:
            img, info = find_img_v2(img)
            print(info)
            if should_send_commands and counter == 60:
                cmd.order_command(info)
                counter = -1
            counter += 1

        cv2.imshow("Output", img)
        cv2.waitKey(1)


def find_img_v2(img):
    faces = model.infer(img)

    myFaceListC = []

    myFaceListArea = []

    for det in faces if faces is not None else []:
        bbox = det[0:4].astype(np.int32)
        x = bbox[0]
        y = bbox[1]
        w = bbox[2]
        h = bbox[3]

        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cx = x + w // 2

        cy = y + h // 2

        area = w * h

        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

        myFaceListC.append([cx, cy])

        myFaceListArea.append(area)

    if len(myFaceListArea) != 0:

        i = myFaceListArea.index(max(myFaceListArea))

        return img, [myFaceListC[i], myFaceListArea[i]]

    else:

        return img, [[0, 0], 0]


def setup_drone():
    tello.connect()
    tello.streamon()


def shutdown():
    tello.streamoff()


def main(drone=False):
    drone = True
    if drone:
        setup_drone()

    run_game_loop(drone)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        shutdown()
        cmd.send_land()
