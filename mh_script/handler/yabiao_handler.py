import threading
from typing import List
import random

from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log, global_log
from mh_script.utils.player import Player


class YaBiao:
    def __init__(self, ocrPlayer):
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    def do_all(self, regions: List[ScreenRegion]):
        global_log.info("🚀 [押镖] 开始任务")
        threads = []
        for region in regions:
            t = threading.Thread(target=self.do, args=(region,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        global_log.info("✅ [押镖] 全部完成")


    def do(self, region: ScreenRegion = None):
        log.info("🚀 [押镖] 开始")
        self.delay()

        self.basicHandler.clean(region)
        log.info("📅 [押镖]进入日常活动")

        self.basicHandler.goDailyActivity(region)

        log.info("🔍 [押镖]查找“参加”按钮")
        pos = self.basicHandler.smart_find_pic_with_scroll(region, "yabiao.canjia", "yabiao.canjia_v2", 0.9, True,
                                                           self.basicHandler.get_center(region))
        if pos is None:
            log.info("🚫 [押镖]找不到“参加”，可能已完成")
            return

        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        self.basicHandler.clean(region)
        log.info("⌛ [押镖]等待“开始押镖”按钮")
        pos = self.ocrPlayer.wait_find_by_pic_first(region, "yabiao.start", 0.9)
        if pos is None:
            log.info("❌ [押镖]未找到“开始押镖”按钮")
            return

        times = 0
        while True:
            pos = self.ocrPlayer.wait_no_time_find_by_pic_first(region, "yabiao.start", 0.9)
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            if self.ocrPlayer.find_by_pic_first(region, "yabiao.no_power", 0.9):
                self.basicHandler.clickCenter(region)
                log.error("⚠️ [押镖]活力不足，停止")
                break

            pos = self.ocrPlayer.find_by_pic_first(region, "yabiao.queding", 0.9)
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            times += 1
            if times >= 3:
                log.info("⏳ [押镖]达到次数上限，等待押镖或战斗结束")
                while (self.basicHandler.battling(region) or
                       self.ocrPlayer.find_by_pic_first(region, "yabiao.doing") is not None):
                    log.info("⌛ [押镖]押镖/战斗中，等待30秒")
                    self.delay(30, 30)
                break

        log.info("✅ [押镖]押镖完成")
        self.basicHandler.clean(region)

    def delay(self, min_seconds=1.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)
