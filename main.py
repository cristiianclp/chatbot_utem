from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import uvicorn

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar carpeta static
app.mount("/static", StaticFiles(directory="static"), name="static")

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
async def consultar(data: Consulta):
    try:
        respuesta = chain.invoke({"question": data.pregunta})
        texto = respuesta.strip().split("<|im_end|>")[0].split("<|assistant|>")[-1].strip()
        print(f"Pregunta: {data.pregunta}\nRespuesta: {texto}")
        return {"respuesta": texto}
    except Exception as e:
        print(f"Error procesando la consulta: {e}")
        raise HTTPException(status_code=500, detail="Error procesando la consulta")

@app.get("/")
async def root():
    return FileResponse("index.html")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
