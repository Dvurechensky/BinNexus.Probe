# app/core/utils.py

import math

from app.core.logging import get_logger

log = get_logger("utils")


def entropy(chunk):
    freq = [0]*256

    for b in chunk:
        freq[b] += 1

    ent = 0
    for f in freq:
        if f:
            p = f / len(chunk)
            ent -= p * math.log2(p)

    return ent


def find_network_imports_custom(imports, apis):
    result = []
    lowered = [x.lower() for x in apis]

    for imp in imports:
        name = imp["name"].lower()
        if any(api in name for api in lowered):
            result.append(imp)

    return result


def find_calls_to_import(text, base, import_addr):
    matches = []

    try:
        addr_bytes = import_addr.to_bytes(4, "little", signed=False)
    except Exception:
        return matches

    for i in range(len(text) - 4):
        if text[i:i + 4] == addr_bytes:
            matches.append(base + i)

    return matches