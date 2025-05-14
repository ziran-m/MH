from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log, global_log
from mh_script.utils.player import Player

# 红色玲珑石
class RedLLS:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    def do(self, region: ScreenRegion):
        global_log.info("[玲珑石] 开始执行玲珑石流程")
        self.basicHandler.clean(region)

        global_log.info("[玲珑石] 打开包裹")
        pos = self.ocrPlayer.find_by_pic_first(region, "common.bag", 0.7)
        if pos:
            global_log.info(f"[玲珑石] 点击包裹图标：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        global_log.info("[玲珑石] 点击整理按钮")
        pos = self.ocrPlayer.find_by_pic_first(region, "common.clean_up")
        if pos:
            log.info(f"[玲珑石] 点击整理：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        global_log.info("[玲珑石] 查找包裹中的红色玲珑石")
        pos = self.basicHandler.smart_find_pic_with_scroll(region, "lls.red", None, 0.8, False,
                                                           self.basicHandler.get_center(region))
        if pos is None:
            log.info("[玲珑石] 找不到玲珑石，玲珑石流程结束")
            return
        global_log.info(f"[玲珑石] 双击玲珑石：{pos}")
        self.ocrPlayer.doubleTouch(pos, True, None)
        self.delay()

        for _  in range(0,5):
            pos = self.ocrPlayer.wait_find_by_pic_first(region,"lls.start")
            if pos is  None:
                continue
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            pos = self.ocrPlayer.wait_find_by_pic_first(region, "lls.confirmed")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()


        global_log.info("[玲珑石] 玲珑石完成")



    def delay(self, min_seconds=2.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)
