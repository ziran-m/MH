
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.ocr_player import OCR_Player


class BasicHandler:
    def __init__(self):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = OCR_Player()

    # 打开日常活动
    def goDailyActivity(self,region:ScreenRegion=None):
        # 延迟
        self.ocrPlayer.delay()
        # 是否有活动
        pos = self.ocrPlayer.find_by_pic(background=region, target_name="common.activity")

        times = 0
        while pos is None:
            print("请关闭弹窗等遮挡物")
            center = [region.left + region.width // 2, region.top + region.height // 2]
            self.ocrPlayer.rightClick(center, True)
            self.ocrPlayer.delay()
            pos = self.ocrPlayer.find_by_pic(region, "common.activity")
            times += 1
            if times >= 20:
                print("有问题！！！")
                return

        # 进入活动页面
        self.ocrPlayer.touch(pos, True, None)
        self.ocrPlayer.delay()
        # 点击日常活动
        pos = self.ocrPlayer.find_by_pic(region, "common.activity_daily")
        self.ocrPlayer.touch(pos, True, None)
        self.ocrPlayer.delay()

    # 是否在战斗
    def battling(self,region:ScreenRegion):
        return self.ocrPlayer.find_by_pic(region, "common.enter_battle_flag")