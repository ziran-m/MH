import mss

from mh_script.model.screen_region import ScreenRegion
import cv2
import numpy


class ScreenUtils:

    @staticmethod
    def screen_shot(region: ScreenRegion):
        with mss.mss() as sct:
            # 设置屏幕区域
            full_monitors = {"top": region.top, "left": region.left, "width": region.width, "height": region.height}

            # 获取屏幕截图
            full_screen = sct.grab(full_monitors)
            # 截图对象转换为 NumPy 数组，以便后续在 OpenCV 中处理
            full_screen = numpy.array(full_screen)
            # 格式转换
            full_screen = cv2.cvtColor(full_screen, cv2.COLOR_BGRA2BGR)
            return full_screen
