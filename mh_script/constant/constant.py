
class Constant:
    # 游戏启动器配置
    EXE_PATH = r"E:\D\MH\My\MyLauncher_x64r.exe"
    WINDOW_TITLE_KEYWORD = "梦幻西游"
    PROCESS_NAME_KEYWORD = "MyLauncher"
    NUM_WINDOWS = 5  # 打开5个客户端
    GHOST_NUM = 2  # 抓鬼轮数
    DUNGEON_NUM= 0 # 是否打狭义 1 不打 0 打


    # 窗口尺寸（4:3）
    WINDOW_WIDTH = 768
    WINDOW_HEIGHT = 600

    # 每行最大窗口数量
    WINDOWS_PER_ROW = 3

    # 窗口起始位置
    START_X = 0
    START_Y = 0

    # 窗口间隔
    X_GAP = WINDOW_WIDTH
    Y_GAP = WINDOW_HEIGHT + 50
