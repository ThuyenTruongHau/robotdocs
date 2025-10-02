# backend/logger.py
import logging
import os
from logging.handlers import TimedRotatingFileHandler

# Tạo thư mục logs nếu chưa có
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Đường dẫn file log
LOG_FILE = os.path.join(LOG_DIR, "app.log")

# Tạo logger chính
logger = logging.getLogger("my_app_logger")
logger.setLevel(logging.DEBUG)

# Handler ghi log ra file, reset sau 1 ngày
# when="midnight": reset lúc 00:00 mỗi ngày
# interval=1: reset mỗi 1 ngày
# backupCount=7: giữ lại 7 file log cũ (app.log.2025-09-03, ...)
file_handler = TimedRotatingFileHandler(
    LOG_FILE, when="midnight", interval=1, backupCount=7, encoding="utf-8"
)
file_handler.setLevel(logging.DEBUG)

# Format log ngắn gọn
formatter = logging.Formatter(
    "[%(asctime)s]-[%(levelname)s]-%(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
file_handler.setFormatter(formatter)

# Gắn handler vào logger
if not logger.hasHandlers():
    logger.addHandler(file_handler)

