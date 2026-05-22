import os

class ConfigNegocio:
    """Configuración básica del negocio"""
    NOMBRE_NEGOCIO = os.environ.get('NOMBRE_NEGOCIO', 'Tu Empresa')
    HORARIO_ATENCION = os.environ.get('HORARIO_ATENCION', 'Lunes a Viernes 8:00 - 18:00')
    WHATSAPP_NUMERO = os.environ.get('WHATSAPP_NUMERO', '+502 1234-5678')
    EMAIL = os.environ.get('EMAIL', 'contacto@tuempresa.com')
    
    # Credenciales Twilio (¡importante usar variables de entorno!)
    WHAPI_TOKEN ="5fzqdjXdfFhupFynlu6GItXlODakIjrz"
