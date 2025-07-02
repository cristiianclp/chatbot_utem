async function consultar() {
    const pregunta = document.getElementById("pregunta").value;
    const respuestaDiv = document.getElementById("respuesta");
    respuestaDiv.textContent = "Consultando...";

    try {
        const res = await fetch("/consultar", { // se usa ruta relativa
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ pregunta })
        });

        if (!res.ok) {
            throw new Error("Error en la consulta");
        }

        const data = await res.json();
        respuestaDiv.textContent = data.respuesta;
    } catch (error) {
        respuestaDiv.textContent = "Error: " + error.message;
    }
}
