from cvzone.HandTrackingModule import HandDetector
import cv2
import os
import numpy as np


width, height = 1280, 720
gestureThreshold = 400
folder = "Presentation 2"

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detectorHand = HandDetector(detectionCon=0.8, maxHands=1)

annotations = [[]]
annotationNumber = -1
annotationStart = False
heightsmall, widthsmall = int(120 * 1), int(220 * 1)
imgList = []
delay = 25
buttonPressed = False
counter = 0
drawMode = False
imgNumber = 0
delayCounter = 0

pathImages = sorted(os.listdir(folder), key=len)
print(pathImages)

while True:

    success, img = cap.read()
    img = cv2.flip(img, 1)
    FullImagepath = os.path.join(folder, pathImages[imgNumber])
    currentImg = cv2.imread(FullImagepath)

    hands, img = detectorHand.findHands(img)

    cv2.line(img, (0, gestureThreshold), (width, gestureThreshold), (0, 255, 0), 8)

    if hands and buttonPressed is False:

        hand = hands[0]
        cx, cy = hand["center"]
        lmList = hand["lmList"]
        fingers = detectorHand.fingersUp(hand)

        xVal = int(np.interp(lmList[8][0], [width // 2, width], [0, width]))
        yVal = int(np.interp(lmList[8][1], [150, height - 150], [0, height]))
        indexFinger = xVal, yVal
        if cy <= gestureThreshold:
            if fingers == [1, 0, 0, 0, 0]:
                print("Left")
                buttonPressed = True
                if imgNumber > 0:
                    imgNumber -= 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
            if fingers == [0, 0, 0, 0, 1]:
                print("Right")
                buttonPressed = True
                if imgNumber < len(pathImages) - 1:
                    imgNumber += 1
                    annotations = [[]]
                    annotationNumber = -1
                    annotationStart = False
        if fingers == [0, 1, 1, 0, 0]:
            cv2.circle(currentImg, indexFinger, 12, (0, 0, 255), cv2.FILLED)
        if fingers == [0, 1, 0, 0, 0]:
            if annotationStart is False:
                annotationStart = True
                annotationNumber += 1
                annotations.append([])
            print(annotationNumber)
            annotations[annotationNumber].append(indexFinger)
            cv2.circle(currentImg, indexFinger, 12, (0, 0, 255), cv2.FILLED)
        else:
            annotationStart = False
        if fingers == [0, 1, 1, 1, 0]:
            if annotations:
                annotations.pop(-1)
                annotationNumber -= 1
                buttonPressed = True
    else:
        annotationStart = False
    if buttonPressed:
        counter += 1
        if counter > delay:
            counter = 0
            buttonPressed = False
    for i, annotation in enumerate(annotations):
        for j in range(len(annotation)):
            if j != 0:
                cv2.line(currentImg, annotation[j - 1], annotation[j], (0, 0, 200), 12)
    imgSmall = cv2.resize(img, (widthsmall, heightsmall))
    h, w, _ = currentImg.shape
    currentImg[0:heightsmall, w - widthsmall: w] = imgSmall

    cv2.imshow("Slides", currentImg)
    cv2.imshow("Image", img)

    key = cv2.waitKey(1)
    if key == ord('q'):
        break