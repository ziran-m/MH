from typing import List

from mh_script.handler.fuben_handler import Fuben
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.ocr_player import OCR_Player


class DungeonTask:
    def __init__(self, regions: List[ScreenRegion]):
        """
        初始化副本任务
        :param regions: 客户端窗口的区域信息，包含窗口的大小、位置等
        """
        self.regions = regions  # 存储每个客户端的窗口信息
        self.ocrPlayer = OCR_Player()


    def run(self,idx):
        Fuben(self.ocrPlayer).do(self.regions[idx],False,0)
        print("✅ 所有副本任务完成！")