import cv2
import numpy as np
from hsvfilter import HsvFilter
import pyautogui
class Vision:

    TRACKBAR_WINDOW = "Trackbars"

    object_img = None
    object_w = 0
    object_h = 0
    method = None

    def __init__(self, object_img_path, method=cv2.TM_CCOEFF_NORMED):
        if object_img_path:
            self.object_img = cv2.imread(object_img_path, cv2.IMREAD_UNCHANGED)

            self.object_w = self.object_img.shape[1]
            self.object_h = self.object_img.shape[0]

        self.method = method

    def find_ore_deposit(self, source_img, threshold=0.35):
        print("here")
        #source_img = cv2.imread(source_img_path, cv2.IMREAD_UNCHANGED)
        # object_img = cv2.imread(object_img_path, cv2.IMREAD_UNCHANGED)

        # object_w = object_img.shape[1]
        # object_h = object_img.shape[0]

        # method = cv2.TM_CCOEFF_NORMED
        result = cv2.matchTemplate(source_img, self.object_img, self.method)

        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.object_w, self.object_h]
            rectangles.append(rect)
            rectangles.append(rect)
        print("first for loop done")
        rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.5)
        #print(rectangles)

        return rectangles

    def get_click_points(self, rectangles):
        points = []
    # if len(rectangles):
    #     #object_w = object_img.shape[1]
    #     #object_h = object_img.shape[0]
    #     line_color = (0,255,0)
    #     line_type = cv2.LINE_4
    #     marker_color = (0, 255, 0)
    #     marker_type = cv2.MARKER_CROSS
        for (x, y, w, h) in rectangles:
            #print("starting for loop")
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x, center_y))

        return points

    def draw_rectangles(self, source_img, rectangles):
        line_color = (0,255,0)
        line_type = cv2.LINE_4

        for (x, y, w, h) in rectangles:
            #if debug_mode == "rectangles":
                #print("debugging rectangles")
            top_left = (x, y)
            bottom_right = (x + w, y + h)
            cv2.rectangle(source_img, top_left, bottom_right, line_color, 1, line_type)
            
        return source_img
                
    def draw_crosshairs(self, source_img, points):            
                #elif debug_mode == "points":
                #    print("debugging points")
        marker_color = (255, 0, 255)
        marker_type = cv2.MARKER_CROSS
        
        for (center_x, center_y) in points:
            cv2.drawMarker(source_img, (center_x, center_y), marker_color, marker_type)
                    #cv2.imshow("matches", source_img)
                    #cv2.waitKey()
        return source_img
        # if debug_mode:
        #     cv2.imshow("Matches", source_img)
        #     #cv2.waitKey()
        # return points
    def init_control_gui(self):
        cv2.namedWindow(self.TRACKBAR_WINDOW, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(self.TRACKBAR_WINDOW, 350, 700)

        def nothing(position):
            pass

        cv2.createTrackbar("Hmin", self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv2.createTrackbar("Smin", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar("Vmin", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar("Hmax", self.TRACKBAR_WINDOW, 0, 179, nothing)
        cv2.createTrackbar("Smax", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar("Vmax", self.TRACKBAR_WINDOW, 0, 255, nothing)


        cv2.setTrackbarPos("Hmax", self.TRACKBAR_WINDOW, 179)
        cv2.setTrackbarPos("Smax", self.TRACKBAR_WINDOW, 255)
        cv2.setTrackbarPos("Vmax", self.TRACKBAR_WINDOW, 255)

        cv2.createTrackbar("Sadd", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar("Ssub", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar("Vadd", self.TRACKBAR_WINDOW, 0, 255, nothing)
        cv2.createTrackbar("Vsub", self.TRACKBAR_WINDOW, 0, 255, nothing)

    def get_hsv_filter_from_controls(self):
        hsv_filter = HsvFilter()
        hsv_filter.Hmin = cv2.getTrackbarPos("Hmin", self.TRACKBAR_WINDOW)
        hsv_filter.Smin = cv2.getTrackbarPos("Smin", self.TRACKBAR_WINDOW)
        hsv_filter.Vmin = cv2.getTrackbarPos("Vmin", self.TRACKBAR_WINDOW)
        hsv_filter.Hmax = cv2.getTrackbarPos("Hmax", self.TRACKBAR_WINDOW)
        hsv_filter.Smax = cv2.getTrackbarPos("Smax", self.TRACKBAR_WINDOW)
        hsv_filter.Vmax = cv2.getTrackbarPos("Vmax", self.TRACKBAR_WINDOW)
        hsv_filter.Sadd = cv2.getTrackbarPos("Sadd", self.TRACKBAR_WINDOW)
        hsv_filter.Ssub = cv2.getTrackbarPos("Ssub", self.TRACKBAR_WINDOW)
        hsv_filter.Vadd = cv2.getTrackbarPos("Vadd", self.TRACKBAR_WINDOW)
        hsv_filter.Vsub = cv2.getTrackbarPos("Vsub", self.TRACKBAR_WINDOW)
        return hsv_filter
        
    def apply_hsv_filter(self, original_image, hsv_filter=None):
        hsv = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)

        if not hsv_filter:
            hsv_filter = self.get_hsv_filter_from_controls()

        h, s, v = cv2.split(hsv)
        s = self.shift_channel(s, hsv_filter.Sadd)
        s = self.shift_channel(s, -hsv_filter.Ssub)
        v = self.shift_channel(v, hsv_filter.Vadd)
        v = self.shift_channel(v, -hsv_filter.Vsub)
        hsv = cv2.merge([h, s, v])

        lower = np.array([hsv_filter.Hmin, hsv_filter.Smin, hsv_filter.Vmin])
        upper = np.array([hsv_filter.Hmax, hsv_filter.Smax, hsv_filter.Vmax])

        mask = cv2.inRange(hsv, lower, upper)
        result = cv2.bitwise_and(hsv, hsv, mask=mask)

        img = cv2.cvtColor(result, cv2.COLOR_HSV2BGR)
        return img


    def shift_channel(self, c, amount):
        if amount > 0:
            lim = 255 - amount
            c[c >= lim] = 255
            c[c < lim] += amount
        elif amount < 0:
            amount = -amount
            lim = amount
            c[c <= lim] = 0
            c[c > lim] -= amount
        return c
