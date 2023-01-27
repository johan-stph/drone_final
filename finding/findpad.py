import cv2

cascade = cv2.CascadeClassifier("./cascade/haarcascades/haarcascade_frontalface_default.xml")


def find_img(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = cascade.detectMultiScale(imgGray, 1.2, 8)

    myFaceListC = []

    myFaceListArea = []

    for (x, y, w, h) in faces:
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
