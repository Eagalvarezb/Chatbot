# app.py 
from flask import Flask, request, jsonify
from config import ConfigNegocio
from respuestas import ChatbotNegocio
from webhook import procesar_webhook

app = Flask(__name__)

# Inicializar bot
bot = ChatbotNegocio()

# Datos del negocio para reemplazar en mensajes
datos_negocio = {
    "nombre": ConfigNegocio.NOMBRE_NEGOCIO,
    "horario": ConfigNegocio.HORARIO_ATENCION,
    "whatsapp": ConfigNegocio.WHATSAPP_NUMERO,
    "email": ConfigNegocio.EMAIL
}

@app.route('/', methods=['GET', 'POST'])  
def home():
    if request.method == 'POST':
        # Si Whapi envía POST a /, procesarlo como webhook
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        if data:
            resultado = procesar_webhook(data, bot, datos_negocio)
            return jsonify(resultado)
        else:
            return jsonify({"status": "No data received"}), 200
    
    # GET request - mostrar estado
    return jsonify({
        "status": "Chatbot activo",
        "negocio": ConfigNegocio.NOMBRE_NEGOCIO,
        "webhook_url": "/webhook",
        "info": "Usa POST a /webhook para los mensajes"
    })

@app.route('/webhook', methods=['POST'])
def webhook():
    """Recibe mensajes de WhatsApp/Facebook/Instagram"""
    # Manejar JSON o form data de Twilio
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form.to_dict()
    
    # Si no hay datos, devolver error
    if not data:
        return jsonify({"error": "No se recibieron datos"}), 400
    
    resultado = procesar_webhook(data, bot, datos_negocio)
    return jsonify(resultado)

@app.route('/api/chat', methods=['POST'])
def api_chat():
    """API REST para web/chat embebido"""
    if not request.is_json:
        return jsonify({"error": "Se requiere Content-Type: application/json"}), 400
    
    data = request.get_json()
    usuario_id = data.get('usuario_id', 'web_user')
    mensaje = data.get('mensaje', '')
    
    if not mensaje:
        return jsonify({"error": "El campo 'mensaje' es requerido"}), 400
    
    resultado = bot.responder(usuario_id, mensaje, datos_negocio)
    return jsonify(resultado)

@app.route('/admin/estadisticas', methods=['GET'])
def estadisticas():
    """Dashboard del cliente"""
    return jsonify(bot.get_estadisticas())

@app.route('/admin/config', methods=['GET'])
def ver_config():
    """Ver configuración actual"""
    return jsonify({
        "negocio": ConfigNegocio.NOMBRE_NEGOCIO,
        "horario": ConfigNegocio.HORARIO_ATENCION,
        "whatsapp": ConfigNegocio.WHATSAPP_NUMERO
    })

@app.route('/health', methods=['GET'])
def health():
    """Health check para Render"""
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
