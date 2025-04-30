import mss

from mh_script.model.screen_region import ScreenRegion
import cv2
import numpy


class ScreenUtils:

    @staticmethod
    def screen_shot(region: ScreenRegion):
        with mss.mss() as sct:
            if region is None:
                monitor = sct.monitors[1]
                region = ScreenRegion(
                    top=monitor["top"],
                    left=monitor["left"],
                    width=monitor["width"],
                    height=monitor["height"]
                )
                # 设置截图区域
            monitor_region = {
                "top": region.top,
                "left": region.left,
                "width": region.width,
                "height": region.height
            }

            # 获取屏幕截图
            img = sct.grab(monitor_region)
            img = numpy.array(img)
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            return img
