import os

from PIL import ImageGrab
import cv2 as cv
import numpy as np
from PIL import Image

import main


imagesDir = os.path.dirname(__file__)
SERVANT_CARD_LIST = [72, 391, 710, 1029, 1348]
SERVANT_CARD_HEIGHT = 552
SERVANT_CARD_SIZE = 187, 250
FULL_GAME_SCREEN = (0, 30, 1640, 950)


def test():
    img = ImageGrab.grab(bbox=FULL_GAME_SCREEN)
    img_rgb = np.asarray(img)
    img_gray = cv.cvtColor(img_rgb, cv.COLOR_BGR2GRAY)
    template = cv.imread('images/supportSelect.png', 0)
    w, h = template.shape[::-1]
    res = cv.matchTemplate(img_gray, template, cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    for pt in zip(*loc[::-1]):
        cv.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    cv.imwrite('res.png', img_rgb)
    get_attacker_card()


def day_reset():
    return main.compare_images("dayReset.png", 4, 630, 707, 370, 130)


def needs_apple():
    needsApple = main.compare_images("needApple.png", 3, 627, 79, 400, 80)
    if not needsApple:
        return main.compare_images("needAppleb.png", 3, 627, 79, 400, 80)


def is_support_select():
    return main.compare_images("supportSelect.png", 2, 1155, 42, 440, 70)


def is_confirm_party():
    return main.compare_images("confirmParty.png", 2, 1165, 42, 440, 70)


def get_attacker_card():
    results = []
    index = 1
    for sc in SERVANT_CARD_LIST:
        servant = main.get_screen(sc, SERVANT_CARD_HEIGHT, SERVANT_CARD_SIZE[0], SERVANT_CARD_SIZE[1])
        dif = main.compare_images_for_result("card1.png", servant)
        dif2 = main.compare_images_for_result("card2.png", servant)
        if dif2 < dif:
            dif = dif2
        results.append((dif, index))
        servant.save("servant" + str(index) + ".png")
        print(dif)
        index = index + 1
    sorted_results = sorted(results, key=lambda elem: elem[0])
    return sorted_results[0][1], sorted_results[1][1], sorted_results[2][1]


def in_fight():
    screenshot = main.get_screen(1500, 39, 92, 27)
    return main.compare_images2("inFight", screenshot)
