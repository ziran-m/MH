pyinstaller -F app_ui.py --hidden-import=paddleocr --hidden-import=pygetwindow --hidden-import=pyautogui --hidden-import=mss --add-data "module;module" --add-data "mh_script;mh_script" --windowed
