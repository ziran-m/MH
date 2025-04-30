import datetime

from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.player import Player


class MiJing:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    # 秘境
    def do(self, region: ScreenRegion = None):
        # 延迟
        self.delay()
        self.basicHandler.clean(region)

        # 去到日常活动页面
        self.basicHandler.goDailyActivity(region)

        # 点击秘境的参加,坐标要微调下
        pos = self.ocrPlayer.find_by_pic(region, "mijing.canjia",0.6,True)
        # 找不到就是已经完成了
        if pos is None:
            print("任务已完成或找不到")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        # 会到陆萧然的对话框,秘境降妖
        pos = self.ocrPlayer.wait_find_by_pic(region, "mijing.xiangyao")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        # 如果是周一会让选择日月还是普通，选择普通
        pos = self.ocrPlayer.find_by_pic_first(region, "mijing.join")
        if pos is not None:
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
        # 点击继续挑战
        pos = self.ocrPlayer.find_by_pic_first(region, "mijing.goon")
        if pos is None :
            print("找不到继续挑战")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()
        # 点击右侧秘境降妖的框会进入战斗
        self.join_fight(region)
        # 点击进入战斗的次数
        resumeTimes = 0
        while True:
            # 如果超过50s没有进入战斗那就再点秘境
            lastBattleTime = datetime.datetime.now()
            if self.basicHandler.battling(region):
                lastBattleTime = datetime.datetime.now()
            elif datetime.datetime.now() - lastBattleTime > datetime.timedelta(seconds=50):
                self.join_fight(region)
            # 进入战斗
            resume = self.ocrPlayer.find_by_pic_first(region, "mijing.goin_fight")
            if resume is not None:
                resumeTimes += 1
                if resumeTimes <= 2:
                    self.ocrPlayer.touch(pos, True, None)
                else:
                    self.escape(region)
                    break
            # 失败了也离开
            if self.basicHandler.fail(region):
                self.escape(region)
                break
            self.delay(0, 10)
        print("秘境降妖完成")

    # 离开
    def escape(self, region: ScreenRegion):
        self.delay()
        # 点下中间
        self.basicHandler.clickCenter(region)
        self.delay()
        # 点击离开
        escape = self.ocrPlayer.find_by_pic_first(region, 'mijing.escape')
        if escape is not None:
            self.ocrPlayer.touch(escape, True, None)
            self.delay()

    def touch_center(self, region):
        center = [region.left + region.width // 2, region.top + region.height // 2]
        self.ocrPlayer.touch(center, True, None)
        self.delay()

    # 进入战斗
    def join_fight(self, region: ScreenRegion):
        pos = self.ocrPlayer.find_by_pic_first(region, "mijing.fight")
        if pos is None:
            print("找不到秘境降妖")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

    def delay(self, min_seconds=0.5, max_seconds=3.0):
        Player.delay()
