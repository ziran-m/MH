from basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.ocr_player import OCR_Player
from mh_script.utils.player import Player


class MiJing:
    def __init__(self):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = OCR_Player()
        self.basicHandler = BasicHandler()
    # 秘境
    def do(self, region: ScreenRegion = None):
        # 延迟
        self.delay()

        # 去到日常活动页面
        self.basicHandler.goDailyActivity(region)

        # 点击秘境的参加,坐标要微调下
        pos = self.ocrPlayer.find_by_pic(region, "mijing.mijing_canjia")
        # 找不到就是已经完成了
        if pos is None:
            print("任务已完成或找不到")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()



        return

    def delay(self,min_seconds=0.5, max_seconds=3.0):
        Player.delay()