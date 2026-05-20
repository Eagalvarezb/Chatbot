from twilio.rest import Client
import sys
import os

# Añadir el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ConfigNegocio

def enviar_whatsapp(numero_destino: str, mensaje: str):
    """Envía mensaje por WhatsApp usando Twilio"""
    if ConfigNegocio.TWILIO_SID == "tu_sid_aqui":
        print(f"[MOCK] Enviando WhatsApp a {numero_destino}: {mensaje[:50]}...")
        return "mock_sid_123"
    
    client = Client(ConfigNegocio.TWILIO_SID, ConfigNegocio.TWILIO_TOKEN)
    
    message = client.messages.create(
        from_=ConfigNegocio.TWILIO_NUMERO,
        body=mensaje,
        to=f'whatsapp:{numero_destino}'
    )
    return message.sid

def procesar_webhook(data: dict, bot, datos_negocio: dict):
    """Procesa mensajes entrantes de WhatsApp/Facebook"""
    # Extraer según plataforma
    usuario_id = data.get('From', data.get('from', 'anonimo'))
    mensaje = data.get('Body', data.get('message', ''))
    plataforma = data.get('platform', 'whatsapp')
    
    # Limpiar número de teléfono si viene con prefijo
    if usuario_id.startswith('whatsapp:'):
        usuario_id = usuario_id.replace('whatsapp:', '')
    
    if not mensaje:
        return {"status": "error", "error": "No se recibió mensaje"}
    
    # Procesar con el bot
    resultado = bot.responder(usuario_id, mensaje, datos_negocio)
    
    # Enviar respuesta por WhatsApp si es necesario
    if plataforma == 'whatsapp' and not resultado.get('escalar'):
        enviar_whatsapp(usuario_id, resultado['respuesta'])
    
    return {
        "status": "ok",
        "respuesta": resultado["respuesta"],
        "escalar": resultado["escalar"],
        "plataforma": plataforma
    }