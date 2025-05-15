from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log
from mh_script.utils.player import Player


class DaTi:
    def __init__(self, ocrPlayer):
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    def do(self, region: ScreenRegion):
        self.sanjie(region)
        self.keju(region)

    # 三界奇缘答题
    def sanjie(self, region: ScreenRegion):
        log.info("🌀 [三界奇缘] 开始任务流程")
        self.basicHandler.clean(region)

        log.info("📅 [三界奇缘] 进入日常活动页面")
        self.basicHandler.goDailyActivity(region)

        log.info("🔍 [三界奇缘] 寻找“参加”按钮")
        pos = self.basicHandler.smart_find_pic_with_scroll(
            region, "dati.sanjie", "dati.sanjie_v2", 0.9, True, self.basicHandler.get_center(region)
        )
        if pos is None:
            log.info("🚫 [三界奇缘] 任务已完成或未找到参加按钮")
            return
        log.info(f"▶️ [三界奇缘] 点击参加：{pos}")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        while self.ocrPlayer.find_by_pic_first(region, "dati.sanjie_end", 0.9, True) is None:
            self.basicHandler.clickLeftCenter(region)
            self.delay()

        self.basicHandler.clean(region)
        log.info("✅ [三界奇缘] 答题完成")

    # 科举答题
    def keju(self, region: ScreenRegion):
        log.info("🌀 [科举答题] 开始任务流程")
        self.basicHandler.clean(region)

        log.info("📅 [科举答题] 进入日常活动页面")
        self.basicHandler.goDailyActivity(region)

        log.info("🔍 [科举答题] 寻找“参加”按钮")
        pos = self.basicHandler.smart_find_pic_with_scroll(
            region, "dati.keju", "dati.keju_v2", 0.9, True, self.basicHandler.get_center(region)
        )
        if pos is None:
            log.info("🚫 [科举答题] 任务已完成或未找到参加按钮")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        while self.ocrPlayer.find_by_pic_first(region, "dati.keju_end", 0.9, True) is None:
            self.basicHandler.clickLeftCenter(region)
            self.delay()

        self.basicHandler.clean(region)
        log.info("✅ [科举答题] 答题完成")

    def delay(self, min_seconds=2.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)