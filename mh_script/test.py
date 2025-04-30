from mh_script.client_manager.launcher import Launcher
from mh_script.handler.baotu_handler import BaoTu
from mh_script.utils.ocr_player import OCR_Player
from mh_script.utils.player import Player
l = Launcher()
regions = l.get_regions()
ocrPlayer = OCR_Player()
pos = ocrPlayer.find_by_pic_first(regions[0], "baotu.start",0.9,False)

Player.move(pos,False)

#
#
# baotu = BaoTu(ocrPlayer)
# baotu.do(regions[0])