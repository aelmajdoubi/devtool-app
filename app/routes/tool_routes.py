from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import subprocess
import tempfile
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/", response_class=HTMLResponse)
async def tool_get(request: Request):
    return templates.TemplateResponse("tool.html", {"request": request, "code": "", "output": ""})

@router.post("/", response_class=HTMLResponse)
async def tool_post(request: Request, code: str = Form(...), action: str = Form(...)):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
        f.write(code)
        temp_path = f.name

    if action == "Format":
        subprocess.run(["black", temp_path, "--quiet"])
        with open(temp_path, "r") as f:
            result = f.read()
        output = "✅ Code formatiert"
    elif action == "Lint":
        result = code
        lint_output = subprocess.run(["flake8", temp_path], capture_output=True, text=True)
        output = lint_output.stdout or "✅ Keine Fehler gefunden"
    else:
        result = code
        output = "❌ Ungültige Aktion"

    os.unlink(temp_path)

    return templates.TemplateResponse("tool.html", {
        "request": request,
        "code": result,
        "output": output
    })
