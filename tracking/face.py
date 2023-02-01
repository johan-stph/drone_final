# This file is part of OpenCV Zoo project.
# It is subject to the license terms in the LICENSE file found in the same directory.
#
# Copyright (C) 2021, Shenzhen Institute of Artificial Intelligence and Robotics for Society, all rights reserved.
# Third party copyrights are property of their respective owners.

import argparse

import numpy as np
import cv2 as cv

from yunet import YuNet


# backends = [cv.dnn.DNN_BACKEND_OPENCV, cv.dnn.DNN_BACKEND_CUDA]
# targets = [cv.dnn.DNN_TARGET_CPU, cv.dnn.DNN_TARGET_CUDA, cv.dnn.DNN_TARGET_CUDA_FP16]
# help_msg_backends = "Choose one of the computation backends: {:d}: OpenCV implementation (default); {:d}: CUDA"
# help_msg_targets = "Choose one of the target computation devices: {:d}: CPU (default); {:d}: CUDA; {:d}: CUDA fp16"
# try:
#    backends += [cv.dnn.DNN_BACKEND_TIMVX]
#    targets += [cv.dnn.DNN_TARGET_NPU]
#    help_msg_backends += "; {:d}: TIMVX"
#    help_msg_targets += "; {:d}: NPU"
# except:
#    print('This version of OpenCV does not support TIM-VX and NPU. Visit https://github.com/opencv/opencv/wiki/TIM-VX-Backend-For-Running-OpenCV-On-NPU for more information.')


def visualize(image, results, box_color=(0, 255, 0)):
    output = image.copy()

    for det in (results if results is not None else []):
        bbox = det[0:4].astype(np.int32)
        cv.rectangle(output, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), box_color, 2)

    return output


if __name__ == '__main__':
    # Instantiate YuNet
    model = YuNet(modelPath='face_detection_yunet_2022mar.onnx',
                  inputSize=[320, 320],
                  confThreshold=0.9,
                  nmsThreshold=0.3,
                  topK=5000,
                  backendId=cv.dnn.DNN_BACKEND_OPENCV,
                  targetId=cv.dnn.DNN_TARGET_CPU)

    # Omit input to call default camera
    deviceId = 0
    cap = cv.VideoCapture(deviceId)
    w = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    model.setInputSize([w, h])

    while cv.waitKey(1) < 0:
        hasFrame, frame = cap.read()
        if not hasFrame:
            print('No frames grabbed!')
            break

        # Inference
        results = model.infer(frame)  # results is a tuple

        # Draw results on the input image
        frame = visualize(frame, results)

        # Visualize results in a new Window
        cv.imshow('Feed', frame)
