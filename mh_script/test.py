from mh_script.handler.baotu_handler import BaoTu
from mh_script.model.screen_region import ScreenRegion
from mh_script.task_manager.daily_task import DailyTask
from mh_script.utils.ocr_player import OCR_Player
from mh_script.utils.player import Player







if __name__ == "__main__":
    # ocrPlayer = OCR_Player()
    # region = ScreenRegion(0, 0, 768, 600)
    # pos = ocrPlayer.find_by_pic_first(region, "baotu.canjia", 0.9, False)
    # Player.move(pos, False)
    regions=[]
    region = ScreenRegion(0, 0, 768, 600)
    regions.append(region)

    ocrPlayer = OCR_Player()

    # 宝图
    baotu = BaoTu(ocrPlayer)

    baotu.do(region)
