import threading
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
        ocrPlayer = OCR_Player()

        # 宝图
        self.baotu = BaoTu(ocrPlayer)
        # 秘境
        self.mijing = MiJing(ocrPlayer)
        # 秘境
        self.yabiao = YaBiao(ocrPlayer)
        """
        初始化副本任务
        :param regions: 客户端窗口的区域信息，包含窗口的大小、位置等
        """
        self.regions = regions  # 存储每个客户端的窗口信息

    def run_tasks(self, region:ScreenRegion):
        # 执行具体的任务，这些任务会被放到线程中执行
        self.baotu.do(region)
        self.baotu.dig(region)
        self.mijing.do(region)
        self.yabiao.do(region)
    def run(self, idx):

        if idx == -1:
            threads = []
            for i in range(0, Constant.NUM_WINDOWS):
                # 创建线程来执行任务
                thread = threading.Thread(target=self.run_tasks, args=(self.regions[i],))
                threads.append(thread)
                thread.start()  # 启动线程

                # 等待所有线程完成
            for thread in threads:
                thread.join()

            print("✅ [任务完成] 所有窗口的任务执行完毕")
        else:
            self.baotu.do(self.regions[idx])
            self.baotu.dig(self.regions[idx])
            self.mijing.do(self.regions[idx])
            self.yabiao.do(self.regions[idx])
            print("✅ 所有日常任务完成！")

