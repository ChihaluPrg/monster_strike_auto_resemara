# Python - main.py
import time
import multiprocessing
import ADB
from Tap import process_tap

def run_on_device(device):
    # 各プロセス内で固有のデバイスIDを設定する
    ADB.device_id = device
    print(f"[INFO] {device} の処理を開始します。")
    time.sleep(1)
    process_tap()

if __name__ == "__main__":
    candidate_ports = list(range(5555, 6001))
    devices = ADB.scan_bluestacks_instances(candidate_ports)
    if not devices:
        print("[ERROR] 接続可能な BlueStacks インスタンスがありません。")
        exit(1)
    processes = []
    for device in devices:
        p = multiprocessing.Process(target=run_on_device, args=(device,))
        p.start()
        processes.append(p)
    for p in processes:
        p.join()