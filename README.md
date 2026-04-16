<h1 align="center">BinNexus.Probe</h1>

<p align="center">
    <img src="https://shields.dvurechensky.pro/badge/Reverse-Engineering-blue">
    <img src="https://shields.dvurechensky.pro/badge/Binary-Probing-green">
    <img src="https://shields.dvurechensky.pro/badge/.NET-FastAPI-purple">
</p>

<div align="center" style="margin: 20px 0; padding: 10px; background: #1c1917; border-radius: 10px;">
  <strong>🌐 Language: </strong>
  
  <a href="./README.ru.md" style="color: #F5F752; margin: 0 10px;">
    🇷🇺 Russian
  </a>
  | 
  <span style="color: #0891b2; margin: 0 10px;">
    ✅ 🇺🇸 English (current)
  </span>
</div>

---

## Overview

**BinNexus.Probe** is a fast API-based binary probing tool designed for quick behavioral inspection of executables and DLLs.

It helps identify what a binary _does_ before diving into deep reverse engineering.

---

## Example

<p align="center">
  <img src="media/BINNEXUS.PROBE.gif">
</p>

---

## Documents

- [Build](docs/BUILD.md)
- [How to use](docs/HOW_TO_USE_x32.md)

---

## What it does

- Scans binaries for API usage patterns
- Scores detected candidates
- Highlights behavioral indicators (network, injection, crypto)
- Provides instant insight without full disassembly

---

## Why

Traditional reverse engineering tools are powerful, but often too heavy for quick inspection.

**BinNexus.Probe** focuses on:

> [!TIP]  
> Fast signal extraction instead of deep analysis.

---

## Key Features

- Dynamic API presets (network, file system, anti-debug, etc.)
- Drag & Drop binary analysis
- Automatic scan on file selection
- Dual mode:
  - Path-based analysis
  - File upload analysis
- Lightweight scoring system for quick prioritization

> [!IMPORTANT]  
> This tool is not a disassembler.  
> It is designed for **fast behavioral probing**.

---

## Use Cases

- Malware triage
- Game reverse engineering
- DLL inspection
- Quick behavioral analysis before deep dive

---

## Positioning

BinNexus.Probe fits into the workflow as:

> [!TIP]  
> A pre-analysis tool before using IDA, Ghidra or x64dbg.

---

## Future Direction

- Behavioral pattern detection (injection, beaconing, crypto usage)
- Signature-based analysis
- Integration with BinNexus ecosystem

---
