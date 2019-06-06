from base_platforms import feldbahn

base_platforms = {}
for k, v in feldbahn.base_platforms.items():
    # !! untested, prevent over-writing existing values
    print(k, v)
    if k in base_platforms:
        raise
    base_platforms[k] = v
