## Build & Run

<div align="center" style="margin: 20px 0; padding: 10px; background: #1c1917; border-radius: 10px;">
  <strong>🌐 Language: </strong>
  
  <a href="./BUILD.ru.md" style="color: #F5F752; margin: 0 10px;">
    🇷🇺 Russian
  </a>
  | 
  <span style="color: #0891b2; margin: 0 10px;">
    ✅ 🇺🇸 English (current)
  </span>
</div>

---

### 1. Setup environment

```sh
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # Linux / Mac

pip install -r requirements.txt
```

---

### 2. Run web panel

```sh
uvicorn app.server:app --reload
```

Open in browser:

```
http://127.0.0.1:8000
```

---

## Usage

- Drag & drop a DLL / EXE into the panel
- Or provide a local file path
- Select or create API presets
- Run analysis

> [!TIP]
> File upload mode does not require the file to exist on the server.

---

## Configuration

Example configuration:

```json
{
	"window_size": 64,
	"step": 8,
	"output": "build/my_heatmap.json",

	"log_level": "INFO",
	"log_file": "logs/analyzer.log"
}
```
