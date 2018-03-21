import numpy as np
import cv2
from matplotlib import pyplot as plt

selected_frame = np.loadtxt("selected_frame.txt", dtype=np.int, delimiter=",")
y0y1 = np.loadtxt("y0y1.txt", delimiter=",")

centerX = 1030
centerY = 570

# install youtube-dl and run command below to get video.mp4
# youtube-dl "https://www.youtube.com/watch?v=rRxB4gjE014" --output video.mp4
cap = cv2.VideoCapture('video.mp4')

i = 0
while True:

    i += 1
    ret, frame = cap.read()
    if i in selected_frame:
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

        cv2.imwrite('images/waves-%06i.jpg' % (i), dst[470:, 1300:][:320, :480])
        print(i)

        if cv2.waitKey(10) == 27:
            break
        if i >= max(selected_frame):
            print("Done !!!")
            break