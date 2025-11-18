# ===========================================================
# NeuroForge v1.3 Core: IOManager
# -----------------------------------------------------------
# 功能：
#   管理所有输出目录结构，负责创建并返回标准路径。
# 规范：
#   - 所有场景目录格式为 output/scene_<id>
#   - 每个插件输出目录为 scene_dir/<plugin>/
# ===========================================================

import os

class IOManager:
    """统一的输入输出路径管理器"""

    @staticmethod
    def prepare_scene_dir(base_output: str, scene_id: int) -> str:
        """创建并返回单个场景的输出目录"""
        scene_dir = os.path.join(base_output, f"scene_{scene_id}")
        os.makedirs(scene_dir, exist_ok=True)
        return scene_dir

    @staticmethod
    def get_plugin_dir(scene_dir: str, plugin_name: str) -> str:
        """为插件创建输出子目录"""
        out_dir = os.path.join(scene_dir, plugin_name)
        os.makedirs(out_dir, exist_ok=True)
        return out_dir
