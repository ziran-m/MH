import sys
import threading

from paddleocr import PaddleOCR

from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.screen import ScreenUtils
from .player import Player
import os
import cv2
import numpy


class OCR_Player(Player):
    def __init__(self, accuracy=0.8):
        super().__init__(accuracy)
        self.target_map = {}
        self.load_targets()

    def read(self, region: ScreenRegion = None, debug=False):

        # 截图
        img = ScreenUtils.screen_shot(region) if region else ScreenUtils.screen_shot()
        # 加锁调用 OCR
        result = PaddleOCR(use_angle_cls=True, use_gpu=False).ocr(img, cls=True)
        data = result[0]
        return data

    def find_by_name(self, region: ScreenRegion, keyword, accuracy=None, debug=True):
        """在截图中寻找目标"""
        loc_pos = []
        """根据关键字查找文本中心坐标"""
        if debug:
            print(f"[OCR] 开始查找关键字：'{keyword}'，区域：{region}，置信度阈值：{accuracy}")

        data = self.read(region, debug=debug)

        if accuracy:
            self.accuracy = accuracy

        for i, line in enumerate(data):
            text, confidence = line[1][0], line[1][1]
            if debug:
                print(f"[OCR][{i}] 文本：'{text}'，置信度：{confidence:.4f}")

            if keyword in text and confidence is not None and confidence >= self.accuracy:
                box = line[0]  # 四个顶点坐标
                x = sum(pt[0] for pt in box) / 4
                y = sum(pt[1] for pt in box) / 4
                loc_pos.append([x, y])


        print(f'查找结果：{keyword} 匹配到 {len(loc_pos)} 个位置')
        return loc_pos if loc_pos else None

    # 匹配文字
    def find_by_name_first(self, region: ScreenRegion, keyword, accuracy=None, debug=True) -> tuple[int, int] | None:

        """根据关键字查找文本中心坐标"""
        if debug:
            print(f"[OCR] 开始查找关键字：'{keyword}'，区域：{region}，置信度阈值：{accuracy}")

        data = self.read(region, debug=debug)

        if accuracy:
            self.accuracy = accuracy

        for i, line in enumerate(data):
            text, confidence = line[1][0], line[1][1]
            if debug:
                print(f"[OCR][{i}] 文本：'{text}'，置信度：{confidence:.4f}")

            if keyword in text and confidence is not None and confidence >= self.accuracy:
                box = line[0]  # 四个顶点坐标
                x = sum(pt[0] for pt in box) / 4 + region.left
                y = sum(pt[1] for pt in box) / 4 + region.top
                print(f"[OCR] 找到匹配项 '{text}'，坐标：({int(x)}, {int(y)})")
                return int(x), int(y)
        print(f"[OCR] 未找到匹配关键字：'{keyword}'")
        return None

    # 循环等待
    def wait_find_by_name_first(self, region: ScreenRegion, keyword, accuracy=None, debug=False):
        position = self.find_by_name_first(region, keyword, accuracy, debug)
        times = 0
        while position is None and times <= 10:
            self.delay()
            times += 1
            position = self.find_by_name_first(region, keyword, accuracy, debug)
        return position


    def touch(self, position, offset_click=True, img_name=None):
        Player.touch(position, offset_click, img_name)

    def doubleTouch(self, position, offset_click=True, img_name=None):
        Player.doubleTouch(position, offset_click, img_name)

    # 循环等待
    def wait_find_by_pic_first(self, background: ScreenRegion, target_name, match=None, rightmost=False,max_num=10):
        position = self.find_by_pic_first(background, target_name, match, rightmost)
        times = 0
        while position is None and times <= max_num:
            self.delay()
            times += 1
            position = self.find_by_pic_first(background, target_name, match, rightmost)
        return position

    def wait_no_time_find_by_pic_first(self, background: ScreenRegion, target_name, match=None, rightmost=False):
        position = self.find_by_pic_first(background, target_name, match, rightmost)

        while position is None:
            self.delay()

            position = self.find_by_pic_first(background, target_name, match, rightmost)
        return position

    # 匹配截图
    def find_by_pic(self, region: ScreenRegion, target_name):
        """在截图中寻找目标"""
        loc_pos = []
        if target_name not in self.target_map:
            print(f"❌ 未加载目标图片: {target_name}")
            return loc_pos

        target, _ = self.target_map[target_name]
        h, w = target.shape[:2]
        ex, ey = 0, 0

        background = ScreenUtils.screen_shot(region)
        result = cv2.matchTemplate(background, target, cv2.TM_CCOEFF_NORMED)
        locations = numpy.where(result >= self.accuracy)

        for pt in zip(*locations[::-1]):
            x = pt[0]  + w // 2
            y = pt[1]  + h // 2
            if abs(x - ex) + abs(y - ey) < 15:
                continue
            ex, ey = x, y
            loc_pos.append([x, y])

        print(f'查找结果：{target_name} 匹配到 {len(loc_pos)} 个位置')
        return loc_pos if loc_pos else None

    # 匹配第一个截图
    def find_by_pic_first(self, region: ScreenRegion, target_name, match=None, rightmost=False):
        """在截图中寻找目标"""
        if target_name not in self.target_map:
            print(f"❌ 未加载目标图片: {target_name}")
            return None

        target, _ = self.target_map[target_name]
        h, w = target.shape[:2]
        background = ScreenUtils.screen_shot(region)
        result = cv2.matchTemplate(background, target, cv2.TM_CCOEFF_NORMED)
        if match is None:
            match = self.accuracy
        locations = numpy.where(result >= match)

        if rightmost:
            # 最右侧
            for pt in zip(*locations[::-1]):
                x = pt[0] + region.left + w
                y = pt[1] + region.top + h // 2
                return [x, y]  # 直接返回第一个匹配
        else:
            # 原逻辑，匹配第一个
            for pt in zip(*locations[::-1]):
                x = pt[0] + region.left + w // 2
                y = pt[1] + region.top + h // 2
                return [x, y]  # 直接返回第一个匹配
            return None

    # 加载资源库的所有截图
    def load_targets(self, folder_name='resource'):
        """加载目标图片"""
        self.target_map.clear()
        target_folder = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(target_folder):
            print(f"❌ 目标文件夹 {target_folder} 不存在")
            return

        for root, _, files in os.walk(target_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    relative_folder = os.path.relpath(root, target_folder)
                    name = os.path.splitext(file)[0]
                    if relative_folder != ".":
                        name = os.path.join(relative_folder, name).replace("\\", ".")
                    file_path = os.path.join(root, file)
                    image = cv2.imread(file_path)
                    if image is not None:
                        self.target_map[name] = (image, name)