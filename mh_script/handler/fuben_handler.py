from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log, global_log
from mh_script.utils.player import Player


class Fuben:

    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    # 前置条件，队伍组队组好，在长安城
    def do(self, region: ScreenRegion, go_map=False, times=0):
        if times > 2:
            return
        if times != 0:

            # 点击副本的参加
            if go_map:
                # 去到日常活动页面
                self.basicHandler.goDailyActivity(region)
                pos = self.ocrPlayer.find_by_pic_first(region, "fuben.canjia", 0.9, True)
                # 找不到就是已经完成了
                if pos is None:
                    global_log.info("副本任务已完成或找不到")
                    return
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            else:
                # 点长安城图标
                self.basicHandler.clean(region)
                pos = self.ocrPlayer.find_by_name_first(region, "长安城", 0.9)
                if pos is None:
                    global_log.info("找不到长安")
                    return
                self.ocrPlayer.touch(pos, False, None)
                self.delay()

                # 找到百晓仙子
                pos = self.ocrPlayer.find_by_name_first(region, "百晓仙子")
                if pos is None:
                    pos = self.ocrPlayer.find_by_name_first(region, "袁天罡")
                    self.ocrPlayer.touch(pos, True, None)
                    self.delay()
                    self.delay(7, 7)
                    self.basicHandler.clickCenter(region)
                    # 点长安城图标
                    self.basicHandler.clean(region)
                    pos = self.ocrPlayer.find_by_name_first(region, "长安城", 0.9)
                    if pos is None:
                        global_log.info("找不到长安")
                        return
                    self.ocrPlayer.touch(pos, False, None)
                    self.delay()

                # 找到百晓仙子
                pos = self.ocrPlayer.find_by_name_first(region, "百晓仙子")
                self.ocrPlayer.touch(pos, True, None)
                self.delay()

            # 等待找到百晓仙子出现对话框
            pos = self.ocrPlayer.wait_find_by_name_first(region, "选择副本")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            # 第一次进来点击侠士副本
            if times == 0:
                pos = self.ocrPlayer.find_by_name_first(region, "侠士副本", 0.9)
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            # 进入
            pos_list = self.ocrPlayer.find_by_name(region, "进入", 0.9)
            if times == 0 or times == 1:
                self.ocrPlayer.touch(pos_list[0], True, None)
                self.delay()
            else:
                self.ocrPlayer.touch(pos_list[1], True, None)
                self.delay()

            # 侠士需要全图点击确定
            if times == 0:
                pos_list = self.ocrPlayer.find_by_pic(None, "fuben_zhunbei", 0.9)
                if pos_list is not None:
                    for p in pos_list:
                        self.ocrPlayer.touch(p, True, None)
                        self.delay()
        # 副本里面没有活动这个图标
        while self.ocrPlayer.find_by_pic_first(region, "common.activity") is None:
            while self.basicHandler.battling(region):
                log.info("战斗中")
                self.delay()
            # 没有血条那就是在剧情，狂点左键就完事了
            while self.ocrPlayer.find_by_name(region, "任务", 0.9) is None:
                self.basicHandler.clickLeftCenter(region)
                self.delay()
            # 跳过剧情
            pos = self.ocrPlayer.find_by_name_first(region, "跳过剧情动画")
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            # 副本任务有个时间的标志,
            pos = self.ocrPlayer.find_by_pic_first(region, "fuben.time")
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            # 有对话框就进去然后进入战斗
            pos = self.ocrPlayer.find_by_pic_first(region, "fuben.talk", 0.8)
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
            pos = self.ocrPlayer.find_by_name_first(region, "尔等才是", 0.9)
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                self.delay()
        self.do(region, go_map, times + 1)

        global_log.info("[副本] 三本完成")

    def clickSkip(self, region):
        return

    def delay(self, min_seconds=0.5, max_seconds=3.0):
        Player.delay()
