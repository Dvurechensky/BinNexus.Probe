# app/core/analyzer.py

from app.core.logging import get_logger
from app.core.io import get_image_base, get_text_section, get_imports
from app.core.utils import (
    find_calls_to_import,
    entropy,
    find_network_imports_custom,
)

log = get_logger("analyzer")


def get_region(text, base, offset, size=128):
    start = max(0, offset - base - size)
    end = start + size
    return text[start:end]

def analyze_network_with_custom_apis(path, apis):
    log.info(f"Start NETWORK analysis: {path}")

    text, text_rva = get_text_section(path)
    imports = get_imports(path)
    image_base = get_image_base(path)

    log.info(f"ImageBase: 0x{image_base:X}")
    log.info(f"Total imports: {len(imports)}")

    matched_imports = find_network_imports_custom(imports, apis)

    if not matched_imports:
        log.warning("No matching imports found")
        return []

    log.info(f"Matched imports found: {len(matched_imports)}")

    results = []

    for imp in matched_imports:
        log.info(f"Checking API: {imp['name']} ({imp['dll']})")

        matches = find_calls_to_import(text, text_rva, imp["addr"])
        log.info(f"  Found {len(matches)} references")

        for rva in matches:
            try:
                region = get_region(text, text_rva, rva, size=128)
                if not region:
                    continue

                score = entropy(region)
                va = image_base + rva
                text_offset = rva - text_rva

                results.append({
                    "api": imp["name"],
                    "dll": imp["dll"],
                    "rva": hex(rva),
                    "va": hex(va),
                    "offset": hex(text_offset),
                    "score": float(score),
                })
            except Exception as e:
                log.error(f"Error at RVA {hex(rva)}: {e}")

    results.sort(key=lambda x: x["score"], reverse=True)
    log.info(f"Analysis complete. Found {len(results)} candidates")

    return results
