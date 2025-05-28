from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log, global_log
from mh_script.utils.player import Player


class Fuben:

    def __init__(self, ocrPlayer):
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    # 前置条件，队伍组队组好，在长安城
    def do(self, region: ScreenRegion, times=0):
        if times > 2:
            global_log.info("✅ [副本] 三本完成")
            self.basicHandler.clean(region)
            return

        global_log.info(f"🚀 [副本] 任务开始，第{times + 1}个")
        if times != 0:
            self.basicHandler.clean(region)

            global_log.info("🔍 [副本] 查找长安城图标")
            pos = self.ocrPlayer.find_by_name_first(region, "长安城", 0.9)
            if pos is None:
                global_log.info("❌ [副本] 找不到长安城")
                return
            global_log.info(f"▶️ [副本] 点击长安城图标 {pos}")
            self.ocrPlayer.touch(pos, False, None)
            self.delay()

            global_log.info("🔍 [副本] 查找百晓仙子")
            pos = self.ocrPlayer.find_by_name_first(region, "百晓仙子", 0.9)
            if pos is None:
                global_log.info("🔍 [副本] 找不到百晓仙子，尝试找兵器铺老板")
                pos = self.ocrPlayer.find_by_name_first(region, "兵器铺老板", 0.8)
                if pos is not None:
                    self.ocrPlayer.touch(pos, True, None)
                    self.delay()
                    self.delay(7, 7)
                    self.basicHandler.clickCenter(region)
                    self.basicHandler.clean(region)
                    global_log.info("🔍 [副本] 重新查找长安城图标")
                    pos = self.ocrPlayer.find_by_name_first(region, "长安城", 0.9)
                    if pos is None:
                        global_log.info("❌ [副本] 找不到长安城")
                        return
                    global_log.info(f"▶️ [副本] 点击长安城图标 {pos}")
                    self.ocrPlayer.touch(pos, False, None)
                    self.delay()

                else:
                    global_log.info("❌ [副本] 找不到兵器铺老板，无法继续")
                    return
            pos = self.ocrPlayer.find_by_name_first(region, "百晓仙子", 0.9)
            global_log.info(f"▶️ [副本] 点击百晓仙子 {pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            global_log.info("⌛ [副本] 等待选择副本对话框出现")
            pos = self.ocrPlayer.wait_find_by_name_first(region, "选择副本")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            if times == 0:
                pos = self.ocrPlayer.find_by_name_first(region, "侠士副本", 0.9)
                global_log.info(f"▶️ [副本] 点击侠士副本 {pos}")
                self.ocrPlayer.touch(pos, True, None)
                self.delay()

            pos_list = self.ocrPlayer.find_by_name(region, "进入", 0.9)
            if times == 0:
                global_log.info(f"▶️ [副本] 点击进入按钮 {pos_list[0]}")
                self.ocrPlayer.touch(pos_list[0], True, None)
                self.delay()
            else:
                global_log.info(f"▶️ [副本] 点击进入按钮 {pos_list[times - 1]}")
                self.ocrPlayer.touch(pos_list[times - 1], True, None)
                self.delay()

        while self.ocrPlayer.find_by_pic_first(region, "common.activity", 0.5) is None:
            global_log.info("⚔️ [副本] 流程中")
            while self.basicHandler.battling(region):
                self.delay(5, 10)
            while self.ocrPlayer.find_by_name_first(region, "任务", 0.9) is None:
                self.basicHandler.clickLeftCenter(region)
                self.delay()

            pos = self.ocrPlayer.find_by_name_first(region, "跳过剧情动画", 0.9)
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()

            pos = self.ocrPlayer.find_by_pic_first(region, "fuben.time")
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            pos = self.ocrPlayer.find_by_name_first(region, "休想我束手就擒", 0.9)
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            pos = self.ocrPlayer.find_by_name_first(region, "尔等才是", 0.9)
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            pos = self.ocrPlayer.find_by_name_first(region, "休要血口喷人", 0.9)
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            pos = self.ocrPlayer.find_by_pic_first(region, "fuben.talk", 0.8)
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()

        self.do(region, times + 1)

    def delay(self, min_seconds=0.5, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)
