# app/core/io.py

import pefile

from app.core.logging import get_logger

log = get_logger("io")


def get_text_section(path):
    log.info(f"Loading PE: {path}")

    try:
        pe = pefile.PE(path)
    except Exception as e:
        log.error(f"Failed to parse PE: {e}")
        raise

    for section in pe.sections:
        name = section.Name.decode(errors="ignore").strip("\x00")
        log.debug(f"Found section: {name}")

        if name == ".text":
            data = section.get_data()
            va = section.VirtualAddress
            log.info(f".text найден: size={len(data)} bytes, VA=0x{va:X}")
            return data, va

    log.error(".text section not found")
    raise Exception(".text not found")


def get_imports(path):
    pe = pefile.PE(path)

    imports = []

    if not hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
        return imports

    for entry in pe.DIRECTORY_ENTRY_IMPORT:
        dll = entry.dll.decode(errors="ignore")

        for imp in entry.imports:
            if imp.name:
                name = imp.name.decode(errors="ignore")
                addr = imp.address

                imports.append({
                    "dll": dll,
                    "name": name,
                    "addr": addr
                })

    return imports


def get_image_base(path):
    pe = pefile.PE(path)
    return pe.OPTIONAL_HEADER.ImageBase