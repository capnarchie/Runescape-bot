import cv2
import numpy as np

def find_ore_deposit(source_img_path, object_img_path, threshold=0.35, debug_mode=None):
    print("here")
    source_img = cv2.imread(source_img_path, cv2.IMREAD_UNCHANGED)
    object_img = cv2.imread(object_img_path, cv2.IMREAD_UNCHANGED)

    object_w = object_img.shape[1]
    object_h = object_img.shape[0]

    method = cv2.TM_CCOEFF_NORMED
    result = cv2.matchTemplate(source_img, object_img, method)

    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    rectangles = []
    for loc in locations:
        rect = [int(loc[0]), int(loc[1]), object_w, object_h]
        rectangles.append(rect)
        rectangles.append(rect)
    print("first for loop done")
    rectangles, weights = cv2.groupRectangles(rectangles, 1, 0.5)
    print(rectangles)

    points = []
    print("here")
    if len(rectangles):
        print("object found")

        #object_w = object_img.shape[1]
        #object_h = object_img.shape[0]
        line_color = (0,255,0)
        line_type = cv2.LINE_4
        marker_color = (0, 255, 0)
        marker_type = cv2.MARKER_CROSS


        for (x, y, w, h) in rectangles:
            print("starting for loop")
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x,center_y))
            print("points exist")
            if debug_mode == "rectangles":
                print("debugging rectangles")
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                cv2.rectangle(source_img, top_left, bottom_right, line_color, 1, line_type)
            elif debug_mode == "points":
                print("debugging points")
                cv2.drawMarker(source_img, (center_x, center_y), marker_color, marker_type)
                #cv2.imshow("matches", source_img)
                #cv2.waitKey()
        if debug_mode:
            cv2.imshow("Matches", source_img)
            cv2.waitKey()
    return points

points = find_ore_deposit("screenshot3.png", "copper3.png", debug_mode="rectangles")
print(points)