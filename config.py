import os
from dotenv import load_dotenv

load_dotenv()

class ConfigNegocio:
    """Configuración básica del negocio"""
    NOMBRE_NEGOCIO = os.environ.get('NOMBRE_NEGOCIO', 'Tu Empresa')
    HORARIO_ATENCION = os.environ.get('HORARIO_ATENCION', 'Lunes a Viernes 8:00 - 18:00')
    WHATSAPP_NUMERO = os.environ.get('WHATSAPP_NUMERO', '+502 1234-5678')
    EMAIL = os.environ.get('EMAIL', 'contacto@tuempresa.com')
    
    # Credenciales 
    WHAPI_TOKEN = os.environ.get('WHAPI_TOKEN', '')
    
    if not WHAPI_TOKEN:
        raise ValueError(" WHAPI_TOKEN no está configurado en variables de entorno")
