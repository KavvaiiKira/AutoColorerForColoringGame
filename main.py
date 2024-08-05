import os
import cv2
import mss.tools
import numpy as np
import win32api
import win32con
import time

top = 105
left = 180
width = 1000
height = 1095


def get_screenshot():

    with mss.mss() as sct:
        monitor = {"top": top, "left": left, "width": width, "height": height}
        output = "sct-{top}x{left}_{width}x{height}.png".format(**monitor)
        sct_img = sct.grab(monitor)
        mss.tools.to_png(sct_img.rgb, sct_img.size, output=output)

    return output


def get_pixels_to_color_cords(screenshot_path):
    image = cv2.imread(screenshot_path)
    gray_color_array = np.array([139, 139, 143])
    mask = cv2.inRange(image, gray_color_array, gray_color_array)

    return cv2.findNonZero(mask)


def click(x, y):
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)


def set_next_color():
    win32api.keybd_event(0x45, 0, 0, 0)
    time.sleep(0.5)
    win32api.keybd_event(0x45, 0, win32con.KEYEVENTF_KEYUP, 0)


def main():
    print("Set number of colors:")
    number_of_colors = input()

    for color_number in range(1, int(number_of_colors) + 1):
        screenshot_file_name = get_screenshot()
        pixels_to_color_cords = get_pixels_to_color_cords(screenshot_file_name)

        while pixels_to_color_cords is not None and len(pixels_to_color_cords) != 0:
            click(pixels_to_color_cords[0][0][0] + left, pixels_to_color_cords[0][0][1] + top)

            os.remove(screenshot_file_name)
            screenshot_file_name = get_screenshot()
            pixels_to_color_cords = get_pixels_to_color_cords(screenshot_file_name)

        os.remove(screenshot_file_name)

        set_next_color()


if __name__ == "__main__":
    main()
