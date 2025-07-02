import requests

def obtener_dolar(fecha: str) -> str:
    """
    Consulta el valor del dólar en la fecha dada (dd-mm-yyyy) usando mindicador.cl.
    """
    url = f"https://mindicador.cl/api/dolar/{fecha}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        serie = data.get("serie")
        if not serie:
            return f"No hay datos disponibles para {fecha}."
        valor = serie[0].get("valor")
        return f"El dólar observado el {fecha} fue {valor:.2f} CLP."
    except requests.RequestException:
        return f"Error consultando dólar para {fecha}."
