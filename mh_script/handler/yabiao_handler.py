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
        print("[押镖] 开始执行押镖任务流程")
        self.delay()

        print("[押镖] 开始清理页面")
        self.basicHandler.clean(region)

        print("[押镖] 准备进入日常活动界面")
        self.basicHandler.goDailyActivity(region)

        print("[押镖] 查找“押镖.参加”按钮")
        pos = self.ocrPlayer.find_by_pic_first(region, "yabiao.canjia", 0.9, True)
        if pos is None:
            print("[押镖] 找不到参加按钮，可能任务已完成")
            return

        print(f"[押镖] 点击“参加”按钮：{pos}")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        print("[押镖] 再次清理页面")
        self.basicHandler.clean(region)

        times = 0
        while True:
            print("[押镖] 等待“开始押镖”按钮出现")
            pos = self.ocrPlayer.wait_find_by_pic_first(region, "yabiao.start", 0.9)
            print(f"[押镖] 点击“开始押镖”：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
            times += 1

            no_power = self.ocrPlayer.find_by_pic_first(region, "yabiao.no_power", 0.9)
            if no_power is not None:
                print("[押镖] 活力不足，任务中止")
                break

            if times >= 3:
                print("[押镖] 达到执行上限，检查是否仍在押镖或战斗中")
                while (self.basicHandler.battling(region) or
                       self.ocrPlayer.find_by_pic_first(region, "yabiao.doing") is not None):
                    print("[押镖] 正在押镖或战斗中，等待 30 秒")
                    self.delay(30, 30)
                break

        print("[押镖] 押镖任务完成")

    def delay(self, min_seconds=0.5, max_seconds=2.0):
        Player.delay()
