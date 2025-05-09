from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log
from mh_script.utils.player import Player


class Ghost:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)
    # 抓鬼，在长安城
    def do(self, region: ScreenRegion):
        log.info("[抓鬼] 开始执行任务流程")
        log.info("[抓鬼] 清理界面")
        # 点长安城图标
        self.basicHandler.clean(region)
        pos = self.ocrPlayer.find_by_pic_first(region, "fuben.changan", 0.9, True)
        if pos is None:
            print("找不到长安")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()
        # 地图转换
        pos = self.ocrPlayer.find_by_pic_first(region, "fuben.tab_map", 0.9, True)
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        # 找到钟馗
        pos = self.ocrPlayer.find_by_name_first(region, "钟馗")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        # 点击捉鬼任务
        pos = self.ocrPlayer.wait_find_by_name_first(region, "捉鬼任务")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()


        log.info("[抓鬼] 任务完成")

    def delay(self, min_seconds=2.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)
