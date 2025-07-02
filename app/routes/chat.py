from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import ollama
import json
from app.utils.obtener_dolar import obtener_dolar

router = APIRouter()

# Tool para consultar dólar
def consultar_dolar(fecha: str) -> str:
    """
    Consulta el valor del dólar de una fecha en formato dd-mm-yyyy.
    """
    return obtener_dolar(fecha)

class Consulta(BaseModel):
    pregunta: str

@router.post("/consultar")
async def consultar(data: Consulta):
    try:
        system_prompt = (
            "Eres un asistente educativo en español. "
            "Si el usuario pregunta por el valor del dólar en una fecha específica, "
            "usa SIEMPRE la herramienta 'consultar_dolar' con el parámetro 'fecha'. "
            "No expliques ni estimes valores, usa la herramienta si corresponde."
        )

        response = ollama.chat(
            model="granite3.2:2b",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": data.pregunta}
            ],
            tools=[{
                "name": "consultar_dolar",
                "description": "Consulta el valor del dólar para una fecha en formato dd-mm-yyyy.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "fecha": {
                            "type": "string",
                            "description": "Fecha en formato dd-mm-yyyy"
                        }
                    },
                    "required": ["fecha"]
                }
            }]
        )

        # Verifica si se invocó el tool
        if "tool_calls" in response["message"]:
            tool_calls = response["message"]["tool_calls"]
            for call in tool_calls:
                if call["name"] == "consultar_dolar":
                    argumentos = json.loads(call["arguments"])
                    fecha = argumentos.get("fecha")
                    if fecha:
                        resultado = consultar_dolar(fecha)
                        return {"respuesta": resultado}

        # Respuesta normal si no hay tool calling
        return {"respuesta": response["message"]["content"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando la consulta: {str(e)}")
