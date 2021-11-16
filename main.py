#import os
#import sys
#from PIL import Image
#import imagehash
import sys
import threading
from datetime import date

import pyautogui
import pydirectinput
import win32gui
import pyscreenshot as ImageGrab
import traceback

MASTER_BUTTON = [1500, 425]
SKILL_HEIGHT = 755
SERVANT_HEIGHT = 615
NP_HEIGHT = 300
CARD_HEIGHT = 650
MASTER_HEIGHT = 425
SKILL_LIST = [100, 200, 300, 500, 600, 700, 900, 1000, 1100]
SERVANT_LIST = [415, 835, 1225]
NP_LIST = [520, 820, 1120]
CARD_LIST = [215, 515, 815, 1115, 1415]
MASTER_LIST = [1150, 1250, 1350]


def get_screen(x, y, x2, y2):
    image = None
    try:
        gx, gy = game_grab(x, y)
        image = ImageGrab.grab(bbox=(gx, gy, gx+x2, gy+y2))
        image.save("recent.png")
    except Exception as e:
        lines = traceback.format_exception(type(e), e, e.__traceback__)
        print(''.join(lines))
    return image


def transform_image(image):
    thresh = 200
    fn = lambda x: 255 if x > thresh else 0
    return image.convert('L').point(fn, mode='1')


def game_grab(x, y):
    xSize = GAMEX2 - GAMEX
    ySize = GAMEY2 - GAMEY
    retX = x + GAMEX + 6
    retY = y + GAMEY
    return [retX, retY]


def click_on_screen(x, y, rest=0.0):
    print("Clicking: ", x, y)
    gx, gy = game_grab(x, y)
    pydirectinput.click(gx, gy)
    pyautogui.sleep(rest)


def use_skill(skill, servant=0, rest_time=0.0):
    print("Using skill: ", skill)
    skill_width = SKILL_LIST[skill-1]
    click_on_screen(skill_width, SKILL_HEIGHT, rest_time)
    if servant != 0:
        servant_width = SERVANT_LIST[servant-1]
        click_on_screen(servant_width, SERVANT_HEIGHT, 3)


def battle_card(card):
    card_width = CARD_LIST[card-1]
    click_on_screen(card_width, CARD_HEIGHT, 1)


def attack(np=0, np_duration=15):
    print("Attacking")
    click_on_screen(1400, 755, 2)
    if np != 0:
        use_np(np)
    else:
        battle_card(1)
    battle_card(2)
    battle_card(3)
    pyautogui.sleep(np_duration)


def use_np(servant):
    np_width = NP_LIST[servant-1]
    click_on_screen(np_width, NP_HEIGHT, 1)


def use_master_skill(master, servant, rest_time):
    master_width = MASTER_LIST[master-1]
    servant_width = SERVANT_LIST[servant-1]
    click_on_screen(MASTER_BUTTON[0], MASTER_BUTTON[1], 1)
    click_on_screen(master_width, MASTER_HEIGHT, 1)
    click_on_screen(servant_width, SERVANT_HEIGHT, rest_time)


def eat_apple():
    click_on_screen(830, 425, 2)
    click_on_screen(1065, 740, 2)


def regenerate_ap(ap):
    while True:
        pyautogui.sleep(5*60)
        ap = ap + 1
        print(ap)


def farm(ap, cost, apples):
    threading.Thread(target=regenerate_ap, args=(ap))
    while True:
        ap = ap - cost
        print(ap)
        click_on_screen(660, 385, 1)
        click_on_screen(1510, 888, 20)
        use_skill(3, rest_time=3)
        use_skill(7, 1, rest_time=3)
        attack(np=1, np_duration=25)
        use_skill(4, 1, rest_time=4)
        use_skill(6, rest_time=3)
        attack(np=1, np_duration=25)
        use_skill(9, 1, rest_time=3)
        use_skill(8, rest_time=3)
        use_skill(5, rest_time=3)
        use_master_skill(2, 1, 2)
        attack(np=1, np_duration=25)
        click_on_screen(250, 250, 1)
        click_on_screen(250, 250, 2)
        click_on_screen(1420, 880, 1)
        click_on_screen(1050, 750, 1)
        if ap < cost:
            if apples:
                eat_apple()
                ap = ap + 140
            else:
                sys.exit()
        pyautogui.sleep(10)


#5mins = 1 ap
if __name__ == '__main__':
    pyautogui.sleep(1)
    window = win32gui.GetForegroundWindow()
    GAMEX, GAMEY, GAMEX2, GAMEY2 = win32gui.GetWindowRect(window)
    ap = 82
    farm(ap, 40, False)

