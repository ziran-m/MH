import threading
from typing import List

from mh_script.handler.basic_handler import BasicHandler
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log,global_log
from mh_script.utils.player import Player


class BaoTu:
    def __init__(self, ocrPlayer):
        self.ocrPlayer = ocrPlayer
        self.basicHandler = BasicHandler(ocrPlayer)

    def do_all(self, regions: List[ScreenRegion]):
        global_log.info("[宝图] 开始执行宝图任务流程")
        threads = []

        # 启动线程处理每个区域的任务
        for i, region in enumerate(regions):
            t_do = threading.Thread(target=self.do, args=(region,))
            t_do.start()
            threads.append(t_do)

        # 等待所有线程执行完毕
        for t in threads:
            t.join()

        global_log.info("[宝图] 所有任务执行完成")

    def do(self, region: ScreenRegion):
        log.info("[宝图] 开始执行宝图任务流程")
        self.basicHandler.clean(region)

        log.info("[宝图] 检查任务栏是否存在宝图任务")
        pos = self.ocrPlayer.wait_find_by_pic_first(region, "baotu.baotu_mission",0.7)
        if pos:
            log.info(f"[宝图] 点击宝图任务：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay(3, 5)
        else:
            log.info("[宝图] 进入日常活动界面")
            if self.basicHandler.goDailyActivity(region) is None:
                log.error("[宝图] 进入日常活动页面失败，宝图结束")
                return

            log.info("[宝图] 查找“宝图.参加”按钮")
            pos = self.basicHandler.smart_find_pic_with_scroll(region,"baotu.canjia","baotu.canjia_v2",0.9,True,self.basicHandler.get_center(region))
            if pos is None:
                log.info("[宝图] 找不到参加按钮，任务可能已完成")
                return
            log.info(f"[宝图] 点击“参加”：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            log.info("[宝图] 等待“听听无妨”按钮")
            pos = self.ocrPlayer.wait_find_by_pic_first(region, "baotu.start", 0.9)
            if not pos:
                log.error("[宝图] 等待“听听无妨”按钮异常，宝图结束")
                return
            log.info(f"[宝图] 点击“听听无妨”：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            # 再次点击确认
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

            log.info("[宝图] 查找任务栏宝图任务")
            pos = self.ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission",0.7)
            if not pos:
                log.info("[宝图] 找不到任务栏宝图任务，领取失败,宝图结束")
                return

            log.info(f"[宝图] 点击任务栏宝图任务：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay(3, 5)
        self.while_do(region)
        log.info("[宝图] 宝图任务完成")



    def while_do(self, region: ScreenRegion):
        while True:
            log.info("[宝图] 等待战斗或任务执行完成")
            in_battle = self.basicHandler.battling(region)
            has_task = self.ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission")
            has_blood = self.ocrPlayer.find_by_pic_first(region, "common.blood")
            if has_task:
                self.ocrPlayer.touch(has_task, True, None)
                self.delay()
            # 不在战斗且没有任务，并且有人物血条，说明不在切换地图
            if not in_battle and not has_task and has_blood:
                break  # 任务完成，退出循环

            self.delay(15, 30)

    def dig(self, region: ScreenRegion):
        log.info("[宝图] 开始执行挖宝流程")
        self.basicHandler.clean(region)

        log.info("[宝图] 打开包裹")
        pos = self.ocrPlayer.wait_find_by_pic_first(region, "common.bag", 0.7)
        if pos is None:
            log.info("[宝图] 找不到包裹图标,挖宝失败")
        self.ocrPlayer.touch(pos, True, None)
        self.delay()

        log.info("[宝图] 点击整理按钮")
        pos = self.ocrPlayer.find_by_pic_first(region, "common.clean_up")
        if pos:
            log.info(f"[宝图] 点击整理：{pos}")
            self.ocrPlayer.touch(pos, True, None)
            self.delay()

        log.info("[宝图] 查找包裹中的藏宝图")
        pos = self.basicHandler.smart_find_bag_pic_with_scroll(region, "baotu.bag_baotu", None, 0.8, False,
                                                           self.basicHandler.get_center(region))
        if pos is None:
            log.info("[宝图] 找不到宝图，挖宝完成")
            return
        log.info(f"[宝图] 双击藏宝图：{pos}")
        self.ocrPlayer.doubleTouch(pos, True, None)
        self.delay()

        self.while_dig(region)

        log.info("[宝图] 挖宝完成")

    def while_dig(self, region: ScreenRegion):
        log.info("[宝图] 开始使用藏宝图")
        dig_flag = True
        times = 0
        while dig_flag:
            pos = self.ocrPlayer.find_by_pic_first(region, "baotu.use_baotu")
            if pos:
                log.info("[宝图] 点击使用藏宝图")
                self.ocrPlayer.touch(pos, False, None)
                times = 0
            times += 1
            self.delay(2, 2)
            if times % 40 == 0:
                log.info("[宝图] 超过80秒未发现藏宝图使用按钮，结束挖宝")
                dig_flag = False

    def delay(self, min_seconds=1.0, max_seconds=3.0):
        Player.delay(min_seconds, max_seconds)