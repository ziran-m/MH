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

        # 点击活动
        pos = self.ocrPlayer.find_by_pic_first(region, "common.activity",0.5)
        if pos is None:
            print("❌ 匹配活动失败")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.ocrPlayer.delay()
        # 点击日常活动，防止再挑战活动页面
        pos = self.ocrPlayer.find_by_pic_first(region, "common.activity_daily")
        if pos is None:
            print("❌ 匹配活动页面的日常活动失败")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.ocrPlayer.delay()

    # 是否在战斗,true在战斗
    def battling(self, region: ScreenRegion):
        return self.ocrPlayer.find_by_pic_first(region, "common.enter_battle_flag") is not None

    # 战斗失败
    def fail(self, region: ScreenRegion):
        return self.ocrPlayer.find_by_pic_first(region, "common.fail")

    # 清理主页面，根据活动判断是否在主页面
    def clean(self,region:ScreenRegion):
        return
        for _ in range(10):
            pos = self.ocrPlayer.find_by_pic_first(region=region,target_name= "common.activity")
            if pos is None:
                center = [region.left + region.width // 2, region.top + region.height // 2]
                self.ocrPlayer.rightClick(center, True)
                self.ocrPlayer.delay()
            else:
                self.ocrPlayer.delay()
                return
    # 点击图中间
    def clickCenter(self,region:ScreenRegion):
        center = [region.left + region.width // 2, region.top + region.height // 2]
        self.ocrPlayer.rightClick(center, True)
        self.ocrPlayer.delay()
