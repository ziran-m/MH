from mh_script.client_manager.launcher import Launcher
from mh_script.handler.baotu_handler import BaoTu
from mh_script.utils.ocr_player import OCR_Player

l = Launcher()
regions = l.get_regions()


baotu = BaoTu(OCR_Player())
baotu.dig(regions[0])