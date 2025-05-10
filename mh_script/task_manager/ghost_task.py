from typing import List

from mh_script.handler.ghost_handler import Ghost
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.ocr_player import OCR_Player


class GhostTask:
    def __init__(self, regions: List[ScreenRegion]):
        """
        初始化抓鬼任务
        :param regions: 客户端窗口的区域信息，包含窗口的大小、位置等
        """
        self.regions = regions  # 存储每个客户端的窗口信息
        self.ocrPlayer = OCR_Player()


    def run(self,idx):
        Ghost(self.ocrPlayer).do(self.regions[idx])
        global_log.info("✅ 抓鬼任务完成！")