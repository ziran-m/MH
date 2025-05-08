from mh_script.utils.ocr_player import OCR_Player

if __name__ == "__main__":

    ocrPlayer = OCR_Player()
    pos = ocrPlayer.find_by_name_first(None,"微信",0.8)
    if pos:
        ocrPlayer.move(pos)



