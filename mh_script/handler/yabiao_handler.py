import threading
from typing import List

from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log,global_log
from mh_script.utils.player import Player


class YaBiao:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)


    def do_all(self,regions:List[ScreenRegion]):
        global_log.info("[押镖] 开始执行押镖任务流程")
        threads = []

        # 对于每个区域，启动一个线程来执行 do
        for region in regions:
            t_do = threading.Thread(target=self.do, args=(region,))

            t_do.start()  # do任务
            threads.append(t_do)


        # 等待所有线程执行完毕
        for t in threads:
            t.join()

        global_log.info("[押镖] 所有任务执行完成")


    def do(self, region: ScreenRegion = None):
        log.info("[押镖] 开始执行押镖任务流程")
        self.delay()

        log.info("[押镖] 开始清理页面")
        self.basicHandler.clean(region)

        log.info("[押镖] 准备进入日常活动界面")
        self.basicHandler.goDailyActivity(region)

        log.info("[押镖] 查找“押镖.参加”按钮")
        pos = self.ocrPlayer.find_by_pic_first(region, "mijing.canjia", 0.9, True)
        if pos is None:
            pos = self.ocrPlayer.find_by_pic_first(region, "mijing.canjia_v2", 0.9, True)
            if pos is None:
                log.info("[押镖] 找不到参加按钮，可能任务已完成")
                self.basicHandler.clickCenter(region)
                return
        log.info(f"[押镖] 点击“参加”按钮：{pos}")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        log.info("[押镖] 再次清理页面")
        self.basicHandler.clean(region)

        log.info("[押镖] 等待“开始押镖”按钮出现")
        pos = self.ocrPlayer.wait_find_by_pic_first(region, "yabiao.start", 0.9)
        if pos is None:
            log.info("[押镖] 等待“开始押镖”按钮出现异常")
            return
        times = 1
        while True:
            log.info("[押镖] 等待“开始押镖”按钮出现")
            pos = self.ocrPlayer.wait_no_time_find_by_pic_first(region, "yabiao.start", 0.9)
            log.info(f"[押镖] 点击“开始押镖”：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            no_power = self.ocrPlayer.find_by_pic_first(region, "yabiao.no_power", 0.9)
            if no_power is not None:
                self.basicHandler.clickCenter(region)
                log.info("[押镖] 活力不足，任务中止")
                break

            pos = self.ocrPlayer.find_by_pic_first(region, "yabiao.queding", 0.9)
            log.info(f"[押镖] 点击“确定”：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
            times += 1
            if times >= 3:
                log.info("[押镖] 达到执行上限，检查是否仍在押镖或战斗中")
                while (self.basicHandler.battling(region) or
                       self.ocrPlayer.find_by_pic_first(region, "yabiao.doing") is not None):
                    log.info("[押镖] 正在押镖或战斗中，等待 30 秒")
                    self.delay(30, 30)
                break

        log.info("[押镖] 押镖任务完成")

    def delay(self, min_seconds=1.0, max_seconds=3.0):
        Player.delay(min_seconds,max_seconds)
