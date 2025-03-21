import cv2
import subprocess
import time
import os
import ADB



def find_template_position(template_path, threshold=0.6):
    """
    テンプレート画像（template_path）の位置を、現在の画面キャプチャ上から探し、
    マッチした位置（画像中央: (x, y)）を返します。
    """
    if not ADB.capture_screen():
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
        # テンプレートの中央座標を計算
        template_height, template_width = template.shape[:2]
        center_x = max_loc[0] + template_width // 2
        center_y = max_loc[1] + template_height // 2
        return (center_x, center_y)
    else:
        print(f"[INFO] テンプレートの類似度が閾値（{threshold}）に達していません。（max_val: {max_val}）")
        return None


def tap_on_device(x, y):
    if not ADB.check_device_connected():
        return False
    command = [
        ADB.adb_path,
        "-s",
        ADB.device_id,
        "shell",
        "input",
        "swipe",
        str(x),
        str(y),
        str(x),
        str(y),
        "100"  # 100ミリ秒でスワイプ（タップをエミュレート）
    ]
    subprocess.run(command)
    print(f"[INFO] 座標 ({x}, {y}) に swipe(タップエミュレート) を実行しました。")
    return True



def tap_button_with_retry(template_path, wait_time=2):
    """
    指定のテンプレート画像を探し、見つかるまで無限に再試行しタップします。
    """
    while True:
        position = find_template_position(template_path)
        if position:
            tap_on_device(position[0], position[1])
            time.sleep(1)
            return True
        else:
            print(f"[INFO] {template_path} が見つかりませんでした。再試行します...")
            time.sleep(wait_time)


def tap_button_with_retry_restricted(template_path, wait_time=2, max_retries=3):
    """
    指定のテンプレート画像を探し、最大試行回数内で再試行しタップを試みます。
    見つからなければ False を返します。
    """
    retries = 0
    while retries < max_retries:
        position = find_template_position(template_path)
        if position:
            tap_on_device(position[0], position[1])
            time.sleep(1)
            return True
        else:
            retries += 1
            print(f"[INFO] {template_path} が見つかりませんでした。（試行回数: {retries}/{max_retries}）")
            time.sleep(wait_time)
    print(f"[INFO] {template_path} が見つからなかったためスキップします。")
    return False


def tap_sequence_with_retry(sequence, max_retries=3, wait_time=2):
    """
    複数の画像パス（sequence）を順番に検出し、全てタップできれば True を返します。
    途中の画像が見つからなければシーケンス処理を中断し False を返します。
    """
    for img_path in sequence:
        if not tap_button_with_retry_restricted(img_path, wait_time, max_retries):
            print(f"[ERROR] {img_path} が見つからなかったためシーケンスを中断します。")
            return False
    return True


def scroll_on_device(start_x, start_y, end_x, end_y, duration=300):
    if not ADB.check_device_connected():
        return False
    subprocess.run([ADB.adb_path, "-s", ADB.device_id, "shell", "input", "swipe",
                    str(start_x), str(start_y), str(end_x), str(end_y), str(duration)])
    print(f"[INFO] 座標 ({start_x}, {start_y}) から ({end_x}, {end_y}) へのスクロールを実行しました。")
    return True

