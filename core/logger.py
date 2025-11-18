# ===========================================================
# NeuroForge v1.3 Core: Logger
# -----------------------------------------------------------
# 功能：
#   提供统一格式化日志输出。
#   所有日志以时间戳 + NeuroForge 前缀输出。
# ===========================================================

import sys
import datetime

def log(*args, **kwargs):
    """统一控制台日志输出"""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[NeuroForge {timestamp}]", *args, **kwargs)
    sys.stdout.flush()
