import subprocess
import time
import os
import socket

# ADB のパスとコマンド名（adb.exe のパスが必要な場合は adb_path を利用してください）
adb_path = r"C:\adb\platform-tools\adb.exe"
adb_command = "adb"

# 接続先の IP アドレス（必要に応じて変更）
ip_address = "192.168.0.100"
# device_id は後で自動取得したポート番号を設定します
device_id = None


def get_free_port():
    """空いているポート番号を取得する関数"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("", 0))  # ポート 0 を指定すると、OS が空いているポートを割り当てる
        return s.getsockname()[1]


def process_adb():
    # 空いているポート番号を自動取得
    free_port = get_free_port()
    print(f"自動取得したポート番号: {free_port}\n")

    # グローバル変数 device_id を更新（ADB の接続先指定に使用）
    global device_id
    device_id = f"{ip_address}:{free_port}"

    set_tcpip_mode_without_device_check(free_port)
    connect_device(ip_address, free_port)


def set_tcpip_mode_without_device_check(port):
    """直接TCP/IPモードに設定する関数"""
    try:
        # ADBサーバーを起動
        print("ADBサーバーを起動します\n")
        subprocess.run([adb_command, "start-server"], check=True)
        time.sleep(0.5)

        # TCP/IPモードを指定ポートで設定
        print(f"直接TCP/IPモードをポート {port} で設定します...\n")
        subprocess.run([adb_command, "tcpip", str(port)], check=True)
        time.sleep(0.5)
        print(f"\nポート {port} でTCP/IPモードに設定しました。\n")
        time.sleep(0.5)
    except subprocess.CalledProcessError:
        print("TCP/IP設定中にエラーが発生しました。adbのパスを確認してください。\n")
        time.sleep(0.5)


def connect_device(ip_address, port):
    """指定したIPアドレスとポートにADB接続を試みる関数"""
    try:
        print(f"{ip_address}:{port} に接続を試みます...\n")
        result = subprocess.run([adb_command, "connect", f"{ip_address}:{port}"],
                                capture_output=True, text=True)
        time.sleep(0.5)
        if "connected" in result.stdout:
            print(f"{ip_address} に接続されました。\n")
            time.sleep(0.5)
            return True
        else:
            print(f"{ip_address} に接続できませんでした。エラー: {result.stderr}\n")
            time.sleep(0.5)
            return False
    except subprocess.CalledProcessError:
        print("接続中にエラーが発生しました。\n")
        time.sleep(0.5)
        return False


def check_device_connected():
    """ADB経由でデバイスの接続を確認する関数"""
    result = subprocess.run([adb_path, "devices"], capture_output=True, text=True)
    if device_id not in result.stdout:
        print(f"デバイス {device_id} が見つかりません。adb devicesでIDを確認してください。\n")
        time.sleep(0.5)
        return False
    return True


def capture_screen():
    """ADB経由で画面キャプチャを取得する関数"""
    if not check_device_connected():
        return False
    # 画面キャプチャの保存先を指定
    subprocess.run([adb_path, "-s", device_id, "shell", "screencap", "-p", "/sdcard/screen.png"])
    subprocess.run([adb_path, "-s", device_id, "pull", "-q", "/sdcard/screen.png", "screen.png"])
    return os.path.exists("screen.png")


if __name__ == "__main__":
    process_adb()
