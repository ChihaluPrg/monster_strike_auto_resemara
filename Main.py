from QuestMovement import *
from Gacha import *
from Quest import *
from Launch import *
from ADB import *
from Mission_Receive import *
from Present import *
from Town import *
from Scratch import *

if __name__ == "__main__":
    process_adb()
    time.sleep(1)

    process_bouken()
    time.sleep(2)

    process_quest()
    time.sleep(2)

    process_scratch()

    # 無料ガチャを回す
    process_gacha_all()
    time.sleep(1)

    process_town()
    time.sleep(1)

















