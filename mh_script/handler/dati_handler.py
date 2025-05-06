from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log
from mh_script.utils.player import Player


class DaTi:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    def do(self, region: ScreenRegion):

        self.sanjie(region)

        self.keju(region)

    # 日常答题
    def sanjie(self,region:ScreenRegion):
        log.info("[三界奇缘] 开始执行三界奇缘任务流程")
        log.info("[三界奇缘] 清理界面")
        self.basicHandler.clean(region)

        log.info("[三界奇缘] 进入日常活动页面")
        self.basicHandler.goDailyActivity(region)

        log.info("[三界奇缘] 寻找“参加”按钮")
        pos = self.ocrPlayer.find_by_pic_first(region, "dati.sanjie", 0.9, True)
        if pos is None:
            pos = self.ocrPlayer.find_by_pic_first(region, "dati.sanjie_v2", 0.9, True)
            if pos is None:
                log.info("[三界奇缘] 任务已完成或找不到“参加”按钮")
                return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()


        while self.ocrPlayer.find_by_pic_first(region, "dati.sanjie_end", 0.9, True) is None:
            self.basicHandler.clickCenter(region)
            self.delay()

        log.info("[三界奇缘] 三界奇缘答题完成")

    def keju(self, region: ScreenRegion):
        log.info("[科举答题] 开始执行科举答题任务流程")
        log.info("[科举答题] 清理界面")
        self.basicHandler.clean(region)

        log.info("[科举答题] 进入日常活动页面")
        self.basicHandler.goDailyActivity(region)

        log.info("[科举答题] 寻找“参加”按钮")
        pos = self.ocrPlayer.find_by_pic_first(region, "dati.keju", 0.9, True)
        if pos is None:
            pos = self.ocrPlayer.find_by_pic_first(region, "dati.keju_v2", 0.9, True)
            if pos is None:
                log.info("[科举答题] 任务已完成或找不到“参加”按钮")
                return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        while self.ocrPlayer.find_by_pic_first(region, "dati.keju_end", 0.9, True) is None:
            self.basicHandler.clickCenter(region)
            self.delay()

        log.info("[科举答题] 科举答题完成")

    def delay(self, min_seconds=2.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)
