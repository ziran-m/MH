from mh_script.client_manager.launcher import Launcher
from mh_script.handler.basic_handler import BasicHandler
from mh_script.utils.ocr_player import OCR_Player

launcher = Launcher()
ocrPlayer = OCR_Player()


regions = launcher.get_regions()
pos = BasicHandler(ocrPlayer).smart_find_bag_pic_with_scroll(regions[4], "baotu.canjia", "baotu.canjia_v2", 0.9, False,
                                                         BasicHandler(ocrPlayer).get_center(regions[4]))
# pos = ocrPlayer.find_by_pic_first(regions[1], "fuben.zhunbei",0.8)
ocrPlayer.move(pos)