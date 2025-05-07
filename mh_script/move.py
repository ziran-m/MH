from mh_script.model.screen_region import ScreenRegion
from mh_script.utils.ocr_player import OCR_Player
from mh_script.utils.player import Player

if __name__ == "__main__":
    ocrPlayer = OCR_Player()
    region = ScreenRegion(0, 0, 768, 600)
    pos = ocrPlayer.find_by_pic_first(region, "baotu.baotu_mission", )
    Player.move(pos, False)


