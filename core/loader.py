# core/loader.py
import os
import importlib.util

class PluginLoader:
    plugins = {}

    @classmethod
    def load_plugins(cls, plugins_dir="plugins"):
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
        return cls.plugins.get(name)
