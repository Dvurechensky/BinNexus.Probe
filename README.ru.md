<h1 align="center">BinNexus.Probe</h1>

<p align="center">
    <img src="https://shields.dvurechensky.pro/badge/Reverse-Engineering-blue">
    <img src="https://shields.dvurechensky.pro/badge/Binary-Probing-green">
    <img src="https://shields.dvurechensky.pro/badge/.NET-FastAPI-purple">
</p>

<div align="center" style="margin: 20px 0; padding: 10px; background: #1c1917; border-radius: 10px;">
  <strong>🌐 Язык: </strong>
  
  <span style="color: #F5F752; margin: 0 10px;">
    ✅ 🇷🇺 Русский (текущий)
  </span>
  | 
  <a href="./README.md" style="color: #0891b2; margin: 0 10px;">
    🇺🇸 English
  </a>
</div>

---

## Описание

**BinNexus.Probe** — инструмент для быстрого анализа бинарников на основе API-вызовов.

Позволяет понять поведение файла до полноценного реверса.

---

## Пример

<p align="center">
  <img src="media/BINNEXUS.PROBE.gif">
</p>

---

## Documents

- [Сборка](docs/BUILD.md)
- [Как использовать в x32dbg например](docs/HOW_TO_USE_x32.md)

---

## Возможности

- Поиск API-паттернов в бинарниках
- Система скоринга результатов
- Выявление поведенческих признаков (сеть, инжект, криптография)
- Быстрый анализ без дизассемблирования

---

## Зачем это нужно

Классические инструменты реверса мощные, но избыточны для быстрых проверок.

**BinNexus.Probe** делает акцент на:

> [!TIP]  
> Быстрое получение сигнала вместо глубокого анализа.

---

## Ключевые особенности

- Пресеты API (network, file system, anti-debug и др.)
- Drag & Drop загрузка бинарников
- Автоматический запуск анализа
- Два режима работы:
  - по пути к файлу
  - через загрузку файла
- Лёгкая система приоритизации результатов

> [!IMPORTANT]  
> Это не дизассемблер.  
> Это инструмент для **быстрого поведенческого анализа**.

---

## Применение

- Быстрая проверка malware
- Реверс игр
- Анализ DLL
- Предварительная оценка перед глубоким анализом

---

## Место в пайплайне

BinNexus.Probe используется как:

> [!TIP]  
> Первый шаг перед IDA / Ghidra / x64dbg.

---

## Дальнейшее развитие

- Детекция поведенческих сигнатур (инжект, beaconing, crypto)
- Расширение базы паттернов
- Интеграция с BinNexus

---
