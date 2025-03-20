import cv2
import subprocess
import time
import os
from ADB import capture_screen, check_device_connected, adb_path,  device_id

# テンプレート画像を探す関数
def find_template_position(template_path, threshold=0.8):
    if not capture_screen():
        print("キャプチャに失敗しました。")
        return None
    screen = cv2.imread("screen.png")
    template = cv2.imread(template_path, 0)
    if screen is None or template is None:
        print("画像ファイルが見つかりません。パスを確認してください。")
        return None
    screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(screen_gray, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        # 画像中央の座標を計算
        template_height, template_width = template.shape[:2]
        center_x = max_loc[0] + template_width // 2
        center_y = max_loc[1] + template_height // 2
        return (center_x, center_y)  # 中央の座標を返す
    else:
        return None

# 実機上でタッチ操作を実行する関数
def tap_on_device(x, y):
    if not check_device_connected():
        return False
    # adbコマンドでタッチ操作を実行
    subprocess.run([adb_path, "-s", device_id, "shell", f"input tap {x} {y}"])
    return True

def tap_button_with_retry(template_path, wait_time=2):
    """
    ボタンが見つからない場合、見つかるまで再試行する関数
    """
    while True:
        position = find_template_position(template_path)
        if position:
            tap_on_device(position[0], position[1])
            time.sleep(1)  # 少し待機
            return True
        else:
            print(f"{template_path} が見つかりませんでした。再試行します...")
            time.sleep(wait_time)  # 再試行の前に待機

def tap_button_with_retry_restricted(template_path, wait_time=2, max_retries=3):
    """
    ボタンが見つからない場合、指定された回数まで再試行する関数。
    見つからない場合はスキップ。
    """
    retries = 0  # 試行回数をカウントする

    while retries < max_retries:
        position = find_template_position(template_path)
        if position:
            tap_on_device(position[0], position[1])
            time.sleep(1)  # 少し待機
            return True
        else:
            retries += 1
            print(f"{template_path} が見つかりませんでした。再試行します... (試行回数: {retries}/{max_retries})")
            time.sleep(wait_time)  # 再試行の前に待機

    print(f"{template_path} が見つからないため、スキップします。")
    return False


def tap_sequence_with_retry(sequence, max_retries=3, wait_time=2):
    """
    一連の画像ボタンを順番に検出してタップする。
    途中でボタンが見つからなければ終了。

    Args:
        sequence (list): 画像パスのリスト。順番に処理される。
        max_retries (int): 各画像の検出を試行する最大回数。
        wait_time (float): 再試行の間隔（秒）。

    Returns:
        bool: 全ての画像が正常にタップできた場合は True、失敗した場合は False。
    """
    for img_path in sequence:
        if not tap_button_with_retry_restricted(img_path, wait_time, max_retries):
            print(f"{img_path} が見つからないため、シーケンスを中断します。")
            return False
    return True


# スクロール操作を実行する関数
def scroll_on_device(start_x, start_y, end_x, end_y, duration=300):
    """
    start_x, start_y: スクロール開始の座標
    end_x, end_y: スクロール終了の座標
    duration: スクロールにかける時間（ミリ秒単位）
    """
    if not check_device_connected():
        return False
    # adbコマンドでドラッグ操作（スクロール）を実行
    subprocess.run(
        [adb_path, "-s", device_id, "shell", "input", "swipe", str(start_x), str(start_y), str(end_x), str(end_y),
         str(duration)])
    return True

