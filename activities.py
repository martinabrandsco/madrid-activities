import requests
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# CONFIGURA TUS CREDENCIALES
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# PREGUNTA A PERPLEXITY
def get_perplexity_response(query):
    headers = {
        "Authorization": f"Bearer {PERPLEXITY_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "user", "content": query}
        ],
        "temperature": 0.7
    }

    response = requests.post("https://api.perplexity.ai/chat/completions", json=payload, headers=headers)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

# ENVÍA MENSAJE POR TELEGRAM
def send_telegram_message(text):
    # Split message into chunks of 4000 characters (leaving some margin)
    max_length = 4000
    chunks = [text[i:i + max_length] for i in range(0, len(text), max_length)]
    
    for chunk in chunks:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "Markdown"
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
    
    return {"ok": True}  # Return success if all chunks were sent

def clean_response(text):
    # Remove content between <think> tags
    cleaned_text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
    # Remove any extra whitespace that might be left
    cleaned_text = re.sub(r'\n\s*\n', '\n\n', cleaned_text)
    return cleaned_text.strip()

# PREGUNTA ESPECÍFICA
query = """
Haz un research actualizado de las actividades y eventos culturales, gastronómicos o de ocio que se celebran esta semana en Madrid, España.

Utiliza como mínimo estas tres fuentes: https://feverup.com/es/madrid, https://madridsecreto.co/ y https://madriddiferente.com/, además de otras fuentes locales fiables si es necesario.

Clasifica los eventos en dos grupos:
- Entre semana (lunes a viernes)
- Fin de semana (sábado y domingo)

Crea un resumen breve, visual y amigable (máx. 10 líneas), con emojis y un enlace por cada actividad para más información o reserva.

Añade también una sección con 2 o 3 eventos importantes o destacados que se celebran durante este mes en Madrid, para no perder la oportunidad de comprar entradas con antelación.

Al final, añade una sección con 2 o 3 eventos importantes o destacados que se celebrarán en los próximos 6 meses en Madrid, para no perder la oportunidad de comprar entradas con antelación.

La respuesta debe estar lista para enviar por Telegram: formato claro, directo y bien organizado.




"""

# EJECUCIÓN
try:
    respuesta = get_perplexity_response(query)
    cleaned_respuesta = clean_response(respuesta)
    send_telegram_message(cleaned_respuesta)
    print("✅ Mensaje enviado por Telegram.")
except requests.exceptions.HTTPError as e:
    if e.response is not None:
        print(f"❌ Error: {e}\nResponse content: {e.response.text}")
    else:
        print(f"❌ Error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
