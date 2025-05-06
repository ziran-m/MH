from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log
from mh_script.utils.player import Player


class DaTi:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)
    # 抓鬼
    def do(self, region: ScreenRegion):
        log.info("[抓鬼] 开始执行任务流程")
        log.info("[抓鬼] 清理界面")
        self.basicHandler.clean(region)

        log.info("[抓鬼] 进入日常活动页面")
        self.basicHandler.goDailyActivity(region)

        log.info("[抓鬼] 寻找“参加”按钮")
        pos = self.ocrPlayer.find_by_pic_first(region, "dati.keju", 0.9, True)
        if pos is None:
            pos = self.ocrPlayer.find_by_pic_first(region, "dati.keju_v2", 0.9, True)
            if pos is None:
                log.info("[抓鬼] 任务已完成或找不到“参加”按钮")
                return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        while self.ocrPlayer.find_by_pic_first(region, "dati.keju_end", 0.9, True) is None:
            self.basicHandler.clickCenter(region)
            self.delay()

        log.info("[抓鬼] 任务完成")

    def delay(self, min_seconds=2.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)
