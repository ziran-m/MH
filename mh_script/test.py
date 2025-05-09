from mh_script.client_manager.launcher import Launcher
from mh_script.utils.ocr_player import OCR_Player

launcher = Launcher()
ocrPlayer = OCR_Player()
regions = launcher.get_regions()
pos = ocrPlayer.find_by_pic_first(regions[0], "fuben.talk",0.8)
ocrPlayer.move(pos)