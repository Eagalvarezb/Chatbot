import requests
import json
from flask import request, Response
from config import ConfigNegocio

# Configuración de Whapi
WHAPI_TOKEN = ConfigNegocio.WHAPI_TOKEN  # Agrega esto a tu config.py
WHAPI_BASE = "https://gate.whapi.cloud"

def enviar_whatsapp(numero_destino: str, mensaje: str):
    """Envía mensaje usando Whapi.Cloud (similar a Twilio pero más simple)"""
    url = f"{WHAPI_BASE}/messages/text"
    
    # Limpiar número: eliminar '+' si existe
    numero_clean = numero_destino.replace('+', '')
    
    payload = {
        "to": numero_clean,
        "body": mensaje
    }
    
    headers = {
        "Authorization": f"Bearer {WHAPI_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        if response.status_code == 401:
            print(" Error de autenticación: Token inválido")
        elif response.status_code == 429:
            print(" Límite de tasa excedido")
        return response.json()
    except Exception as e:
        print(f"Error enviando mensaje: {e}")
        return None

def procesar_webhook(data: dict, bot, datos_negocio: dict):
    """
    Procesa mensajes entrantes de WhatsApp vía webhook.
    Whapi.Cloud envía los mensajes en un formato específico.
    """
    # El formato de Whapi es diferente al de Twilio
    # Los mensajes entrantes vienen en data["messages"]
    messages = data.get("messages", [])
    
    if not messages:
        return {"status": "ok", "message": "No messages"}
    
    for msg in messages:
        # Extraer información del mensaje
        numero = msg.get("from", "")  # Quien envía
        texto = msg.get("text", {}).get("body", "")  # El mensaje
        chat_id = msg.get("chat", {}).get("id", numero)
        
        if not texto:
            continue
        
        # Procesar con tu chatbot existente
        resultado = bot.responder(chat_id, texto, datos_negocio)
        
        # Enviar respuesta
        enviar_whatsapp(numero, resultado["respuesta"])
    
    return {"status": "ok", "processed": len(messages)}