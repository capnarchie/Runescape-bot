import pyautogui
import time
import random
import cv2
#screenshot = pyautogui.screenshot()
#screenshot2 = pyautogui.screenshot("my_screenshot.png")
time.sleep(5)
# copperlocation = pyautogui.locateCenterOnScreen("copper.png")
# pyautogui.click(copperlocation)
# print(copperlocation)
# def main():
#     time.sleep(7)
#     findOre()
#     #pyautogui.click(copperX, copperY)
#     print("clicked")

time.sleep(5)
def findOre():
    x = 300
    y = 300
    width = 1300
    height = 700
    img = pyautogui.screenshot(region = (x,y,width,height))
    ore_colors = ["734E2E", "624327", "6E4B2C", (110, 75, 44), (109, 74, 43), (106, 72, 42)]

    for i in range(0, 910000):
        random_x = random.randint(0, width-1)
        random_y = random.randint(0, height-1)
        sample_color = img.getpixel((random_x, random_y))
        print(sample_color)
        print(random_x)
        print(random_y)


        if sample_color in ore_colors:
            pyautogui.moveTo(random_x, random_y)
            time.sleep(3)



print(findOre())