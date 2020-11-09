def add_optional_kv(d, key_name, obj, attr=None, func=None):
    if obj is None:
        return
    if attr is None:
        attr = key_name.replace('-', '_')

    val = getattr(obj, attr)
    if val is not None and val != '':
        if func:
            val = getattr(val, func)()
        d[key_name] = val
    return d
