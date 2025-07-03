from flask import Blueprint, request, jsonify, session
import ollama

chat_bp = Blueprint('chat_bp', __name__)

MODEL_NAME = "granite3.2:2b"

@chat_bp.route('/consultar', methods=['POST'])
def consultar():
    data = request.get_json()
    pregunta = data.get('pregunta', '')

    if 'chat_history' not in session:
        session['chat_history'] = [
            {
                "role": "system",
                "content":
                    "Eres un chatbot conversacional institucional de la Universidad Tecnológica Metropolitana (UTEM), especializado en brindar orientación y asistencia a estudiantes sobre el proceso de inscripción de asignaturas y matrícula, operando como asistente de SISEI de la UTEM. "
                    "Responde de forma clara, breve y en español, adaptando el nivel de detalle según la consulta, utilizando un lenguaje cordial y educativo. "
                    "Puedes guiar paso a paso a los estudiantes sobre temas como fechas de inscripción y matrícula, reglas de inscripción, reglas de los tres niveles, tramos de inscripción, recuperación de clave, requisitos y documentos necesarios, problemas comunes en el sistema de inscripción y orientación general sobre procesos administrativos. "
                    "Si una consulta no está relacionada con inscripción o matrícula, indícalo amablemente y sugiere al estudiante comunicarse con la unidad correspondiente. "
                    "No realices acciones administrativas ni confirmes estados académicos específicos, tu rol es informativo y orientativo. "
                    "Cuando respondas, utiliza ejemplos si es necesario para facilitar la comprensión del estudiante. "
                    "Si el estudiante saluda o realiza consultas generales, responde de forma cálida, fomentando la confianza en el uso del sistema."
            }
        ]

    chat_history = session['chat_history']
    chat_history.append({"role": "user", "content": pregunta})

    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=chat_history
        )
        respuesta_modelo = response["message"]["content"]

        chat_history.append({"role": "assistant", "content": respuesta_modelo})
        session['chat_history'] = chat_history

        return jsonify({"respuesta": respuesta_modelo})

    except Exception as e:
        return jsonify({"error": f"Error procesando la consulta: {str(e)}"}), 500
