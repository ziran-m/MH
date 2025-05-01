import mss
import paddlehub as hub

from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.screen import ScreenUtils
from .player import Player
import os
import cv2
import numpy


class OCR_Player(Player):
    def __init__(self, accuracy=0.8):
        super().__init__(accuracy)
        self.ocr = hub.Module(name="chinese_ocr_db_crnn_mobile", enable_mkldnn=True)
        self.target_map = {}
        self.load_targets()

    def read(self, region: ScreenRegion = None, debug=False):
        """截图并识别，可传入区域"""
        screen = ScreenUtils.screen_shot(region) if region else ScreenUtils.screen_shot()
        imgs = [screen]
        results = self.ocr.recognize_text(
            images=imgs,
            use_gpu=False,
            output_dir='ocr_result',
            visualization=debug,
            box_thresh=self.accuracy,
            text_thresh=self.accuracy
        )
        data = results[0]['data']
        return data

    # 匹配文字
    def find_by_name(self,region: ScreenRegion ,key_list, debug=False):
        """找到关键字"""
        data = self.read(region,debug)
        key_list = [key_list] if isinstance(key_list, str) else key_list
        re = False
        for key in key_list:
            found = [e for e in data if key in e['text']]
            msg = f'目标：{key}, 找到数量：{len(found)}'
            print(msg)
            if found:
                p1, _, p2, _ = found[0]['text_box_position']
                (x1, y1), (x2, y2) = p1, p2
                center = (int((x1 + x2) / 2), int((y1 + y2) / 2))
                return center
        return None

    def touch(self, position, offset_click=True, img_name=None):
        Player.touch(position, offset_click, img_name)

    def doubleTouch(self, position, offset_click=True, img_name=None):
        Player.doubleTouch(position, offset_click, img_name)
    # 循环等待
    def wait_find_by_pic_first(self, background: ScreenRegion, target_name, match=None, rightmost=False):
        position = self.find_by_pic_first(background, target_name,match,rightmost)
        times = 0
        while position is None and times <=10:
            self.delay()
            times+=1
            position = self.find_by_pic_first(background, target_name,match,rightmost)
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

        background =ScreenUtils.screen_shot(region)
        result = cv2.matchTemplate(background, target, cv2.TM_CCOEFF_NORMED)
        locations = numpy.where(result >= self.accuracy)

        for pt in zip(*locations[::-1]):
            x = pt[0] + region.left + w // 2
            y = pt[1] + region.top + h // 2
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
                y = pt[1] + region.top + h //2
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
                    # 通过结合文件夹和文件名来创建唯一的名称
                    relative_folder = os.path.relpath(root, target_folder)
                    name = os.path.splitext(file)[0]
                    if relative_folder != ".":
                        name = os.path.join(relative_folder, name).replace("\\", ".")
                    file_path = os.path.join(root, file)
                    image = cv2.imread(file_path)
                    if image is not None:
                        self.target_map[name] = (image, name)
