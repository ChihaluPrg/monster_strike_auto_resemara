import subprocess
import time
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

adb_path = r"C:\adb\adb.exe"
adb_command = "adb"
device_id = None

def connect_bluestacks_instance(port):
    device = f"127.0.0.1:{port}"
    print(f"[INFO] {device} への接続を試みます...")
    result = subprocess.run([adb_command, "connect", device],
                            capture_output=True, text=True)
    time.sleep(0.5)
    if "connected" in result.stdout.lower():
        print(f"[SUCCESS] {device} に接続されました。\n")
        return device
    else:
        print(f"[WARN] {device} への接続に失敗しました。エラー: {result.stderr.strip()}\n")
        return None

def scan_bluestacks_instances(candidate_ports=list(range(5555, 6001))):
    connected_devices = []
    with ThreadPoolExecutor(max_workers=100) as executor:
        future_to_port = {executor.submit(connect_bluestacks_instance, port): port for port in candidate_ports}
        for future in as_completed(future_to_port):
            device = future.result()
            if device is not None:
                connected_devices.append(device)
    return connected_devices

def process_adb():
    global device_id
    candidate_ports = list(range(5555, 6001))
    devices = scan_bluestacks_instances(candidate_ports)
    if not devices:
        print("[ERROR] 接続可能な BlueStacks インスタンスが見つかりませんでした。")
        return None
    else:
        print("【接続された BlueStacks インスタンス】")
        for dev in devices:
            print(f" - {dev}")
        device_id = devices[0]
        return device_id

def check_device_connected():
    global device_id
    result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
    if device_id not in result.stdout:
        print(f"[WARN] デバイス {device_id} が一覧に存在しません。")
        return False
    return True

def safe_remove(file_path):
    """
    ファイル削除時にエラーが発生しないようにするための例外処理付きの関数
    """
    try:
        os.remove(file_path)
        print()
    except FileNotFoundError:
        # ファイルが存在しなくてもエラーとせず、ログに記録するだけにする
        print()
    except PermissionError:
        # 権限エラーの場合、リトライ処理などを追加することも可能
        print()
    except Exception as e:
        # その他の予期しない例外もキャッチしてログ出力する
        print()


def capture_screen():
    global device_id
    if not check_device_connected():
        return False

    # 既存の screen.png を安全に削除
    safe_remove("screen.png")

    # デバイス上に画面キャプチャを保存
    subprocess.run([adb_path, "-s", device_id, "shell", "screencap", "-p", "/sdcard/screen.png"])
    time.sleep(1)
    # キャプチャ画像を PC に pull
    subprocess.run([adb_path, "-s", device_id, "pull", "-q", "/sdcard/screen.png", "screen.png"])
    time.sleep(1)
    if os.path.exists("screen.png") and os.path.getsize("screen.png") > 0:
        print("[INFO] 画面キャプチャを取得しました。")
        return True
    else:
        print("[ERROR] 画面キャプチャの取得に失敗しました。")
        return False
