import pyautogui
import cv2

import os
import time
import pathlib
from collections import namedtuple

from .config import *

IMAGES = {} 
ImgData = namedtuple('ImgData', 'name file position')

center = pyautogui.center

def load_images(fp):
    fp = pathlib.Path(fp)
    for f in os.listdir(fp):
        fname = f
        f = fp / fname
        if os.path.isfile(f) and '---' in fname:
            name, pos = fname.split('.')[0].split('---')
            IMAGES[name] = ImgData(name, str(f.absolute()), tuple(map(int, pos.split(','))))

def retake_img(name):
    img = IMAGES[name]
    pyautogui.screenshot(img.file, g_to_s(img.position))

def test_changed_img(name, gray=False):
    img = IMAGES[name]
    old = cv2.imread(img.file).copy()
    retake_img(name)
    new = cv2.imread(img.file).copy()
    if gray:
        old = cv2.cvtColor(old, cv2.COLOR_RGB2GRAY) 
        new = cv2.cvtColor(new, cv2.COLOR_RGB2GRAY) 
    similar = abs(float(cv2.matchTemplate(old, new, cv2.TM_CCOEFF_NORMED)))
    return similar < 0.8

def locate(img_data, **kwargs):
    pos = list(img_data.position)
    pos = g_to_s(pos)
    # pos[2] += pos[0]
    # pos[3] += pos[1]
    # print(pos)
    result = (pyautogui.locateOnScreen(img_data.file, confidence=0.90, region=pos, **kwargs))
    return result

def wait_many_img(names):
    print('wait_many_img', names)
    while True:
        for name in names:
            result = locate(IMAGES[name])
            if result: 
                return name, result
        time.sleep(0.8)

def wait_img(name):
    return wait_many_img((name, ))[1]


def click_wait_img(name):
    pyautogui.click(pyautogui.center(wait_img(name)))

def find_img(name):
    return locate(IMAGES[name])

def click_img(name):
    pos = locate(IMAGES[name])
    if pos:
        pyautogui.click(*center(pos))
    return pos

def click(game_pos):
    pyautogui.click(*(g_to_s(game_pos)))

def scroll_wait_img(name, dx, dy):
    pos = center(wait_img(name))
    pyautogui.moveTo(*pos)
    pyautogui.dragRel(dx, dy, duration=1)


load_images('images')
if __name__ == '__main__':
    wait_img('menu')