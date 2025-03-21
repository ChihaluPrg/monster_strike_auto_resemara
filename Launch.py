import subprocess
from ADB import check_device_connected, adb_path, device_id
from OpenCV2 import find_template_position, tap_on_device
import ADB
def launch_game():
    if check_device_connected():
        result = subprocess.run([ADB.adb_path, "-s", ADB.device_id, "shell", "monkey", "-p",
                                 "jp.co.mixi.monsterstrike", "-c", "android.intent.category.LAUNCHER", "1"],
                                capture_output=True, text=True)
        if result.returncode != 0:
            print("アプリの起動に失敗しました。\n")
            return False
        print("モンストを起動しました。\n")
        return True
    return False

def tap_template(template_path, description):
    position = find_template_position(template_path)
    if position:
        tap_on_device(position[0], position[1])
        print(f"{description}をタップしました。\n")
        return True
    return False  # 見つからなければ False を返す
