import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from vision import Vision

# initialize the WindowCapture class

wincap = WindowCapture('2009scape')

cascade_iron = cv.CascadeClassifier("cascade/cascade.xml")
vision_iron = Vision(None)

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    rectangles = cascade_iron.detectMultiScale(screenshot)

    detection_image = vision_iron.draw_rectangles(screenshot, rectangles)
    cv.imshow("screenshot", detection_image)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    key = cv.waitKey(1)
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
    # Press F to save image containing image you want to be detected
    elif key == ord("f"):
        cv.imwrite("positive/{}.jpg".format(loop_time), screenshot)
    # Press D to save image not containing image you want to be detected
    elif key == ord("d"):
        cv.imwrite("negative/{}.jpg".format(loop_time), screenshot)

print('Done.')