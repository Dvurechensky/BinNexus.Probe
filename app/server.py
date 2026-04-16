import tempfile
import json

from pathlib import Path

from fastapi import Body, FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from app.conf import DEFAULT_CONFIG, ensure_output_path
from app.core.analizer import analyze_network_with_custom_apis
from app.core.logging import setup_logging, get_logger
from fastapi import UploadFile, File, Form

from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]  # <-- самый надёжный вариант

WEB_DIR = ROOT_DIR / "web"
STATIC_DIR = WEB_DIR / "static"
TEMPLATES_DIR = WEB_DIR / "templates"
PRESETS_FILE = STATIC_DIR / "presets.json"

print("ROOT_DIR =", ROOT_DIR)
print("STATIC_DIR =", STATIC_DIR)
print("STATIC EXISTS =", STATIC_DIR.exists())

ensure_output_path(str(ROOT_DIR / "build" / "dummy.txt"))
ensure_output_path(str(ROOT_DIR / "logs" / "analyzer.log"))

setup_logging(
    level=DEFAULT_CONFIG["log_level"],
    log_file=DEFAULT_CONFIG["log_file"],
)

log = get_logger("web")

app = FastAPI(title="ReverseAI Panel")

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


class AnalyzeRequest(BaseModel):
    path: str
    apis: list[str]


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "default_apis": "\n".join([
                "send",
                "recv",
                "connect",
                "WSASend",
                "WSARecv",
                "HttpSendRequest",
                "WinHttpSendRequest",
                "InternetReadFile",
                "InternetWriteFile",
            ])
        }
    )


@app.post("/api/analyze")
async def analyze(
    file: UploadFile = File(None),
    apis: str = Form(None),
    path: str = Form(None)
):
    try:
        # если пришёл файл
        if file:
            content = await file.read()

            # сохраняем во временный файл
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(content)
                tmp_path = tmp.name

            apis_list = json.loads(apis or "[]")
            cleaned_apis = [x.strip() for x in apis_list if x.strip()]

            results = analyze_network_with_custom_apis(
                path=tmp_path,
                apis=cleaned_apis,
            )

        # если пришёл путь (старый режим)
        else:
            if not path:
                return JSONResponse(
                    status_code=400,
                    content={"error": "Path is empty."},
                )

            apis_list = json.loads(apis or "[]")
            cleaned_apis = [x.strip() for x in apis_list if x.strip()]

            results = analyze_network_with_custom_apis(
                path=path.strip(),
                apis=cleaned_apis,
            )

        return {
            "ok": True,
            "count": len(results),
            "results": results,
        }

    except Exception as e:
        log.exception("Analyze failed")
        return JSONResponse(
            status_code=500,
            content={"error": str(e)},
        )
    
@app.post("/api/presets/save")
async def save_preset(data: dict = Body(...)):
    try:
        name = data.get("name")
        apis = data.get("apis")

        if not name or not apis:
            return {"error": "Invalid data"}

        # загрузить текущие
        if PRESETS_FILE.exists():
            with open(PRESETS_FILE, "r", encoding="utf-8") as f:
                presets = json.load(f)
        else:
            presets = {}

        # добавить новый
        key = name.lower().replace(" ", "_")

        presets[key] = {
            "title": name,
            "apis": apis,
        }

        # сохранить
        with open(PRESETS_FILE, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2)

        return {"ok": True}

    except Exception as e:
        log.exception("Save preset failed")
        return {"error": str(e)}  
    

@app.post("/api/presets/delete")
async def delete_preset(data: dict = Body(...)):
    try:
        key = data.get("key")
        if not key:
            return {"error": "No key provided"}

        if PRESETS_FILE.exists():
            with open(PRESETS_FILE, "r", encoding="utf-8") as f:
                presets = json.load(f)
        else:
            return {"error": "No presets file"}

        if key not in presets:
            return {"error": "Preset not found"}

        del presets[key]

        with open(PRESETS_FILE, "w", encoding="utf-8") as f:
            json.dump(presets, f, indent=2)

        return {"ok": True}

    except Exception as e:
        log.exception("Delete preset failed")
        return {"error": str(e)}