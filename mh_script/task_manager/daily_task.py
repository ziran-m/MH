import threading
from typing import List
from mh_script.handler.mijing_handler import MiJing
from mh_script.handler.yabiao_handler import YaBiao
from mh_script.model.screen_region import ScreenRegion
from mh_script.handler.baotu_handler import BaoTu
from mh_script.handler.dati_handler import DaTi
from mh_script.constant.constant import Constant
from mh_script.utils.log_util import global_log , set_thread_prefix
from mh_script.utils.ocr_player import OCR_Player



class DailyTask:
    def __init__(self, regions: List[ScreenRegion]):
        ocrPlayer = OCR_Player()
        self.baotu = BaoTu(ocrPlayer)
        self.mijing = MiJing(ocrPlayer)
        self.yabiao = YaBiao(ocrPlayer)
        self.dati = DaTi(ocrPlayer)
        self.regions = regions

    def run_tasks(self, region: ScreenRegion, idx: int):
        prefix = f"窗口{idx}"
        set_thread_prefix(prefix)
        global_log .info("开始执行日常任务")

        self.baotu.do(region)
        self.baotu.dig(region)
        self.mijing.do(region)
        self.yabiao.do(region)
        self.dati.do(region)

        global_log .info("✅ 所有日常任务完成")

    def run(self, idx: int):
        if idx == -1:
            threads = []
            for i in range(Constant.NUM_WINDOWS):
                thread = threading.Thread(target=self.run_tasks, args=(self.regions[i], i))
                threads.append(thread)
                thread.start()

            for thread in threads:
                thread.join()

            global_log.info( "✅ 所有窗口的任务执行完毕")
        else:
            self.run_tasks(self.regions[idx], idx)
