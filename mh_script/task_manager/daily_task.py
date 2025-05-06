from typing import List
import pyautogui

from mh_script.handler.mijing_handler import MiJing
from mh_script.handler.yabiao_handler import YaBiao
from mh_script.model.screen_region import ScreenRegion
from mh_script.handler.baotu_handler import BaoTu
from mh_script.constant.constant import Constant
from mh_script.utils.ocr_player import OCR_Player


class DailyTask:
    def __init__(self, regions: List[ScreenRegion]):
        """
        初始化副本任务
        :param regions: 客户端窗口的区域信息，包含窗口的大小、位置等
        """
        self.regions = regions  # 存储每个客户端的窗口信息

    def run(self, idx):
        ocrPlayer = OCR_Player()


        # 宝图
        baotu = BaoTu(ocrPlayer)
        # 秘境
        mijing = MiJing(ocrPlayer)
        # 秘境
        yabiao = YaBiao(ocrPlayer)
        if idx == -1:
            for i in range(0, Constant.NUM_WINDOWS):
                baotu.do(self.regions[i])
                baotu.dig(self.regions[i])
                mijing.do(self.regions[i])
                yabiao.do(self.regions[i])
        else:
            baotu.do(self.regions[idx])
            baotu.dig(self.regions[idx])
            mijing.do(self.regions[idx])
            yabiao.do(self.regions[idx])

        print("✅ 所有日常任务完成！")
