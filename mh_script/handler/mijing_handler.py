import datetime
import threading
from typing import List

from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log, global_log
from mh_script.utils.player import Player


class MiJing:
    def __init__(self, ocrPlayer):
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    def do_all(self, regions: List[ScreenRegion]):
        global_log.info("🚀 [秘境] 开始执行秘境任务流程")
        threads = []

        for region in regions:
            t_do = threading.Thread(target=self.do, args=(region,))
            t_do.start()
            threads.append(t_do)

        for t in threads:
            t.join()

        global_log.info("✅ [秘境] 所有任务执行完成")

    def do(self, region: ScreenRegion):
        log.info("🚀 [秘境] 开始执行秘境任务流程")

        self.basicHandler.clean(region)

        log.info("📅 [秘境] 进入日常活动页面")
        self.basicHandler.goDailyActivity(region)

        log.info("🔍 [秘境] 寻找“参加”按钮")
        pos = self.basicHandler.smart_find_pic_with_scroll(
            region, "mijing.canjia", "mijing.canjia_v2", 0.9, True,
            self.basicHandler.get_center(region)
        )
        if pos is None:
            log.info("🚫 [秘境] 任务已完成或找不到“参加”按钮")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        log.info("⌛ [秘境] 等待“降妖”对话框")
        pos = self.ocrPlayer.wait_find_by_pic_first(region, "mijing.xiangyao")
        if pos is None:
            log.error("❌ [秘境] 等待“降妖”对话框异常")
            return

        log.info("▶️ [秘境] 进入秘境")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        pos = self.ocrPlayer.find_by_pic_first(region, "mijing.join")
        if pos is not None:
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
            pos = self.ocrPlayer.find_by_pic_first(region, "mijing.yes")
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()

        log.info("🔍 [秘境] 查找“继续挑战”按钮")
        pos = self.ocrPlayer.find_by_pic_first(region, "mijing.goon")
        if pos is None:
            log.error("❌ [秘境] 找不到“继续挑战”")
            return

        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        log.info("⚔️ [秘境] 准备进入战斗")
        self.join_fight(region)

        self.while_do(region)

        log.info("✅ [秘境] 秘境降妖完成")

    def while_do(self, region):
        resumeTimes = 0
        lastBattleTime = datetime.datetime.now()
        while True:
            if self.basicHandler.battling(region):
                log.info("⚔️ [秘境] 正在战斗中...")
                lastBattleTime = datetime.datetime.now()
            elif datetime.datetime.now() - lastBattleTime > datetime.timedelta(seconds=50):
                log.info("⏰ [秘境] 超过 50 秒未进入战斗，尝试重新进入")
                self.join_fight(region)
                lastBattleTime = datetime.datetime.now()

            resume = self.ocrPlayer.find_by_pic_first(region, "mijing.join_fight")
            if resume is not None:
                resumeTimes += 1
                if resumeTimes <= 2:
                    log.info(f"▶️ [秘境] 尝试第 {resumeTimes} 次点击“进入战斗”：{resume}")
                    self.ocrPlayer.touch(resume, True, None)
                else:
                    log.info("⚠️ [秘境] 多次进入战斗，尝试退出")
                    self.escape(region)
                    break

            if self.basicHandler.fail(region):
                log.info("❌ [秘境] 检测到战斗失败，准备退出")
                self.basicHandler.clickCenter(region)
                self.escape(region)
                break

            self.delay(5, 10)

    def escape(self, region: ScreenRegion):
        log.info("🏃‍♂️ [秘境] 开始执行逃离流程")
        self.delay()

        log.info("🖱️ [秘境] 点击中间区域")
        self.basicHandler.clickCenter(region)
        self.delay()

        log.info("🔍 [秘境] 寻找“离开”按钮")
        escape = self.ocrPlayer.find_by_pic_first(region, 'mijing.escape')
        if escape is not None:
            log.info(f"▶️ [秘境] 点击“离开”按钮：{escape}")
            self.ocrPlayer.touch(escape, True, None)
            self.delay()
        else:
            log.info("❌ [秘境] 未找到“离开”按钮，可能已离开或不在战斗中")

    def join_fight(self, region: ScreenRegion):
        log.info("⚔️ [秘境] 尝试查找“降妖”图标以进入战斗")
        pos = self.ocrPlayer.find_by_pic_first(region, "mijing.fight")
        if pos is None:
            log.info("❌ [秘境] 找不到“降妖”图标，无法进入战斗")
            return
        log.info(f"▶️ [秘境] 点击“降妖”图标进入战斗：{pos}")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

    def delay(self, min_seconds=1.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)
