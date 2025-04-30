from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.ocr_player import OCR_Player
from mh_script.utils.player import Player


class YaBiao:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    def do(self, region: ScreenRegion = None):
        # 延迟
        self.delay()
        # 清理页面
        self.basicHandler.clean(region)
        # 去到日常活动页面
        self.basicHandler.goDailyActivity(region)

        # 点击押镖的参加
        pos = self.ocrPlayer.find_by_pic_first(region, "yabiao.canjia",0.9,True)
        # 找不到就是已经完成了
        if pos is None:
            print("任务已完成或找不到")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()
        # 清理页面
        self.basicHandler.clean(region)
        times=0
        while True:
            # 会自动走到镖头脸上,点击押镖
            pos = self.ocrPlayer.wait_find_by_pic_first(region, "yabiao.start", 0.9)
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
            times+=1
            if self.ocrPlayer.find_by_pic_first(region, "yabiao.no_power", 0.9) is not None:
                print("活力不够50")
                break
            if times>=3:
                # 是否还在押镖
                while (self.basicHandler.battling(region) or
                       self.ocrPlayer.find_by_pic_first(region, "yabiao.doing") is not None):
                    self.delay(30,30)
                break
        print("押镖完成")

    def delay(self, min_seconds=0.5, max_seconds=2.0):
        Player.delay()
