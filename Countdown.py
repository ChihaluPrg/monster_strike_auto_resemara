import time


def countdown(seconds):
    print("処理待機中...")
    for i in range(seconds, 0, -1):  # 秒数から1秒ずつ減らしていく
        print(f"{i}...")  # カウントダウンを表示
        time.sleep(1)  # 1秒待つ