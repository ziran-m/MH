# mh_script/utils/log_util.py

import logging
import threading
from logging.handlers import TimedRotatingFileHandler

# 线程本地变量，存储每个线程的前缀
thread_local = threading.local()

def set_thread_prefix(prefix: str):
    thread_local.prefix = prefix

def get_thread_prefix():
    return getattr(thread_local, "prefix", "未知线程")

class ThreadPrefixAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        prefix = get_thread_prefix()
        return f"[{prefix}] {msg}", kwargs

# 创建 logger
logger = logging.getLogger("DailyLogger")
logger.setLevel(logging.INFO)

# 控制台日志输出
console_handler = logging.StreamHandler()
console_formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%H:%M:%S')
console_handler.setFormatter(console_formatter)

# 文件日志输出（每天新文件，最多保留7天）
file_handler = TimedRotatingFileHandler("daily_task.log", when="midnight", backupCount=7, encoding='utf-8')
file_formatter = logging.Formatter('%(asctime)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
file_handler.setFormatter(file_formatter)

# 添加 handler
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 有前缀（用于线程日志）
log = ThreadPrefixAdapter(logger, {})

# 无前缀日志（用于全局信息）
global_log = logger
