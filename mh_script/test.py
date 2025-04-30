from mh_script.model.screen_region import ScreenRegion
from mh_script.task_manager.daily_task import DailyTask
from mh_script.utils.ocr_player import OCR_Player
from mh_script.utils.player import Player



def main():
    ocrPlayer = OCR_Player()
    region = ScreenRegion(0, 0, 708, 600)


    pos = ocrPlayer.find_by_pic_first(region, "baotu.start", 0.9, False)

    Player.move(pos, False)


if __name__ == "__main__":
    regions=[]
    region = ScreenRegion(0, 0, 708, 600)
    regions.append(region)

    daily = DailyTask(regions)
    daily.run(0)
