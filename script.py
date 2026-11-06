import os
import datetime
from google import genai
from google.genai import types

# Lista de empresas o analistas a supervisar
EMPRESAS = [
"NKE","ADBE","SCL","CLX","FUL","BYD","DGE.L","TRU","DNR.MI","NESN.SW","TATE.L","RENK","HTO","PLX","XNYS:PNR","EFX","EXO","AON","BKNG","WKL.AS","SIKA.SW",
]

HOY = datetime.date.today().strftime("%Y-%m-%d")

# Inicializa el cliente usando la variable de entorno
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

def escanear_novedades(empresa):
    prompt = f"""
    Realiza una búsqueda web exhaustiva sobre la empresa o analista '{empresa}' para las últimas 24-48 horas ({HOY}).
    
    Busca específicamente:
    1. Publicación de resultados trimestrales/anuales o revisiones de estimaciones (guidance).
    2. Hechos relevantes corporativos, compras/adquisiciones o dividendos.
    3. Cambios notables de recomendación o precio objetivo por analistas.

    Genera un informe ejecutivo conciso en español.
    Si no hay novedades relevantes en las últimas 48h, responde únicamente: "Sin novedades relevantes".
    """
    
    try:
        response = client.models.generate_content(
            model='gemini-3.8-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=[{"google_search": {}}]
            )
        )
        return response.text
    except Exception as e:
        return f"Error al consultar {empresa}: {str(e)}"

if __name__ == "__main__":
    print(f"=== INFORME DIARIO DE CARTERA - {HOY} ===")
    for item in EMPRESAS:
        print(f"\n### {item}")
        resumen = escanear_novedades(item)
        print(resumen)
