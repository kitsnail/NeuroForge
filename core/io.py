# core/io.py
import os

class IOManager:
    """统一管理输入、输出路径"""
    
    @staticmethod
    def prepare_scene_dir(base_output, scene_id):
        scene_dir = os.path.join(base_output, f"scene_{scene_id}")
        os.makedirs(scene_dir, exist_ok=True)
        return scene_dir

    @staticmethod
    def get_plugin_dir(scene_dir, plugin_name):
        out = os.path.join(scene_dir, plugin_name)
        os.makedirs(out, exist_ok=True)
        return out
