import os

class ConfigNegocio:
    """Configuración básica del negocio"""
    NOMBRE_NEGOCIO = os.environ.get('NOMBRE_NEGOCIO', 'Tu Empresa')
    HORARIO_ATENCION = os.environ.get('HORARIO_ATENCION', 'Lunes a Viernes 8:00 - 18:00')
    WHATSAPP_NUMERO = os.environ.get('WHATSAPP_NUMERO', '+502 1234-5678')
    EMAIL = os.environ.get('EMAIL', 'contacto@tuempresa.com')
    
    # Credenciales Twilio (¡importante usar variables de entorno!)
    TWILIO_SID = os.environ.get('TWILIO_SID', '')
    TWILIO_TOKEN = os.environ.get('TWILIO_TOKEN', '')
    TWILIO_NUMERO = os.environ.get('TWILIO_NUMERO', 'whatsapp:+14155238886')