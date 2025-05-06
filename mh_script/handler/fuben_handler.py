from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.player import Player


class Fuben:

    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    # 前置条件，队伍组队组好
    def do(self,region:ScreenRegion,go_map,times=0):
        if times > 1:
            return
        # 清理页面
        self.basicHandler.clean(region)

        # 点击副本的参加
        if go_map:
            # 去到日常活动页面
            self.basicHandler.goDailyActivity(region)
            pos = self.ocrPlayer.find_by_pic_first(region, "fuben.canjia", 0.9, True)
            # 找不到就是已经完成了
            if pos is None:
                print("副本任务已完成或找不到")
                return
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
        else:
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

            # 找到百晓仙子
            pos = self.ocrPlayer.find_by_name(region, "百晓仙子")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        # 等待找到百晓仙子
        pos = self.ocrPlayer.wait_find_by_pic_first(region, "fuben.join", 0.9)
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        # 第一次进来点击侠士副本
        if times == 0:
            pos = self.ocrPlayer.wait_find_by_pic_first(region, "fuben.xiashi", 0.9)
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
        # 进入
        pos = self.ocrPlayer.wait_find_by_pic_first(region, "fuben.join", 0.9)
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        # 需要点击确定
        pos_list = self.ocrPlayer.find_by_pic(region, "fuben.check", 0.9)
        if pos_list is not None:
            for p in pos_list:
                self.ocrPlayer.touch(p, True, None)
                self.delay()
        # 副本里面没有活动这个图标
        while self.ocrPlayer.find_by_pic_first(region,"common.activity") is None:
            # 副本任务有个时间的标志
            pos = self.ocrPlayer.find_by_pic_first(region, "common.time")
            if pos is None:
                # 战斗中或者有对话
                self.clickSkip(region)
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            # 好多都要手动点击按钮才能进入战斗


            break



        self.do(region,go_map,times+1)

        print("三本完成")

    def clickSkip(self,region):
        return

    def delay(self, min_seconds=0.5, max_seconds=3.0):
        Player.delay()