import cv2 as cv
import numpy as np
from time import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter

# initialize the WindowCapture class

wincap = WindowCapture('2009scape')
vision_iron = Vision("iron2.png")
vision_iron.init_control_gui()

#West Varrock Iron mining threshold values
hsv_filter = HsvFilter(6, 129, 48, 8, 193, 57, 0, 15, 0, 12)

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()
    processed_image = vision_iron.apply_hsv_filter(screenshot, hsv_filter=hsv_filter)
    #cv.imshow('Computer Vision', screenshot)
    rectangles = vision_iron.find_ore_deposit(processed_image, threshold=0.35)
    print(rectangles)
    #points = vision_iron.find_ore_deposit(processed_image, threshold=0.3 )
    output = vision_iron.draw_rectangles(screenshot, rectangles)
    #output = vision_iron.draw_crosshairs(screenshot, rectangles)
    cv.imshow("Matches", output)
    cv.imshow("Processed", processed_image)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')