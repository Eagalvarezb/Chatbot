import json
from datetime import datetime
from pathlib import Path

class ChatbotNegocio:
    def __init__(self):
        self.sesiones = {}
        self.config = self._cargar_config()
    
    def _cargar_config(self):
        """Carga palabras clave y mensajes desde JSON"""
        ruta = Path(__file__).parent.parent / "respuestas.json"
        with open(ruta, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def detectar_intencion(self, mensaje: str) -> str:
        mensaje = mensaje.lower().strip()
        
        palabras = self.config["palabras_clave"]
        
        # Coincidencia exacta
        if mensaje in palabras:
            return palabras[mensaje]
        
        # Coincidencia parcial
        for palabra, intencion in palabras.items():
            if palabra in mensaje:
                return intencion
        
        return "no_entendi"
    
    def obtener_mensaje(self, intencion: str, datos_negocio: dict) -> str:
        """Obtiene mensaje y reemplaza variables"""
        mensaje = self.config["mensajes"].get(intencion, self.config["mensajes"]["no_entendi"])
        
        # Reemplazar variables dinámicas
        mensaje = mensaje.format(
            nombre=datos_negocio.get("nombre", "Tu Empresa"),
            horario=datos_negocio.get("horario", ""),
            whatsapp=datos_negocio.get("whatsapp", ""),
            email=datos_negocio.get("email", "")
        )
        return mensaje
    
    def responder(self, usuario_id: str, mensaje: str, datos_negocio: dict) -> dict:
        # Primera vez = bienvenida
        if usuario_id not in self.sesiones:
            self.sesiones[usuario_id] = {
                "inicio": datetime.now().isoformat(),
                "mensajes": 0,
                "ultima_intencion": None
            }
            return {
                "respuesta": self.obtener_mensaje("bienvenida", datos_negocio),
                "tipo": "bienvenida",
                "escalar": False
            }
        
        self.sesiones[usuario_id]["mensajes"] += 1
        
        intencion = self.detectar_intencion(mensaje)
        self.sesiones[usuario_id]["ultima_intencion"] = intencion
        
        # Escalar si pide humano o lleva muchos mensajes
        escalar = (intencion == "escalamiento" or 
                   self.sesiones[usuario_id]["mensajes"] > 5)
        
        return {
            "respuesta": self.obtener_mensaje(intencion, datos_negocio),
            "tipo": intencion,
            "escalar": escalar,
            "metadata": self.sesiones[usuario_id]
        }
    
    def get_estadisticas(self):
        total_usuarios = len(self.sesiones)
        total_mensajes = sum(s["mensajes"] for s in self.sesiones.values())
        return {
            "usuarios_activos": total_usuarios,
            "total_mensajes": total_mensajes,
            "sesiones": self.sesiones
        }