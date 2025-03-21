import sys
from OpenCV2 import find_template_position, tap_on_device, scroll_on_device
import mss
import mss.tools
import time

# 画像パスの定義
TITLE2_PATH       = "img/title2.png"
OSIRASE_PATH      = "img/osirase.png"
ROGUBO_PATH       = "img/rogubo.png"
ROGUSUTA1_PATH    = "img/rogusuta1.png"
ROGUSUTA2_PATH    = "img/rogusuta2.png"
PREZENT_PATH      = "img/purezento.png"
GACHA1_PATH       = "img/gacha1.png"
GACHA2_PATH       = "img/gacha2.png"
GACHA3_PATH       = "img/gacha3.png"
GACHA4_PATH       = "img/gacha4.png"
GACHA5_PATH       = "img/gacha5.png"
GACHA6_PATH       = "img/gacha6.png"
GACHA7_PATH       = "img/gacha7.png"
GACHA8_PATH       = "img/gacha8.png"
GACHA9_PATH       = "img/gacha9.png"
GACHA10_PATH      = "img/gacha10.png"
SAITOUROKU1_PATH  = "img/saitouroku1.png"
SAITOUROKU2_PATH  = "img/saitouroku2.png"
SAITOUROKU3_PATH  = "img/saitouroku3.png"
SAITOUROKU4_PATH  = "img/saitouroku4.png"
MASAMUNE_PATH     = "img/masamune.png"

# 任意のタップ座標
TITLE2_TAP_COORD       = (270, 780)
OSIRASE_TAP_COORD      = (273, 837)
ROGUBO_TAP_COORD       = (270, 684)
ROGUSUTA1_TAP_COORD    = (270, 620)
ROGUSUTA2_TAP_COORD    = (260, 840)
PREZENT_TAP_COORD      = (266, 660)
GACHA1_TAP_COORD       = (270, 780)
GACHA2_TAP_COORD       = (270, 640)
GACHA3_TAP_COORD       = (260, 790)
GACHA4_TAP_COORD       = (100, 815)
GACHA5_TAP_COORD       = (140, 670)
GACHA6_TAP_COORD       = (270, 690)
GACHA7_TAP_COORD       = (270, 780)
GACHA8_TAP_COORD       = (270, 690)
GACHA9_TAP_COORD       = (270, 690)
GACHA10_TAP_COORD      = (270, 280)
SAITOUROKU1_TAP_COORD  = (140, 700)
SAITOUROKU2_TAP_COORD  = (230, 830)
SAITOUROKU3_TAP_COORD  = (140, 830)
SAITOUROKU4_TAP_COORD  = (140, 675)
# ※ MASAMUNE 画像に対応するタップ座標（必要なら調整）
MASAMUNE_TAP_COORD     = (270, 500)  # 仮の座標例


def process_after_gacha9():
    """
    GACHA9検出後にMASAMUNE_PATHの存在をチェックし、
    両方検出されている場合は、タップ後「次の処理実行後にプログラム終了」を示す True を返す。
    """
    pos_masamune = find_template_position(MASAMUNE_PATH, threshold=0.5)
    if pos_masamune:
        print(f"[INFO] {MASAMUNE_PATH} も検出されました。")
        tap_on_device(*MASAMUNE_TAP_COORD)
        time.sleep(1)
        print("[INFO] 次の処理実行後にプログラムを終了します。")
        return True
    else:
        print(f"[INFO] {MASAMUNE_PATH} は検出されなかったため、通常の次の処理に移行します。")
        return False


def next_process():
    """
    GACHA10およびSAITOUROKU系の処理を実施する。
    """
    # GACHA10画像検出後、固定座標へタップ（最大5回試行）
    max_attempts = 5
    for attempt in range(1, max_attempts + 1):
        position = find_template_position(GACHA10_PATH, threshold=0.4)
        if position:
            print(f"[INFO] {GACHA10_PATH} が検出されました。（試行回数: {attempt}）")
            tap_on_device(*GACHA10_TAP_COORD)
            time.sleep(1)
            break
        else:
            print(f"[WARN] {GACHA10_PATH} が見つかりません。（試行回数: {attempt}）再試行します...")
            time.sleep(1)
    else:
        print(f"[ERROR] {max_attempts}回試行しましたが、{GACHA10_PATH} の検出に失敗しました。")

    # SAITOUROKU系の画像検出＋タップ処理
    for path, coord in [(SAITOUROKU1_PATH, SAITOUROKU1_TAP_COORD),
                        (SAITOUROKU2_PATH, SAITOUROKU2_TAP_COORD),
                        (SAITOUROKU3_PATH, SAITOUROKU3_TAP_COORD),
                        (SAITOUROKU4_PATH, SAITOUROKU4_TAP_COORD)]:
        while True:
            position = find_template_position(path, threshold=0.8)
            if position:
                print(f"[INFO] {path} が検出されました。")
                tap_on_device(*coord)
                time.sleep(1)
                break
            else:
                print(f"[WARN] {path} が見つかりません。再試行します...")
                time.sleep(1)


def process_tap():
    while True:
        # TITLE2画像検出後、固定座標へタップ
        while True:
            position = find_template_position(TITLE2_PATH)
            if position:
                print(f"[INFO] {TITLE2_PATH} が検出されました。")
                tap_on_device(*TITLE2_TAP_COORD)
                time.sleep(5)
                break
            else:
                print(f"[WARN] {TITLE2_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # ROGUBO画像検出後、固定座標へタップ
        while True:
            position = find_template_position(ROGUBO_PATH)
            if position:
                print(f"[INFO] {ROGUBO_PATH} が検出されました。")
                tap_on_device(*ROGUBO_TAP_COORD)
                time.sleep(5)
                break
            else:
                print(f"[WARN] {ROGUBO_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # ROGUSUTA1画像検出後、固定座標へタップ
        while True:
            position = find_template_position(ROGUSUTA1_PATH)
            if position:
                print(f"[INFO] {ROGUSUTA1_PATH} が検出されました。")
                tap_on_device(*ROGUSUTA1_TAP_COORD)
                time.sleep(3)
                break
            else:
                print(f"[WARN] {ROGUSUTA1_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # ROGUSUTA2画像検出後、固定座標へタップ
        while True:
            position = find_template_position(ROGUSUTA2_PATH)
            if position:
                print(f"[INFO] {ROGUSUTA2_PATH} が検出されました。")
                tap_on_device(*ROGUSUTA2_TAP_COORD)
                time.sleep(1)
                break
            else:
                print(f"[WARN] {ROGUSUTA2_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # PREZENT画像検出後、固定座標へタップ
        while True:
            position = find_template_position(PREZENT_PATH)
            if position:
                print(f"[INFO] {PREZENT_PATH} が検出されました。")
                tap_on_device(*PREZENT_TAP_COORD)
                time.sleep(1)
                break
            else:
                print(f"[WARN] {PREZENT_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # GACHA1画像検出後、固定座標へタップ
        while True:
            position = find_template_position(GACHA1_PATH)
            if position:
                print(f"[INFO] {GACHA1_PATH} が検出されました。")
                tap_on_device(*GACHA1_TAP_COORD)
                time.sleep(1)
                break
            else:
                print(f"[WARN] {GACHA1_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # GACHA2画像検出後、固定座標へタップ
        while True:
            position = find_template_position(GACHA2_PATH)
            if position:
                print(f"[INFO] {GACHA2_PATH} が検出されました。")
                tap_on_device(*GACHA2_TAP_COORD)
                time.sleep(1)
                break
            else:
                print(f"[WARN] {GACHA2_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # GACHA3画像検出後、固定座標へタップ
        while True:
            position = find_template_position(GACHA3_PATH)
            if position:
                print(f"[INFO] {GACHA3_PATH} が検出されました。")
                tap_on_device(*GACHA3_TAP_COORD)
                time.sleep(1)
                break
            else:
                print(f"[WARN] {GACHA3_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # GACHA4画像検出後、固定座標へタップ
        while True:
            position = find_template_position(GACHA4_PATH)
            if position:
                print(f"[INFO] {GACHA4_PATH} が検出されました。")
                tap_on_device(*GACHA4_TAP_COORD)
                time.sleep(1)
                break
            else:
                print(f"[WARN] {GACHA4_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # GACHA5画像検出後、固定座標へタップ
        while True:
            position = find_template_position(GACHA5_PATH)
            if position:
                print(f"[INFO] {GACHA5_PATH} が検出されました。")
                tap_on_device(*GACHA5_TAP_COORD)
                time.sleep(1)
                break
            else:
                print(f"[WARN] {GACHA5_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # GACHA6画像検出後、固定座標へタップ
        while True:
            position = find_template_position(GACHA6_PATH)
            if position:
                print(f"[INFO] {GACHA6_PATH} が検出されました。")
                tap_on_device(*GACHA6_TAP_COORD)
                time.sleep(3)
                break
            else:
                print(f"[WARN] {GACHA6_PATH} が見つかりません。再試行します...")
                time.sleep(1)

        # GACHA7画像検出後、スクロール処理＋再チェック
        attempt = 0
        while attempt < 10:
            position = find_template_position(GACHA7_PATH)
            if position:
                print(f"[INFO] {GACHA7_PATH} が検出されました。")
                scroll_on_device(270, 630, 270, 840, 300)
                time.sleep(5)  # スクロール後5秒待機
                # 再度検出チェック（画像が残っていれば再実行）
                if find_template_position(GACHA7_PATH):
                    print(f"[INFO] 5秒後も {GACHA7_PATH} が検出されているため、再度スクロール処理を実行します。")
                    attempt += 1
                    continue
                else:
                    print(f"[INFO] 5秒後に {GACHA7_PATH} の検出がなくなりました。")
                    break
            else:
                attempt += 1
                print(f"[WARN] {GACHA7_PATH} が見つかりません。再試行します... ({attempt}/10)")
                time.sleep(3)
        else:
            print(f"[WARN] {GACHA7_PATH} の検出に失敗したため、次の処理に進みます。")

        # GACHA8画像検出後、タップ（10回繰り返し、最大30回リトライ）
        MAX_RETRIES = 30
        for i in range(20):
            print(f"[INFO] 【{i + 1}回目】GACHA8 の検出処理を開始します。")
            retry_count = 0
            while retry_count < MAX_RETRIES:
                pos_gacha8 = find_template_position(GACHA8_PATH, threshold=0.3)
                pos_specified = find_template_position(MASAMUNE_PATH)  # 指定画像（MASAMUNE）
                if pos_gacha8 and pos_specified:
                    print(f"[INFO] {GACHA8_PATH} と {MASAMUNE_PATH} が検出されました。")
                    tap_on_device(*GACHA8_TAP_COORD)
                    time.sleep(1)
                    break
                elif pos_gacha8:
                    print(f"[INFO] {GACHA8_PATH} が検出されました。タップを実行します。")
                    tap_on_device(*GACHA8_TAP_COORD)
                    time.sleep(1)
                    break
                else:
                    retry_count += 1
                    print(f"[WARN] {GACHA8_PATH} が見つかりません。再試行します... ({retry_count}/{MAX_RETRIES})")
                    time.sleep(1)
            else:
                print(f"[WARN] 【{i + 1}回目】タイムアウトしました。次の処理に移ります。")
            time.sleep(3)

        # GACHA9の検出（最大5回試行）
        gacha9_detected = False
        attempt = 0
        while attempt < 15:
            pos_gacha9 = find_template_position(GACHA9_PATH, threshold=0.3)
            if pos_gacha9:
                print(f"[INFO] {GACHA9_PATH} が検出されました。（試行回数: {attempt + 1}）")
                tap_on_device(*GACHA9_TAP_COORD)
                time.sleep(1)
                gacha9_detected = True
                break
            else:
                attempt += 1
                print(f"[WARN] {GACHA9_PATH} が見つかりません。再試行します... ({attempt}/5)")
                time.sleep(1)
        if gacha9_detected:
            # GACHA9検出後にMASAMUNEの有無をチェック
            both_detected = process_after_gacha9()
        else:
            print("[WARN] GACHA9 の検出に失敗したため、次の処理に進みます。")
            both_detected = False

        # 次の処理（GACHA10、SAITOUROKU系の処理）
        next_process()

        # 両画像（GACHA9＆MASAMUNE）が検出されていた場合、次の処理後にプログラム終了
        if both_detected:
            print("[INFO] 両画像が検出されたため、処理を終了します。")
            return

        print("[INFO] １サイクル終了。次のサイクルを開始します。")
        time.sleep(1)
