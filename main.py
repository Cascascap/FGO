import os
import random
import time
from enum import Enum

import imagehash
import pyautogui
import pydirectinput
import pyscreenshot as ImageGrab
import traceback
from PIL import Image
import pygame
import pyperclip


class State(Enum):
    SELECT_SUPPORT = 1
    FIGHT = 2


imagesDir = os.path.dirname(__file__)
MASTER_BUTTON = [1500, 425]
SKILL_HEIGHT = 755
SERVANT_HEIGHT = 615
NP_HEIGHT = 300
CARD_HEIGHT = 650
MASTER_HEIGHT = 425
SKILL_LIST = [100, 200, 300, 500, 600, 700, 900, 1000, 1100]
SERVANT_CHANGE_LIST = [250, 500, 750, 1000, 1250, 1500]
SERVANT_LIST = [415, 835, 1225]
NP_LIST = [520, 820, 1120]
CARD_LIST = [215, 515, 815, 1115, 1415]
MASTER_LIST = [1150, 1250, 1350]
GAME_X = 0
GAME_Y = 0
GAME_X2 = 0
GAME_Y2 = 0
STATE = State.SELECT_SUPPORT
ASSIST_URL = "https://game.granbluefantasy.jp/#quest/assist"
RAID_URL = "https://game.granbluefantasy.jp/#quest/supporter/903471/1"
global NEED_BERRY


def compare_images_for_result(image: str, image2: Image):
    path = os.path.join(imagesDir, './images/' + image)
    hash0 = imagehash.average_hash(transform_image(image2))
    hash1 = imagehash.average_hash(transform_image(Image.open(path)))
    cutoff = hash0 - hash1  # maximum bits that could be different between the hashes.
    return cutoff


def compare_images2(image: str, screenshot: Image):
    path = os.path.join(imagesDir + "/images/" + image+".png")
    hash0 = imagehash.average_hash(screenshot)
    hash1 = imagehash.average_hash(Image.open(path))
    cutoff = 8  # maximum bits that could be different between the hashes.
    if cutoff > hash0 - hash1:
        return True
    else:
        return False


def compare_images(image: str, resistance: int, ix, iy, isx, isy):
    screenshot = get_screen(ix, iy, isx, isy)
    path = os.path.join(imagesDir, './images/' + image)
    hash0 = imagehash.average_hash(screenshot)
    hash1 = imagehash.average_hash(Image.open(path))
    cutoff = hash0 - hash1  # maximum bits that could be different between the hashes.
    if cutoff < resistance:
        return True
    else:
        return False


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
    #xSize = GAME_X2 - GAME_X
    #ySize = GAME_Y2 - GAME_Y
    retX = x + GAME_X + 6
    retY = y + GAME_Y
    return [retX, retY]


def click_on_screen(x, y, rest=0.0):
    print("Clicking: ", x, y)
    gx, gy = game_grab(x, y)
    pydirectinput.click(gx, gy)
    pyautogui.sleep(rest)


def join_fight(element):
    if element == "kaguya":
        if click_when_found('images/kaguya.png', 0) or click_when_found('images/kaguya2.png', 0):
            pyautogui.sleep(0)
        else:
            click_gbf(300, 530, 0, True)
        wait_for_image("ok_accept_summon.png", click=True)
    if element == "fire":
        if not click_when_found('images/shiva.png', 3):
            if not click_when_found('images/shivaname.png', 3):
                if not click_when_found('images/colossus.png', 3):
                    pydirectinput.click(200, 500)
                    pyautogui.sleep(2)
    if element == "dark":
        if not click_when_found('images/bahamut.png', 3):
            if not click_when_found('images/celeste.png', 3):
                pydirectinput.click(200, 500)
                pyautogui.sleep(2)
    if element == "light":
        box = pyautogui.locateOnScreen('images/lucifer.png')
        if box is not None:
            pydirectinput.click(box[0], box[1])
            pyautogui.sleep(2)
        else:
            box = pyautogui.locateOnScreen('images/luminera.png')
            if box is not None:
                pydirectinput.click(box[0], box[1])
                pyautogui.sleep(2)
            else:
                pydirectinput.click(200, 500)
                pyautogui.sleep(2)
    click_when_found('images/oksummon.png', 0) or click_when_found('images/oksummon2.png', 0)
    if element != "kaguya":
        pyautogui.sleep(6)


def get_captcha():
    x = 190
    y = 591# + 70
    length = 195
    height = 75
    screenshot = pyautogui.screenshot(region=(x, y, length, height))
    screenshot.save('captcha.png')


def hold_gbf(x, y, hold=0.0):
    random_float = random.uniform(0.05, 0.1)
    pyautogui.moveTo(x, y, random_float)
    pyautogui.mouseDown()
    pyautogui.sleep(hold)
    pyautogui.mouseUp()


def click_gbf(x, y, rest_time, optimized=False):
    if optimized:
        random_float = random.uniform(0.05, 0.1)
        pyautogui.moveTo(x, y, random_float)
        pydirectinput.click(x, y)
    else:
        random_float = random.uniform(0.10, 0.25)
        random_rest = random.uniform(0.15, 0.2)
        pyautogui.moveTo(x, y, random_float)
        pydirectinput.click(x, y)
        pyautogui.sleep(rest_time + random_rest)


def skill1(wait=0):
    click_gbf(205, 665, 0.2 + wait)


def nextCharRight(wait=0):
    click_gbf(510, 625, 0.2+wait)


def nextCharLeft(wait=0):
    click_gbf(74, 650, 0.2+wait)


def openChar1(wait=0):
    click_gbf(100, 625, 0.1 + wait)


def skill2(wait=0):
    click_gbf(290, 665, 0.1 + wait)


def skill3(wait=0.0):
    click_gbf(370, 665, 0.1 + wait)


def skill4(wait=0.0):
    click_gbf(460, 665, 0.1 + wait)


def attackButton(wait=0):
    attack_once()
    pyautogui.sleep(wait)


def fullAutoButton():
    click_gbf(93, 500, 0)


def backButton():
    click_gbf(95, 1005, 1)


def grand_order_fight():
    openChar1()
    nextCharRight()  # For Fediel
    nextCharRight()
    skill3()
    nextCharRight()
    skill2()


def fediel_fight():
    if click_when_found('images/strike_time.png', 0, False):
        pyautogui.sleep(0)
    else:
        openChar1()
        skill1()
        skill2()
        nextCharLeft() #For Fediel
        skill3()


def fight_raid(auto=True, otk=False):
    #grand_order_fight()
    #fediel_fight()
    if otk:
        openChar1()
        skill1()
        skill2()
    if auto:
        attackButton(1)
        fullAutoButton()
    else:
        attackButton(6)
        backButton()


def back_button():
    click_gbf(120, 470, 0, False)

def fight(auto: bool, has_drops=False, otk=False, request_help=False):
    if has_drops:
        click_when_found('images/ok_drops.png', 4)
    pyautogui.sleep(4)
    if otk:
        openChar1()
        skill1()
        skill2()
    if auto:
        openChar1()
        nextCharRight()
        skill3()
        nextCharRight()
        nextCharRight()
        skill2()
        back_button()
        use_summon()
        attackButton(1)
        fullAutoButton()
    if otk:
        attackButton(4)
        backButton()
    if request_help:
        request_backup()


def request_backup():
    click_when_found('images/backup.png', 2)
    click_when_found('images/backup2.png', 2)
    click_when_found('images/backup_ok.png', 2)


def one_hko_dark(auto: bool):
    openChar1()
    skill1()
    skill2()
    nextCharLeft()
    skill3()
    if auto:
        attackButton(6)
        backButton()
    else:
        attackButton(1)
        fullAutoButton()


def click_when_found(path, wait=0, click=True):
    random_float = random.randint(1, 5)
    random_float2 = random.randint(1, 5)
    random_rest = random.uniform(0.1, 0.5)
    box = pyautogui.locateOnScreen(path, confidence=0.9, grayscale=True)

    if box is not None:
        if click:
            x, y = box.left + random_float, box.top + random_float2
            pyautogui.moveTo(x, y)
            pyautogui.click(x, y)
            pyautogui.sleep(wait + random_rest)
        return True
    return False


def leave_death_screen():
    click_gbf(470, 495, 5)
    click_when_found('images/cancel.png', 4)
    click_when_found('images/cancel.png', 4)
    click_when_found('images/close2.png', 2)


def fight_next():
    click_when_found('images/ok.png', 2)
    join_fight("dark")
    click_when_found('images/elemental_damage_ok.png', 8)
    fight(auto=True, has_drops=False, otk=False, request_help=True)


def use_summon():
    click_when_found('images/use_summon.png', 1)
    click_gbf(110, 600, 0, False)
    click_when_found('images/ok_use_summon.png', 6)



def back_to_fight(unlocks_fight=False, repeat=True):
    start = time.time()
    timer_multiplier = 1
    while True:
        if unlocks_fight:
            if click_when_found('images/playNext.png', 3):
                fight_next()
                continue
        #if click_when_found('images/attack.png', 1):
            #continue
        if click_when_found('images/nextDef.png', 0) or click_when_found('images/next3.png', 0):
            pyautogui.sleep(4)
            continue
        if click_when_found('images/ok.png', 2) or click_when_found('images/okdrops.png', 2):
            continue
        if click_when_found('images/close.png', 2) or click_when_found('images/close2.png', 2):
            continue
        if click_when_found('images/elixir.png', 3):
            continue
        if click_when_found('images/full.png', 3):
            continue
        if click_when_found('images/mastery.png', 3):
            continue
        if click_when_found('images/summon.png'):
            return
        if click_when_found('images/quests.png', 5):
            return
        if click_when_found('images/quests2.png', 5):
            return
        if click_when_found('images/cancel2.png', 1):
            return
        if click_when_found('images/webok.png', 5):
            return
        if click_when_found('images/rejoin.png', 0, False):
            return
        if click_when_found('images/deathicon.png', 1):
            leave_death_screen()
            continue
        if check_for_captcha():
            play_alarm()
            return
        if time.time() - start > 180 * timer_multiplier:
            if timer_multiplier > 3:
                return
            else:
                timer_multiplier = refresh_and_attack(timer_multiplier)
        if repeat:
            if click_when_found('images/playagain.png', 3):
                continue
        else:
            if click_when_found('images/event_home.png', 3):
                return


def refresh_and_attack(timer_multiplier):
    timer_multiplier = timer_multiplier + 1
    pyautogui.hotkey('F5')
    pyautogui.sleep(5)
    if click_when_found('images/attack.png', 1):
        attack_once()
        fullAutoButton()
    return timer_multiplier


def attack_once():
    attack_button = None
    while attack_button is None:
        attack_button = click_when_found('images/attack.png', 1)
        if not attack_button:
            click_gbf(380, 465, 1)


def grind(auto: bool, element, has_drops=False, coop=False, otk=False, unlocks_fight=False, rise_of_the_beasts=False, repeat=True):
    while True:
        if check_for_captcha():
            play_alarm()
        if rise_of_the_beasts:
            if click_when_found('images/rise_of_the_beasts_menu.png', 0, False):
                click_gbf(300, 840, 3) #click battle the beasts
                click_when_found('images/rise_of_the_beasts_bonus.png', 4, True)
        if coop:
            wait_for_image("inroom.png", False)
            start_coop_fight(4)
        else:
            join_fight(element)
        fight(auto, has_drops, otk)
        if coop:
            if click_when_found('images/room.png', 3):
                continue
        else:
            back_to_fight(unlocks_fight, repeat=repeat)


def start_coop_fight(wait=0.0):
    click_gbf(464, 720, 0+wait)


def delete_raid_id_code():
    click_gbf(200, 590, 0)
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('delete')


def wait_for_image(image, click=False):
    start = time.time()
    got_image = False
    while got_image is False:
        got_image = click_when_found('images/' + image, 0, click)
        if check_for_captcha():
            play_alarm()
        if click_when_found('images/pending_battles_button.png', 0, False):
            go_back_to_raid_code()
        if time.time() - start > 60:
            return


def check_if_raid_already_ended(image):
    pyautogui.sleep(1)
    return click_when_found('images/' + image, 0, True)


def go_back_to_raid_code():
    click_gbf(300, 50, 0, True)
    pyperclip.copy(ASSIST_URL)
    pyautogui.hotkey('ctrl', 'v')
    pyautogui.hotkey('enter')
    pyautogui.sleep(1)
    wait_for_image("enterid.png", True)


def wait_for_new_raid(param):
    current_copy = param
    while current_copy == param:
        current_copy = pyperclip.paste()


def join_raid_wait_for_new(element="kaguya", optimized=False):
    successfully_joined = False
    while successfully_joined is False:
        go_back_to_raid_code()
        if check_for_captcha():
            play_alarm()
        pyperclip.copy("beforeAnima")
        click_gbf(360, 15, 0, optimized)
        wait_for_new_raid(pyperclip.paste())
        click_gbf(110, 15, 0, optimized)
        click_gbf(200, 590, 0, optimized)
        pyautogui.hotkey('ctrl', 'v')
        click_gbf(385, 590, 0, False)
        pyautogui.sleep(3)
        # If too many pending battles
        successfully_joined = not click_when_found('images/pending_battles.png', 0, False)
        if not successfully_joined:
            click_when_found('images/ok.png', 1)
            pyautogui.sleep(3)
            clean_pending_battles()
            go_back_to_raid_code()
            continue
        # If already in 3 fights
        successfully_joined = not click_when_found('images/maxbackup.png', 0, False)
        if not successfully_joined:
            click_when_found('images/ok.png', 1)
            delete_raid_id_code()
            pyautogui.sleep(30)
            continue
        click_when_found("images/ok_berry.png", 0, True)
        pyautogui.sleep(1)
        successfully_joined = not click_when_found("images/ok_raid_ended.png", 0, True)
        if not successfully_joined:
            delete_raid_id_code()
            continue
        wait_for_image("choose_summon.png")
        join_fight(element)
        if check_if_raid_already_ended("ok_raid_ended.png"):
            go_back_to_raid_code()
            successfully_joined = False
            continue
        else:
            successfully_joined = True


def clean_pending_battles():
    pending = True
    while pending:
        pending = click_when_found('images/pending_anima.png', 3)
        if not pending:
            return
        else:
            click_when_found('images/ok.png', 2)
            click_when_found('images/pending_battles_button.png', 2)


#Assumes Chrome in full screen and gbf.life in second tab
def join_raid(element="light", optimized=False):
    successfully_joined = False
    while successfully_joined is False:
        previous_code = pyperclip.paste()
        click_gbf(360, 15, 0, optimized)
        click_gbf(235, 615, 0, optimized)
        click_gbf(110, 15, 0, optimized)
        if previous_code == pyperclip.paste(): #If it didnt copy a code, there's no more raids to farm
            pyautogui.sleep(300)
        click_gbf(200, 590, 0, optimized)
        pyautogui.hotkey('ctrl', 'v')
        click_gbf(385, 590, 3, optimized)
        #If room wasnt found you need to close the announcement
        click_when_found('images/ok.png', 1)
        #If have to recover EP
        click_when_found('images/ok.png', 3)
        successfully_joined = not click_when_found('images/joinroom.png', 4, False)
        if not successfully_joined:
            delete_raid_id_code()
    join_fight(element)


def back_to_raid_id_from_quests_menu():
    click_gbf(440, 550, 5)
    click_gbf(450, 330, 0)


def restore_ep_in_menu():
    click_gbf(350, 665, 1.2)
    click_gbf(453, 666, 0.5)
    hold_gbf(473, 610, 1.5)
    click_gbf(414, 623, 1)
    click_gbf(392, 724, 2)
    click_when_found("images/ok_raid_ended.png", 0, True)


def grind_raid(element="kaguya"):
    while True:
        join_raid_wait_for_new(element, optimized=True)
        wait_for_image("attack.png")
        #treasure_hunt()
        fight_raid(otk=False)
        back_to_fight()
        '''
        back_to_fight()
        if NEED_BERRY:
            click_gbf(80, 120, 5)
            restore_ep_in_menu()
        go_back_to_raid_code()
        '''


def treasure_hunt(auto=False):
    openChar1()
    skill3(0.2)
    skill4(0.2)
    if auto:
        attackButton(1)
        fullAutoButton()
    else:
        pyautogui.sleep(3)
        go_back_to_raid_code()


def play_alarm():
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("alarm.mp3")
    pygame.mixer.music.play(-1)
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)


#captcha every 4 hours
def check_for_captcha():
    return click_when_found('images/captcha.png', 0, click=False)


if __name__ == '__main__':
    pydirectinput.FAILSAFE = False
    pyautogui.FAILSAFE = False
    try:
        grind(auto=True, element="dark", has_drops=False, coop=False, otk=False, unlocks_fight=False, rise_of_the_beasts=False)
        #grind_raid("fire")
    except KeyboardInterrupt:
        print("Program interrupted by user. Exiting...")

