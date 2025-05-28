

import threading
from typing import List

from mh_script.client_manager.launcher import Launcher
from mh_script.constant.constant import Constant
from mh_script.handler.baotu_handler import BaoTu
from mh_script.handler.dati_handler import DaTi
from mh_script.handler.red_lls_handler import RedLLS
from mh_script.handler.mijing_handler import MiJing
from mh_script.handler.yabiao_handler import YaBiao
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.log_util import global_log, set_thread_prefix, log
from mh_script.utils.ocr_player import OCR_Player

launcher = Launcher()

# launcher.resize_and_move_window()
# regions = launcher.get_regions()
# r = RedLLS(OCR_Player())
# r.do(regions[0])

o = OCR_Player()
o.move((699,60),True)