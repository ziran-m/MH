import threading
from typing import List

from mh_script.constant.constant import Constant
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import log, global_log
from mh_script.utils.player import Player


class BasicHandler:
    def __init__(self, ocrPlayer):
        # 初始化时创建 OCR_Player 实例
        self.ocrPlayer = ocrPlayer
        self._touch_lock = threading.Lock()

    # 打开日常活动
    def goDailyActivity(self, region: ScreenRegion = None):
        # 延迟
        self.ocrPlayer.delay()

        # 点击活动
        pos = self.ocrPlayer.find_by_pic_first(region, "common.activity", 0.4)
        if pos is None:
            log.info("❌ 匹配活动失败")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.ocrPlayer.delay()
        # 点击日常活动，防止再挑战活动页面
        pos = self.ocrPlayer.wait_find_by_pic_first(region, "common.activity_daily")
        if pos is None:
            log.info("❌ 匹配活动页面的日常活动失败")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.ocrPlayer.delay()

    def escape_all(self, regions: List[ScreenRegion]):
        threads = []
        for i in range(Constant.NUM_WINDOWS):
            self.escape_team(regions[i])

        global_log.info("✅ 脱离队伍完毕")

    # 退出队伍
    def escape_team(self, region: ScreenRegion = None):
        log.info("开始脱离队伍")
        # 点击队伍
        pos = self.ocrPlayer.find_by_name_first(region, "队伍", 0.9)
        if pos is None:
            log.info("找不到队伍")
            return
        self.ocrPlayer.touch(pos, True, None)
        self.ocrPlayer.delay()
        self.ocrPlayer.touch(pos, True, None)
        self.ocrPlayer.delay()
        # 退出队伍
        out = self.ocrPlayer.find_by_name_first(region, "退出队伍", 0.9)
        if out is None:
            self.ocrPlayer.touch(pos, True, None)
            self.ocrPlayer.delay()
            log.info("找不到退出队伍")
        self.ocrPlayer.touch(out, True, None)
        self.ocrPlayer.delay()
        # 清理页面
        self.clickCenter(region)
        self.ocrPlayer.delay()

        # 点击任务
        pos = self.ocrPlayer.find_by_pic_first(region, "common.task", 0.5)
        if pos is None:
            log.info("任务未匹配")
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
    def clean(self, region: ScreenRegion):
        for _ in range(4):
            pos = self.ocrPlayer.find_by_pic_first(region=region, target_name="common.activity", match=0.5)
            if pos is None:
                center = [region.left + region.width // 2, region.top + region.height // 2]
                self.ocrPlayer.rightClick(center, True)
                self.ocrPlayer.delay()
            else:
                self.ocrPlayer.delay()
                return

    def get_center(self, region: ScreenRegion):
        return [region.left + region.width // 2, region.top + region.height // 2]

    # 点击图中间
    def clickCenter(self, region: ScreenRegion):
        center = [region.left + region.width // 2, region.top + region.height // 2]
        self.ocrPlayer.rightClick(center, True)
        self.ocrPlayer.delay()

    def clickLeftCenter(self, region: ScreenRegion):
        center = [region.left + region.width // 2, region.top + region.height // 2]
        self.ocrPlayer.touch(center, True)
        self.ocrPlayer.delay()

    # 智能查找目标图片：
    def smart_find_pic_with_scroll(self, region, target_names, target_names2=None, match=0.8, rightmost=False,
                                   start_pos=None):
        pos = self.ocrPlayer.find_by_pic_first(region, target_names, match, rightmost)
        if pos is not None:
            return pos
        if target_names2 is not None:
            pos = self.ocrPlayer.find_by_pic_first(region, target_names2, match, rightmost)
            if pos is not None:
                return pos
        # 向上拖动尝试3次
        self.drag_down(start_pos)
        Player.delay()

        # 向下拖动尝试6次
        for _ in range(3):
            pos = self.ocrPlayer.find_by_pic_first(region, target_names, match, rightmost)
            if pos is not None:
                return pos
            if target_names2 is not None:
                pos = self.ocrPlayer.find_by_pic_first(region, target_names2, match, rightmost)
                if pos is not None:
                    return pos
            self.drag_up(start_pos, 80)
            Player.delay()

        return None

    def smart_find_bag_pic_with_scroll(self, region, target_names, target_names2=None, match=0.8, rightmost=False,
                                       start_pos=None):
        pos = self.ocrPlayer.find_by_pic_first(region, target_names, match, rightmost)
        if pos is not None:
            return pos
        if target_names2 is not None:
            pos = self.ocrPlayer.find_by_pic_first(region, target_names2, match, rightmost)
            if pos is not None:
                return pos
        x, y = start_pos
        start_pos = x + 50, y
        # 向上拖动尝试3次
        for _ in range(6):
            pos = self.ocrPlayer.find_by_pic_first(region, target_names, match, rightmost)
            if pos is not None:
                return pos
            if target_names2 is not None:
                pos = self.ocrPlayer.find_by_pic_first(region, target_names2, match, rightmost)
                if pos is not None:
                    return pos
            self.drag_down(start_pos, 100)

        # 向下拖动尝试6次
        for _ in range(6):
            pos = self.ocrPlayer.find_by_pic_first(region, target_names, match, rightmost)
            if pos is not None:
                return pos
            if target_names2 is not None:
                pos = self.ocrPlayer.find_by_pic_first(region, target_names2, match, rightmost)
                if pos is not None:
                    return pos
            self.drag_up(start_pos, 100)
        return None

    def drag_down(self, start_pos, distance=100):
        with self._touch_lock:
            Player.drag_down(start_pos, distance)

    def drag_up(self, start_pos, distance=100):
        with self._touch_lock:
            Player.drag_up(start_pos, distance)
