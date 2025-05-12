import datetime

from mh_script.client_manager.launcher import Launcher
from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log
from mh_script.utils.ocr_player import OCR_Player
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
            log.info(f"[挖宝] 点击包裹图标：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        pos = self.ocrPlayer.find_by_pic_first(region, "common.clean_up")
        if pos is not None:
            log.info(f"[挖宝] 点击整理：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        pos = self.ocrPlayer.find_by_pic_first(region, "wabao.wabao")
        if pos is None:
            log.info("[挖宝] 找不到挖宝，挖宝流程结束")
            return
        self.ocrPlayer.doubleTouch(pos, True, None)
        self.delay()

        pos = self.ocrPlayer.find_by_pic_first(region, "wabao.kaogu")
        if pos is None:
            log.info("[挖宝] 找不到挖宝，挖宝流程结束")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        dig_flag = True
        times = 0
        while dig_flag:
            pos = self.ocrPlayer.find_by_pic_first(region, "wabao.wajue")
            if pos is not None:
                log.info(f"[挖宝] 点击使用藏挖宝：{pos}")
                self.ocrPlayer.touch(pos, False, None)
                times = 0
            times += 1
            self.delay(2, 2)
            if times % 40 == 0:
                log.info("[挖宝] 超过80秒未发现藏挖宝使用按钮，结束挖宝")
                dig_flag = False

        log.info("[挖宝] 挖宝完成")

    def delay(self, min_seconds=0.5, max_seconds=3.0):
        Player.delay()



