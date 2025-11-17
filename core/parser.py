import re
import os
import yaml

class Scene:
    def __init__(self, title, narration, visual, subtitle):
        self.title = title
        self.narration = narration
        self.visual = visual
        self.subtitle = subtitle


class Parser:
    def parse(self, markdown_path):
        with open(markdown_path, "r", encoding="utf-8") as f:
            text = f.read()

        meta = self._parse_meta(text)
        scenes = self._parse_scenes(text)

        return meta, scenes


    def _parse_meta(self, text):
        meta_match = re.search(r"---(.*?)---", text, re.S)
        if not meta_match:
            return {}

        meta_text = meta_match.group(1)
        return yaml.safe_load(meta_text)


    def _parse_scenes(self, text):
        blocks = re.split(r"## ", text)[1:]
        scenes = []

        for block in blocks:
            lines = block.strip().split("\n")
            title = lines[0].strip()

            narration = []
            visual = ""
            subtitle = {}

            mode = None

            for line in lines[1:]:
                if line.startswith("### narration"):
                    mode = "narration"
                elif line.startswith("### visual"):
                    mode = "visual"
                elif line.startswith("### subtitle"):
                    mode = "subtitle"
                else:
                    if mode == "narration" and line.strip():
                        narration.append(line.strip("- ").strip())
                    elif mode == "visual":
                        visual += line + "\n"
                    elif mode == "subtitle" and ":" in line:
                        k, v = line.split(":")
                        subtitle[k.strip()] = v.strip()

            scenes.append(Scene(title, narration, visual, subtitle))

        return scenes
