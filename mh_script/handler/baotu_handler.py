from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.ocr_player import OCR_Player
from mh_script.utils.player import Player


class BaoTu:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    def do(self, region: ScreenRegion = None):
        print("[宝图] 开始执行宝图任务流程")
        self.delay()

        print("[宝图] 清理页面")
        self.basicHandler.clean(region)

        print("[宝图] 检查任务栏是否存在宝图任务")
        pos = self.ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission")
        if pos is not None:
            print(f"[宝图] 点击宝图任务：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
        else:

            print("[宝图] 进入日常活动界面")
            self.basicHandler.goDailyActivity(region)

            print("[宝图] 查找“宝图.参加”按钮")
            pos = self.ocrPlayer.find_by_pic_first(region, "baotu.canjia", 0.9, True)
            if pos is None:
                print("[宝图] 找不到参加按钮，任务可能已完成")
                return
            print(f"[宝图] 点击“参加”：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            print("[宝图] 等待“听听无妨”按钮")
            pos = self.ocrPlayer.wait_find_by_pic_first(region, "baotu.start", 0.9)
            print(f"[宝图] 点击“听听无妨”：{pos}")
            if pos is None:
                print("[宝图] 等待“听听无妨”按钮异常")
                return
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            print("[宝图] 查找任务栏宝图任务")
            pos = self.ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission")
            if pos is None:
                print("[宝图] 找不到任务栏宝图任务，领取失败")
                return
            print(f"[宝图] 点击任务栏宝图任务：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        print("[宝图] 等待战斗或任务执行完成")
        while self.basicHandler.battling(region) or self.ocrPlayer.find_by_pic_first(region,
                                                                                     "baotu.baotu_mission") is not None:
            self.delay(10, 10)

        print("[宝图] 宝图任务完成")

    def dig(self, region: ScreenRegion = None):
        print("[宝图] 开始执行挖宝流程")
        self.delay()
        self.basicHandler.clean(region)

        print("[宝图] 打开包裹")
        pos = self.ocrPlayer.find_by_pic_first(region, "common.bag", 0.7)
        if pos is not None:
            print(f"[宝图] 点击包裹图标：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        print("[宝图] 点击整理按钮")
        pos = self.ocrPlayer.find_by_pic_first(region, "common.clean_up")
        if pos is not None:
            print(f"[宝图] 点击整理：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        print("[宝图] 查找包裹中的藏宝图")
        pos = self.ocrPlayer.find_by_pic_first(region, "baotu.bag_baotu")
        if pos is None:
            print("[宝图] 找不到宝图，挖宝流程结束")
            return
        print(f"[宝图] 双击藏宝图：{pos}")
        self.ocrPlayer.doubleTouch(pos, True, None)
        self.delay()

        print("[宝图] 开始使用藏宝图")
        dig_flag = True
        times = 0
        while dig_flag:
            pos = self.ocrPlayer.find_by_pic_first(region, "baotu.use_baotu")
            if pos is not None:
                print(f"[宝图] 点击使用藏宝图：{pos}")
                self.ocrPlayer.touch(pos, False, None)
                times = 0
            times += 1
            self.delay(2, 2)
            if times % 40 == 0:
                print("[宝图] 超过80秒未发现藏宝图使用按钮，结束挖宝")
                dig_flag = False

        print("[宝图] 挖宝完成")

    def delay(self, min_seconds=1.0, max_seconds=2.0):
        Player.delay()
