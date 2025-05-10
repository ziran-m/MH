from mh_script.constant.constant import Constant
from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log, global_log
from mh_script.utils.player import Player


class Ghost:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)
    # 抓鬼，在长安城
    def do(self, region: ScreenRegion,times=0):
        if times >= Constant.GHOST_NUM:
            return
        if times == 0:
            log.info("[抓鬼] 开始执行任务流程")
            log.info("[抓鬼] 清理界面")
            # 点长安城图标
            self.basicHandler.clean(region)
            pos = self.ocrPlayer.find_by_name_first(region, "长安城", 0.9)
            if pos is None:
                global_log.info("找不到长安")
                return
            self.ocrPlayer.touch(pos, False, None)
            self.delay()
            # 找到钟馗
            pos = self.ocrPlayer.find_by_name_first(region, "钟道",0.8)
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        # 点击捉鬼任务
        pos = self.ocrPlayer.wait_find_by_name_first(region, "捉鬼任务",0.9)
        if pos:
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
            self.basicHandler.clickLeftCenter(region)

        # 点击任务栏的捉鬼任务
        self.basicHandler.clean(region)
        pos = self.ocrPlayer.wait_find_by_name_first(region, "捉鬼（1/10）",0.9)
        if pos:
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        while True:
            global_log.info("抓鬼ing")
            self.delay(30,35)
            pos = self.ocrPlayer.wait_find_by_name_first(region, "捉鬼", 0.9)
            if pos:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            if  self.ocrPlayer.find_by_name_first(region, "是否继续抓鬼",0.9):
                end = self.ocrPlayer.find_by_name_first(region, "确定",0.9)
                self.ocrPlayer.touch(end, True, None)
                self.delay()
                break

        # 捉鬼完成就点击确定保证回到长安

        self.do(region,times+1)

        self.basicHandler.clean(region)
        log.info("[抓鬼] 任务完成")

    def delay(self, min_seconds=2.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)
