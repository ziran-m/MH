from mh_script.client_manager.launcher import Launcher
from mh_script.handler.baotu_handler import BaoTu
from mh_script.handler.mijing_handler import MiJing
from mh_script.handler.wabao_handler import WaBao
from mh_script.handler.yabiao_handler import YaBiao
from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.ocr_player import OCR_Player
from mh_script.utils.player import Player

if __name__ == "__main__":
    # ocrPlayer = OCR_Player()
    # region = ScreenRegion(0, 0, 768, 600)
    # pos = ocrPlayer.find_by_pic_first(region, "mijing.canjia", 0.9,True )
    # Player.move(pos, False)
    # regions=[]
    # region = ScreenRegion(0, 0, 768, 600)
    # regions.append(region)

    ocrPlayer = OCR_Player()

    launcher = Launcher()
    regions = launcher.get_regions()
    ocrPlayer = OCR_Player()
    wabao = WaBao(ocrPlayer)  # 假设你有这样一个方法
    wabao.do(regions[0])

    # 宝图
    # baotu = BaoTu(ocrPlayer)
    # baotu.do(region)
    # baotu.dig(region)
    # mijing = MiJing(ocrPlayer)
    # mijing.do(region)
    # yabiao = YaBiao(ocrPlayer)
    # yabiao.do(region)

