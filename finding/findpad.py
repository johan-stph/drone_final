import cv2

cascade = cv2.CascadeClassifier("cascade/cascade.xml")


def find_pad(img):
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = cascade.detectMultiScale(img_gray, 1.2, 8)

    for (x, y, w, h) in faces:
        print(x, y, w, h)
        print(img.shape)
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)



