from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import openai
import os

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

openai.api_key = os.getenv("OPENAI_API_KEY")

@router.get("/", response_class=HTMLResponse)
async def form_get(request: Request):
    return templates.TemplateResponse("code_helper.html", {"request": request, "result": None})

@router.post("/", response_class=HTMLResponse)
async def form_post(request: Request, code_input: str = Form(...)):
    prompt = f"Erkläre den folgenden Python-Code und schlage Verbesserungen vor:\n\n{code_input}"
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message["content"].strip()
    except Exception as e:
        result = f"Fehler bei der KI-Anfrage: {e}"

    return templates.TemplateResponse("code_helper.html", {
        "request": request,
        "result": result,
        "code_input": code_input
    })
