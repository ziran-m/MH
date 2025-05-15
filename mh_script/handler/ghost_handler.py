from mh_script.constant.constant import Constant
from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log, global_log
from mh_script.utils.player import Player


class Ghost:
    def __init__(self, ocrPlayer):
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    # 抓鬼，在长安城
    def do(self, region: ScreenRegion, times=0):
        if times >= Constant.GHOST_NUM:
            global_log.info("✅ [抓鬼] 任务全部完成")
            return

        if times == 0:
            global_log.info("🚀 [抓鬼] 开始执行任务流程")
            self.basicHandler.clean(region)

            global_log.info("🔍 [抓鬼] 查找长安城图标")
            pos = self.ocrPlayer.find_by_name_first(region, "长安城", 0.9)
            if pos is None:
                global_log.info("❌ [抓鬼] 找不到长安城")
                return
            global_log.info(f"▶️ [抓鬼] 点击长安城图标 {pos}")
            self.ocrPlayer.touch(pos, False, None)
            self.delay()

            global_log.info("🔍 [抓鬼] 查找钟馗")
            pos = self.ocrPlayer.find_by_name_first(region, "钟道", 0.8)
            if pos is None:
                global_log.info("❌ [抓鬼] 找不到钟馗")
                return
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        global_log.info("⌛ [抓鬼] 等待捉鬼任务开始按钮")
        pos = self.ocrPlayer.wait_find_by_pic_first(region, "ghost.start", 0.9)
        if pos is not None:
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
            self.basicHandler.clickLeftCenter(region)

        pos = self.ocrPlayer.wait_find_by_pic_first(region, "common.time", 0.9)
        if pos:
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        while True:
            global_log.info(f"⌛ [抓鬼] 当前第{times + 1}轮，抓鬼中……")
            self.delay(30, 35)
            pos = self.ocrPlayer.wait_find_by_pic_first(region, "common.time", 0.9)
            if pos:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            if self.ocrPlayer.find_by_name_first(region, "少侠已经捉完1轮鬼，是否继续捉鬼", 0.9):
                end = self.ocrPlayer.find_by_name_first(region, "确定", 0.9)
                self.ocrPlayer.touch(end, True, None)
                self.delay()
                break

        self.do(region, times + 1)

        self.basicHandler.clean(region)
        global_log.info("✅ [抓鬼] 任务完成")

    def delay(self, min_seconds=2.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)
