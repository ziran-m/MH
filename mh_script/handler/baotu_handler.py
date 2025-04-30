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
        # 延迟
        self.delay()
        self.basicHandler.clean(region)

        # 看下任务栏有没有宝图任务先
        pos = self.ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission")
        if pos is not None:
            self.ocrPlayer.touch(pos, True, None)
            self.delay()
        # 去到日常活动页面
        self.basicHandler.goDailyActivity(region)



        # 点击宝图的参加,坐标要微调下
        pos = self.ocrPlayer.find_by_pic_first(region, "baotu.canjia",0.9,True)
        # 找不到就是已经完成了
        if pos is None:
            print("任务已完成或找不到")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        self.basicHandler.clean(region)
        # 会自动走到店小二脸上,点击听听无妨
        self.ocrPlayer.wait_find_by_pic_first(region, "baotu.start",0.9)
        self.ocrPlayer.touch(pos, True, None)
        self.delay()
        # 点下任务栏宝图任务
        pos = self.ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission")
        if pos is None:
            print("问题领取失败了")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        # 根据战斗页面和宝图任务判断是否已经结束
        while self.basicHandler.battling(region) or self.ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission"):
            self.delay(10, 10)

        print("宝图任务完成")

    # 挖宝
    def dig(self, region: ScreenRegion = None):
        # 延迟
        self.delay()
        self.basicHandler.clean(region)

        # 打开包裹
        pos = self.ocrPlayer.find_by_pic_first(region, "common.bag")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        # 点击整理
        pos = self.ocrPlayer.find_by_pic_first(region, "common.clean_up")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()
        # 双击背包里的宝图
        pos = self.ocrPlayer.find_by_pic_first(region, "baotu.bag_baotu")
        if pos is None:
            print("挖宝完成")
            return
        self.ocrPlayer.doubleTouch(pos, True, None)
        self.delay()
        # 点击藏宝图的使用
        dig_flag = True
        times = 0
        while dig_flag:
            pos = self.ocrPlayer.find_by_pic_first(region, "baotu.use_baotu")
            if pos is not None:
                self.ocrPlayer.touch(pos, True, None)
                times = 0
            times += 1
            # 2s休眠
            self.delay(2, 2)
            #  60s没有第二个使用直接跳出循环了
            if times % 30 == 0:
                dig_flag = False

        print("挖宝完成")

    def delay(self, min_seconds=0.5, max_seconds=2.0):
        Player.delay()
