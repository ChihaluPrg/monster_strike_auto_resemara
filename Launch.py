import subprocess
import time
from ADB import check_device_connected, adb_path, device_id
from OpenCV2 import find_template_position, tap_on_device
from Update_apk import process_update, update_start
from Countdown import countdown

# 画像テンプレートのパス
DAILY_ROULETTE_TEMPLATE_PATH = "img/daily_roulette.jpg"
APOLOGY_TEMPLATE_PATH = "img/apology.jpg"
CLOSE_NEWS_TEMPLATE_PATH = "img/news_close.jpg"
CLOSE_MOVIE_TEMPLATE_PATH = "img/movie_close.jpg"
BOSS_WEAKNESSES_TEMPLATE_PATH = "img/boss_weaknesses.jpg"
BOSS_WEAKNESSES_OK_TEMPLATE_PATH = "img/boss_weaknesses_ok.jpg"
UPDATE_POPUP_PATH = "img/update_popup.jpg"
UPDATE_START_PATH = "img/update_start.jpg"
TOWN_BOUKEN_PARTY_PATH = "img/town_bouken_party.jpg"
QUEST_PATH = "img/quest_bouken3.jpg"

def process_launch():

    while True:
        # 白猫の起動とアプデの確認、更新
        launch_game()
        countdown(10)
        print("最新バージョンの更新の確認をします...")
        position = find_template_position(UPDATE_POPUP_PATH)
        if position:
            process_update()
            break
        else:
            print("更新は見つかりませんでした")
            break

    while True:
        if start():
            countdown(20)
            break
        else:
            countdown(10)
            break

    while True:
        position = find_template_position(QUEST_PATH)
        if position:
            return True
        else:
            break

    while True:
        # デイリールーレットのOKボタンをタップ
        if daily_roulette():
            print("デイリールーレットのOKボタンをタップしました")
            time.sleep(5)
            break
        else:
            print("デイリールーレットのOKボタンが表示されませんでした")
            time.sleep(1)
            break

    while True:
        # お詫びのOKボタンをタップ
        if apology():
            print("お詫びのOKボタンをタップしました")
            time.sleep(2)
            break
        else:
            print("お詫びのOKボタンのタップが表示されませんでした")
            time.sleep(1)
            break

    while True:
        # ボスの弱点変更
        if boss_weaknesses():
            print("BOSSの弱点変更画面をタップしました")
            time.sleep(2)
            break
        else:
            print("ボスの弱点変更画面が表示されませんでした")
            time.sleep(1)
            break

    while True:
        if boss_weaknesses_ok():
            print("BOSSの弱点変更ボタンをタップしました")
            time.sleep(2)
            break
        else:
            print("ボスの弱点変更ボタンが表示されませんでした")
            time.sleep(1)
            break

    while True:
        # ニュースのOKボタンをタップ
        position = find_template_position(BOSS_WEAKNESSES_TEMPLATE_PATH)
        if close_news():
            print("ニュースのOKボタンをタップしました")
            if position:
                time.sleep(2)
                return True
            else:
                countdown(35)
                break
        else:
            print("ニュースのOKボタンが表示されませんでした")
            time.sleep(2)
            break

    while True:
        # 動画画面を閉じる
        if movie_news():
            print("ムービーのOKボタンをタップしました")
            time.sleep(2)
            break
        else:
            print("ムービーのOKボタンが表示されませんでした")
            time.sleep(2)
            break

# 白猫プロジェクトを起動する
def launch_game():
    if check_device_connected():
        result = subprocess.run([adb_path, "-s", device_id, "shell", "monkey", "-p", "jp.colopl.wcat", "-c",
                                 "android.intent.category.LAUNCHER", "1"], capture_output=True, text=True)
        if result.returncode != 0:
            print("アプリの起動に失敗しました。\n")
            return False
        print("白猫プロジェクトを起動しました。\n")
        return True
    return False


# 共通のタップ処理関数
def tap_template(template_path, description):
    position = find_template_position(template_path)
    if position:
        tap_on_device(position[0], position[1])
        print(f"{description}をタップしました。\n")
        return True
    return False  # 見つからなければ何もせず、Falseを返す


# 各タップ関数
def daily_roulette():
    return tap_template(DAILY_ROULETTE_TEMPLATE_PATH, "デイリールーレットのOKボタン")

def apology():
    return tap_template(APOLOGY_TEMPLATE_PATH, "お詫びのOKボタン")

def boss_weaknesses():
    return tap_template(BOSS_WEAKNESSES_TEMPLATE_PATH, "ボスの弱点変更")

def boss_weaknesses_ok():
    return tap_template(BOSS_WEAKNESSES_OK_TEMPLATE_PATH, "ボスの弱点変更のOKボタン")

def close_news():
    return tap_template(CLOSE_NEWS_TEMPLATE_PATH, "ニュースの閉じるボタン")

def movie_news():
    return tap_template(CLOSE_MOVIE_TEMPLATE_PATH, "動画の閉じるボタン")

def start():
    while True:
        # アプデ後の起動
        position = find_template_position(UPDATE_START_PATH)
        if position:
            update_start()
            break
        else:
            break