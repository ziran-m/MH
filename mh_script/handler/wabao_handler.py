from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log
from mh_script.utils.player import Player


class WaBao:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    def do(self, region: ScreenRegion = None):
        self.delay()
        self.basicHandler.clean(region)

        pos = self.ocrPlayer.find_by_pic_first(region, "common.bag", 0.7)
        if pos is not None:
            log.info(f"[考古] 点击包裹图标：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        pos = self.ocrPlayer.find_by_pic_first(region, "common.clean_up")
        if pos is not None:
            log.info(f"[考古] 点击整理：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        pos = self.basicHandler.smart_find_pic_with_scroll(region, "wabao.wabao", None, 0.8, False,
                                                           self.basicHandler.get_center(region))
        if pos is None:
            log.info("[考古] 找不到铲子，考古流程结束")
            return
        self.ocrPlayer.doubleTouch(pos, True, None)
        self.delay()

        pos = self.ocrPlayer.find_by_pic_first(region, "wabao.kaogu")
        if pos is None:
            log.info("[考古] 找不到考古，考古流程结束")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        dig_flag = True
        times = 0
        while dig_flag:
            pos = self.ocrPlayer.find_by_pic_first(region, "wabao.wajue")
            if pos is not None:
                log.info(f"[考古] 点击使用：{pos}")
                self.ocrPlayer.touch(pos, False, None)
                times = 0
            times += 1
            self.delay(2, 2)
            if times % 40 == 0:
                log.info("[考古] 超过80秒未发现考古使用按钮，结束考古")
                dig_flag = False

        log.info("[考古] 考古完成")

    def delay(self, min_seconds=0.5, max_seconds=3.0):
        Player.delay()



