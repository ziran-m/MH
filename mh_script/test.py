from mh_script.client_manager.launcher import Launcher
from mh_script.handler.baotu_handler import BaoTu
from mh_script.handler.dati_handler import DaTi
from mh_script.handler.mijing_handler import MiJing
from mh_script.handler.yabiao_handler import YaBiao
from mh_script.utils.ocr_player import OCR_Player

if __name__ == "__main__":
    launcher = Launcher()
    regions = launcher.get_regions()
    region = regions[0]

    ocrPlayer = OCR_Player()
    baotu = BaoTu(ocrPlayer)
    baotu.do(region)
    baotu.dig(region)
    mijing = MiJing(ocrPlayer)
    mijing.do(region)
    yabiao = YaBiao(ocrPlayer)
    yabiao.do(region)
    dati = DaTi(ocrPlayer)
    dati.do(region)
