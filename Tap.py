from Print import ERROR_MESSAGE
from OpenCV2 import *

TOWN_PATH = "img/town.jpg"
GO_TWON_PATH = "img/go_town.jpg"
GET_TOWN_PATH = "img/get_town.jpg"
TOWN_OK_PATH = "img/town_ok.jpg"

def process_town():
    while True:
        position = find_template_position(TOWN_PATH)
        if position:
            tap_on_device(position[0], position[1])
            time.sleep(1)
            break
        else:
            print("タウンボタン" + ERROR_MESSAGE)

    while True:
        position = find_template_position(GO_TWON_PATH)
        if position:
            tap_on_device(position[0], position[1])
            time.sleep(15)
            break
        else:
            print("タウンへ行くボタン" + ERROR_MESSAGE)

    while True:
        position = find_template_position(GET_TOWN_PATH)
        if position:
            tap_on_device(position[0], position[1])
            time.sleep(3)
            break
        else:
            print("全回収ボタン" + ERROR_MESSAGE)


    while True:
        position = find_template_position(TOWN_OK_PATH)
        if position:
            tap_on_device(position[0], position[1])
            break
        else:
            print("すでに回収済みか、OKボタンが見つかりませんでした。")
            break