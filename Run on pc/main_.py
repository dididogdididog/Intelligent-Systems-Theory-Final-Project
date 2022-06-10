import cv2
from cv2 import imshow
import numpy as np
from threading import Thread
from pcCommunicate import connectPi

connector = connectPi('192.168.43.85')

rpi_name = ''
image = np.zeros((240, 320, 3))


def empty(v):
    pass

# untrans_width = 80
# untrans_height = 80
# trans_width = 80
# trans_height = 50


untrans_height = 50
trans_width = 80


def get_perspective_mat(img):
    height, width, _ = img.shape
    # src_points = np.array([[0, height], [width, height], [width-untrans_width, untrans_height], [untrans_width, untrans_height]], dtype = "float32")
    src_points = np.array([[0, height], [width, height], [width, untrans_height], [
                          0, untrans_height]], dtype="float32")
    # dst_points = np.array([[trans_width, height], [width-trans_width, height], [width-trans_width, trans_height], [trans_width, trans_height]], dtype = "float32")
    dst_points = np.array([[trans_width, height], [
                          width-trans_width, height], [width, 0], [0, 0]], dtype="float32")

    M = cv2.getPerspectiveTransform(src_points, dst_points)

    return M


def get_image():

    cv2.namedWindow('TrackBar')
    cv2.resizeWindow('TrackBar', 640, 320)
    cv2.createTrackbar('Threshold', 'TrackBar', 70, 255, empty)
    while True:
        global rpi_name
        global image
        rpi_name, image = connector.get_image()
        threshold = cv2.getTrackbarPos('Threshold', 'TrackBar')
        # image = cv2.flip(image, 0)
        # image = cv2.resize(image, (0, 0), fx = 0.2, fy = 0.2)
        height, width, _ = image.shape
        M = get_perspective_mat(image)
        birdeye = cv2.warpPerspective(
            image, M, [width, height], cv2.INTER_LINEAR)
        blue = birdeye[:, :, 0]
        bin = np.zeros_like(blue)
        bin[blue > threshold] = 255
        kernel = np.ones((3, 3), np.uint8)
        open = cv2.morphologyEx(bin, cv2.MORPH_OPEN, kernel)

        midline = []

        scan_top = 200
        scan_bot = 239
        offset = 0                 # The first line is to the 0: left; 1:right

        for i in range(scan_bot, scan_top, -1):
            flag = 0               # Whether a line has been detected
            leftline = 0
            rightline = 0

            for j in range(int(i*trans_width/height)+1, int(width/2)):
                if open[i, j] == 0:
                    leftline = j
            if leftline == 0 and i == scan_bot:
                offset = 1
            for j in range(int(width/2), int(i*-trans_width/height)+width-1):
                if open[i, j] == 0:
                    rightline = j
            if leftline == 0 and offset == 0:
                scan_top = i
                break
            if rightline == 0 and offset == 1:
                scan_top = i
                break
            if offset == 0:
                midline.append(int(leftline))
            elif offset == 1:
                midline.append(int(rightline))
            cv2.rectangle(birdeye, (leftline, i-1),
                          (rightline, i), (0, 0, 255), -1)

        # vertical axis of fitting curve
        x = np.arange(1000)[scan_top:scan_bot]
        if len(x) >= 3:
            # fitting with second order
            fit = np.polyfit(x, np.flip(midline), 2)
            for i in range(scan_top, scan_bot):
                cv2.circle(
                    birdeye, (int(fit[0]*i*i+fit[1]*i+fit[2]), i), 2, (255, 0, 0), -1)

            if offset == 0:
                pos = fit[0]*i*i+fit[1]*i+fit[2]-width/3
            elif offset == 1:
                pos = fit[0]*i*i+fit[1]*i+fit[2]-width*2/3
            ang = (2*fit[0]*(scan_top+scan_bot)/2+fit[1])
            cur = 2*fit[0]/(1+(2*fit[0]*i+fit[1])**2)**(3/2)

            K_pos = -1/100
            K_ang = 0.5
            K_cur = 0

            # print(pos*K_pos)
            # print(ang*K_ang)
            # print(cur*K_cur)

            turn = pos*K_pos+ang*K_ang+cur*K_cur
            command = ''
            command = 't ' + str(turn)
            connector.send_message(command)

        imshow('birdeye', birdeye)
        imshow('open', open)

        if(cv2.waitKey(10) == ord('q')):
            break

        # cv2.imshow(rpi_name, image)
        cv2.waitKey(1)


t = Thread(target=get_image)
t.start()

while True:
    # print(image[120, 160, 0])
    command = input('Enter your command: ')

    connector.send_message(command)
