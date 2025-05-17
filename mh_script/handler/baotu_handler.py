import threading
from typing import List

from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log,global_log
from mh_script.utils.player import Player


class BaoTu:
    def __init__(self, ocrPlayer):
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    def do_all(self, regions: List[ScreenRegion]):
        global_log.info("🔶 [宝图] 任务开始")
        threads = []
        for region in regions:
            t = threading.Thread(target=self.do, args=(region,))
            t.start()
            threads.append(t)
        for t in threads:
            t.join()
        global_log.info("✅ [宝图] 任务全部完成")

    def do(self, region: ScreenRegion):
        log.info("🔶 [宝图] 执行宝图任务")
        self.basicHandler.clean(region)

        pos = self.ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission", 0.7)
        if pos:
            log.info("⚔️ [宝图] 找到宝图任务，点击开始")
            self.ocrPlayer.touch(pos, False, None)
            self.delay(3, 5)
        else:
            log.info("📅 [宝图] 进入日常活动尝试开始宝图")
            if self.basicHandler.goDailyActivity(region) is None:
                log.error("❌ [宝图] 进入日常活动失败，任务终止")
                return
            log.info("🔍 [宝图] 寻找“参加”按钮")
            pos = self.basicHandler.smart_find_pic_with_scroll(region, "baotu.canjia", "baotu.canjia_v2", 0.9, True,
                                                               self.basicHandler.get_center(region))
            if pos is None:
                log.info("🚫 [宝图] 未找到参加按钮，任务可能已完成")
                return
            log.info("▶️ [宝图] 点击参加")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
            log.info("⌛ [宝图] 等待听听无妨按钮")
            pos = self.ocrPlayer.wait_find_by_pic_first(region, "baotu.start", 0.9)
            if not pos:
                log.error("❌ [宝图] 未找到听听无妨按钮，任务终止")
                return
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            pos = self.ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission", 0.7)
            if not pos:
                log.info("🚫 [宝图] 未找到任务栏宝图，领取失败")
                return
            log.info("⚔️ [宝图] 点击任务栏宝图任务")
            self.ocrPlayer.touch(pos, False, None)
            self.delay(3, 5)

        self.while_do(region)
        log.info("✅ [宝图] 任务完成")

    def while_do(self, region: ScreenRegion):
        log.info("⏳ [宝图] 等待战斗和任务完成")
        while True:
            in_battle = self.basicHandler.battling(region)
            has_task = self.ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission")
            has_blood = self.ocrPlayer.find_by_pic_first(region, "common.blood")
            if has_task:
                log.info("⚔️ [宝图] 点击任务栏宝图任务")
                self.ocrPlayer.touch(has_task, False, None)
                self.delay()
            if not in_battle and not has_task and has_blood:
                break
            self.delay(15, 30)
        log.info("✅ [宝图] 战斗和任务已完成")

    def dig(self, region: ScreenRegion):
        log.info("📦 [宝图] 开始挖宝")
        self.basicHandler.clean(region)
        pos = self.ocrPlayer.wait_find_by_pic_first(region, "common.bag", 0.7)
        if pos is None:
            log.info("🚫 [宝图] 未找到包裹图标，挖宝失败")
            return
        self.ocrPlayer.touch(pos, False, None)
        self.delay()

        pos = self.ocrPlayer.find_by_pic_first(region, "common.clean_up")
        if pos:
            log.info("🧹 [宝图] 整理包裹")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        pos = self.basicHandler.smart_find_bag_pic_with_scroll(region, "baotu.bag_baotu", None, 0.8, False,
                                                               self.basicHandler.get_center(region))
        if pos is None:
            log.info("🚫 [宝图] 包裹中无藏宝图，挖宝结束")
            return
        log.info("🗺️ [宝图] 双击藏宝图开始挖宝")
        self.ocrPlayer.doubleTouch(pos, True, None)
        self.delay()
        self.while_dig(region)
        log.info("✅ [宝图] 挖宝流程完成")

    def while_dig(self, region: ScreenRegion):
        log.info("⏳ [宝图] 使用藏宝图中...")
        times = 0
        while True:
            pos = self.ocrPlayer.find_by_pic_first(region, "baotu.use_baotu")
            if pos:
                self.ocrPlayer.touch(pos, False, None)
                times = 0
            times += 1
            self.delay(2, 2)
            if times % 40 == 0:
                log.info("⏰ [宝图] 80秒内未检测到使用按钮，挖宝结束")
                break

    def delay(self, min_seconds=1.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)