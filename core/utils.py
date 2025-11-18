def normalize_payload(payload: dict) -> dict:
    """
    把 payload 中的 scene 字段平铺到顶层，插件无感知。
    """

    if "scene" not in payload:
        return payload  # already flat

    flat = dict(payload)

    scene = flat.pop("scene")  # 删除 scene 层级

    for k, v in scene.items():
        if k not in flat:       # 顶层不存在时才提升
            flat[k] = v

    return flat
