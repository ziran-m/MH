import paddlehub as hub
from PyQt6.QtGui.QTextCursor import position

from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.screen import ScreenUtils
from player import Player
import os
import cv2
import numpy

class OCR_Player(Player):
    def __init__(self, accuracy=0.85):
        super().__init__(accuracy)
        self.ocr = hub.Module(name="chinese_ocr_db_crnn_mobile", enable_mkldnn=True)
        self.load_targets()
        self.target_map = {}

    def read(self, debug=False, region: ScreenRegion = None):
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
    def find_by_name(self, key_list, debug=False):
        """找到关键字"""
        data = self.read(debug)
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
        Player.touch(position,offset_click,img_name)

    # 循环等待
    def wait_find_by_pic(self, background:ScreenRegion, target_name):
        position = self.find_by_pic(background,target_name)
        while position is  None:
            self.delay()
            position = self.find_by_pic(background, target_name)
        return position


    # 匹配截图
    def find_by_pic(self, background:ScreenRegion, target_name):
        """在截图中寻找目标"""
        loc_pos = []
        if target_name not in self.target_map:
            print(f"未加载目标图片: {target_name}")
            return loc_pos

        target, _ = self.target_map[target_name]
        h, w = target.shape[:2]
        ex, ey = 0, 0

        result = cv2.matchTemplate(background, target, cv2.TM_CCOEFF_NORMED)
        locations = numpy.where(result >= self.accuracy)

        for pt in zip(*locations[::-1]):
            x, y = pt[0] + w // 2, pt[1] + h // 2
            if abs(x - ex) + abs(y - ey) < 15:
                continue
            ex, ey = x, y
            loc_pos.append([x, y])

        print(f'查找结果：{target_name} 匹配到 {len(loc_pos)} 个位置')
        return loc_pos if loc_pos else None

    # 匹配第一个截图
    def find_by_pic_first(self, background: ScreenRegion, target_name):
        """在截图中寻找目标"""
        if target_name not in self.target_map:
            print(f"未加载目标图片: {target_name}")
            return None

        target, _ = self.target_map[target_name]
        h, w = target.shape[:2]
        ex, ey = 0, 0

        result = cv2.matchTemplate(background, target, cv2.TM_CCOEFF_NORMED)
        locations = numpy.where(result >= self.accuracy)

        for pt in zip(*locations[::-1]):
            x, y = pt[0] + w // 2, pt[1] + h // 2
            if abs(x - ex) + abs(y - ey) < 15:
                continue
            return [x,y]
        return  None

    # 加载资源库的所有截图
    def load_targets(self, folder_name='resource'):
        """加载目标图片"""
        self.target_map.clear()
        target_folder = os.path.join(os.getcwd(), folder_name)
        if not os.path.exists(target_folder):
            print(f"目标文件夹 {target_folder} 不存在")
            return

        for root, _, files in os.walk(target_folder):
            for file in files:
                if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                    # 通过结合文件夹和文件名来创建唯一的名称
                    relative_folder = os.path.relpath(root, target_folder)
                    name = os.path.splitext(file)[0]
                    if relative_folder != ".":
                        name = os.path.join(relative_folder, name)
                    file_path = os.path.join(root, file)
                    image = cv2.imread(file_path)
                    if image is not None:
                        self.target_map[name] = (image, name)