from mh_script.client_manager.launcher import Launcher
from mh_script.handler.baotu_handler import BaoTu
from mh_script.handler.dati_handler import DaTi
from mh_script.handler.mijing_handler import MiJing
from mh_script.handler.yabiao_handler import YaBiao
from mh_script.utils.ocr_player import OCR_Player

if __name__ == "__main__":

    ocrPlayer = OCR_Player()
    pos = ocrPlayer.find_by_name_first(None,"微信",0.9,True)
    if pos:
        ocrPlayer.move(pos)



