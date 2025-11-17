import os
import yaml
import importlib.util

class PluginRegistry:
    plugins = {}

    @classmethod
    def load_plugins(cls, plugins_dir="plugins"):
        for name in os.listdir(plugins_dir):
            sub = os.path.join(plugins_dir, name)
            if not os.path.isdir(sub):
                continue

            yaml_path = os.path.join(sub, "plugin.yaml")
            py_path = os.path.join(sub, "plugin.py")

            if not os.path.exists(yaml_path):
                continue

            meta = yaml.safe_load(open(yaml_path, encoding="utf-8"))

            cls.plugins[meta["name"]] = {
                "meta": meta,
                "path": py_path
            }

    @classmethod
    def get(cls, name):
        return cls.plugins.get(name)

    @classmethod
    def run(cls, name, input_data):
        plugin = cls.get(name)
        if not plugin:
            raise RuntimeError(f"Plugin {name} not found")

        module = cls._load_python(plugin["path"])
        func_name = plugin["meta"]["entry"].split(":")[1]
        func = getattr(module, func_name)

        return func(input_data)


    @staticmethod
    def _load_python(path):
        spec = importlib.util.spec_from_file_location("plugin", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
