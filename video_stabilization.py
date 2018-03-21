import numpy as np
import cv2

y0y1 = np.loadtxt("y0y1.txt", delimiter=",")

centerX = 1030
centerY = 570

# install youtube-dl and run command below to get video.mp4
#youtube-dl "https://www.youtube.com/watch?v=rRxB4gjE014" --output video.mp4
cap = cv2.VideoCapture('video.mp4')


i = -1
while True:
    i += 1
    ret, frame = cap.read()
    im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    rows, cols, X = im.shape

    M1 = np.float32([[1, 0, 0],
                     [0, 1, centerY - y0y1[i].dot([1 - (centerX / 1920), centerX / 1920])],
                     [0, 0, 1]])

    alpha = np.cos(np.arctan(y0y1[i].dot([-1, 1]) / 1920))
    beta = np.sin(np.arctan(y0y1[i].dot([-1, 1]) / 1920))

    M2 = np.float32([[alpha, beta, (1 - alpha) * centerX],
                     [-beta, alpha, beta * centerX + (1 - alpha) * centerY],
                     [0, 0, 1]])

    dst = cv2.warpAffine(im, M1.dot(M2)[:2], (cols, rows))


    cv2.imshow('stabilized video', dst)


    if cv2.waitKey(10) == 27:
        break

