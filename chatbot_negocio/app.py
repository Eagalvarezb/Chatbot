# app.py 
from flask import Flask, request, jsonify
from config import ConfigNegocio
from bot import ChatbotNegocio, procesar_webhook

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

@app.route('/')
def home():
    return jsonify({
        "status": "Chatbot activo",
        "negocio": ConfigNegocio.NOMBRE_NEGOCIO
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

if __name__ == '__main__':
    app.run(debug=True, port=5000)