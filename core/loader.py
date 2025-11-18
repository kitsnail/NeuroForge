# ===========================================================
# NeuroForge v1.3 Core: PluginLoader
# -----------------------------------------------------------
# 功能：
#   负责动态加载 plugins 目录下的所有插件模块。
# 规范：
#   - 插件必须包含 run(ctx) 函数作为入口。
#   - 插件调用方式统一为 PluginLoader.get(name)(ctx)
# ===========================================================

import os
import importlib.util

class PluginLoader:
    """NeuroForge 插件加载器"""
    plugins = {}

    @classmethod
    def load_plugins(cls, plugins_dir="plugins"):
        """动态加载所有插件模块"""
        cls.plugins.clear()
        if not os.path.exists(plugins_dir):
            return

        for folder in os.listdir(plugins_dir):
            subdir = os.path.join(plugins_dir, folder)
            plugin_file = os.path.join(subdir, "plugin.py")
            if not os.path.isfile(plugin_file):
                continue

            module = cls._load_module(plugin_file, f"plugins.{folder}.plugin")
            if hasattr(module, "run"):
                cls.plugins[folder] = module.run

    @staticmethod
    def _load_module(path, module_name):
        spec = importlib.util.spec_from_file_location(module_name, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    @classmethod
    def get(cls, name):
        """根据插件名称获取函数句柄"""
        return cls.plugins.get(name)
