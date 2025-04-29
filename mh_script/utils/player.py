import pyautogui
import random
import time

from mh_script.utils.screen import ScreenUtils


class Player:
    def __init__(self, accuracy=0.8):
        self.accuracy = accuracy

    # 延时
    @staticmethod
    def delay(min_seconds=0.5, max_seconds=3.0):
        time.sleep(random.uniform(min_seconds, max_seconds))

    @staticmethod
    def screen_shot(self):
        """调用 ScreenUtils 截图"""
        return ScreenUtils.screen_shot()

    @staticmethod
    def random_offset(position, offset=5):
        x, y = position
        return [x + random.randint(-offset, offset), y + random.randint(-offset, offset)]

    @staticmethod
    def random_hw(position, w, h):
        w, h = max(1, int(w / 6)), max(1, int(h / 6))
        return position[0] + random.randint(-w, w), position[1] + random.randint(-h, h)

    @staticmethod
    def click(position, is_offset=True):
        if is_offset:
            x, y = Player.random_offset(position)
        else:
            x, y = position
        duration = random.uniform(0.1, 0.2)
        pyautogui.moveTo(x, y, duration)
        pyautogui.click(x, y)
        print(f"点击坐标 ({x}, {y}) 成功")

    @staticmethod
    def doubleClick(position, is_offset=True):
        if is_offset:
            x, y = Player.random_offset(position)
        else:
            x, y = position
        duration = random.uniform(0.1, 0.2)
        pyautogui.moveTo(x, y, duration)
        pyautogui.doubleClick(x, y)
        print(f"双击坐标 ({x}, {y}) 成功")

    @staticmethod
    def rightClick(position, is_offset=True):
        if is_offset:
            x, y = Player.random_offset(position)
        else:
            x, y = position
        duration = random.uniform(0.1, 0.2)
        pyautogui.moveTo(x, y, duration)
        pyautogui.rightClick(x, y)
        print(f"右键点击坐标 ({x}, {y}) 成功")

    @staticmethod
    def drag(start_pos, end_pos):
        sx, sy = Player.random_offset(start_pos)
        ex, ey = Player.random_offset(end_pos)
        duration = random.uniform(0.1, 0.2)
        pyautogui.moveTo(sx, sy, duration)
        pyautogui.dragTo(ex, ey, duration, button='left')

    @staticmethod
    def move(position, is_offset=True):
        if is_offset:
            x, y = Player.random_offset(position)
        else:
            x, y = position
        duration = random.uniform(0.1, 0.2)
        pyautogui.moveTo(x, y, duration)
        print(f"移动坐标 ({x}, {y}) 成功")

    @staticmethod
    def touch(position, offset_click=True, img_name=None):
        """提供 touch 的简化调用（给 OCR_Player 用）"""
        Player.click(position, is_offset=offset_click)

    @staticmethod
    def doubleTouch(position, offset_click=True, img_name=None):
        """提供 touch 的简化调用（给 OCR_Player 用）"""
        Player.doubleClick(position, is_offset=offset_click)
