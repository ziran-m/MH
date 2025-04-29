import mss
from mh_script.model.screen_region import ScreenRegion


class ScreenUtils:
    @staticmethod
    def screen_shot(region: ScreenRegion = None):
        """截图，可选指定区域对象"""
        with mss.mss() as sct:
            monitor = sct.monitors[0]  # 主屏幕

            if region is None:
                region = ScreenRegion(
                    top=0,
                    left=0,
                    width=monitor["width"],
                    height=monitor["height"]
                )

            capture_area = {
                "top": region.top,
                "left": region.left,
                "width": region.width,
                "height": region.height
            }

            screenshot = sct.grab(capture_area)
            img = np.array(screenshot)
            return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
