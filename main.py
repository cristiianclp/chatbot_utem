from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelo
model = OllamaLLM(model="deepseek-r1:7b")
prompt_template = """
Eres un asistente en español. Responde de forma clara y concisa.

Pregunta: {question}
Respuesta:
"""
prompt = ChatPromptTemplate.from_template(prompt_template)
chain = prompt | model

class Consulta(BaseModel):
    pregunta: str

@app.post("/consultar")
def consultar(data: Consulta):
    respuesta = chain.invoke({"question": data.pregunta})
    texto = respuesta.strip().split("<|im_end|>")[0].split("<|assistant|>")[-1].strip()
    return {"respuesta": texto}

# Servir HTML estático
@app.get("/", response_class=HTMLResponse)
def index():
    return FileResponse("index.html")
