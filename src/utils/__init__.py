def lerp(source: float, dest: float, weight: float) -> float:
    LOWER = 0
    UPPER = 1

    # prevent weird effects if `source` or `dest` is out of bounds
    if weight < LOWER:
        return source
    if weight > UPPER:
        return dest

    return source + (dest - source) * weight
