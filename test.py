from mh_script.client_manager.launcher import Launcher
from mh_script.handler.basic_handler import BasicHandler
from mh_script.utils.ocr_player import OCR_Player

launcher = Launcher()
ocrPlayer = OCR_Player()


regions = launcher.get_regions()
# BasicHandler(ocrPlayer).escape_all(regions)
pos = ocrPlayer.find_by_pic_first(regions[0], "common.task",0.5)
# pos = ocrPlayer.find_by_pic_first(regions[1], "fuben.zhunbei",0.8)
ocrPlayer.move(pos)