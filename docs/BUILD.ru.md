## Сборка и запуск

<div align="center" style="margin: 20px 0; padding: 10px; background: #1c1917; border-radius: 10px;">
  <strong>🌐 Язык: </strong>
  
  <span style="color: #F5F752; margin: 0 10px;">
    ✅ 🇷🇺 Русский (текущий)
  </span>
  | 
  <a href="./BUILD.md" style="color: #0891b2; margin: 0 10px;">
    🇺🇸 English
  </a>
</div>

---

### 1. Подготовка окружения

```sh
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux / Mac

pip install -r requirements.txt
```

---

### 2. Запуск веб-панели

```sh
uvicorn app.server:app --reload
```

Открыть в браузере:

```
http://127.0.0.1:8000
```

---

## Использование

- Перетащи DLL / EXE в окно
- Или укажи путь к файлу
- Выбери или создай пресет API
- Запусти анализ

> [!TIP]
> В режиме загрузки файл не обязан находиться на сервере.

---

## Конфигурация

Пример:

```json
{
	"window_size": 64,
	"step": 8,
	"output": "build/my_heatmap.json",

	"log_level": "INFO",
	"log_file": "logs/analyzer.log"
}
```
