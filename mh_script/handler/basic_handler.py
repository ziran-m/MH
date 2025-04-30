from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.player import Player


class BasicHandler:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer

    # 打开日常活动
    def goDailyActivity(self, region: ScreenRegion = None):
        # 延迟
        self.ocrPlayer.delay()

        # 快捷键打开
        Player.hotKeyAlt('m')
        self.ocrPlayer.delay()
        # 点击日常活动，防止再挑战活动页面
        pos = self.ocrPlayer.find_by_pic(region, "common.activity_daily")
        self.ocrPlayer.touch(pos, True, None)
        self.ocrPlayer.delay()

    # 是否在战斗
    def battling(self, region: ScreenRegion):
        return self.ocrPlayer.find_by_pic_first(region, "common.enter_battle_flag")

    # 战斗失败
    def fail(self, region: ScreenRegion):
        return self.ocrPlayer.find_by_pic_first(region, "common.fail")
    # 清理主页面
    def clean(self,region):
        for _ in range(2):
            center = [region.left + region.width // 2, region.top + region.height // 2]
            self.ocrPlayer.rightClick(center, True)
            self.ocrPlayer.delay()

