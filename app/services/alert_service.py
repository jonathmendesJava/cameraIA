import httpx
from typing import Optional, Dict
import os


class AlertService:
    def __init__(self):
        self.default_webhook_url = os.getenv("WEBHOOK_URL", "")
        self.enabled = True
    
    def send_alert(
        self,
        face_id: str,
        name: str,
        confidence: float,
        timestamp: str,
        webhook_url: Optional[str] = None
    ) -> bool:
        """
        Envia alerta quando uma face é reconhecida.
        Retorna True se enviado com sucesso.
        """
        if not self.enabled:
            return False
        
        url = webhook_url or self.default_webhook_url
        
        if not url:
            # Sem webhook configurado, apenas log
            print(f"🚨 ALERTA: {name} (ID: {face_id}) reconhecido com {confidence:.2%} de confiança às {timestamp}")
            return False
        
        try:
            payload = {
                "event": "face_recognized",
                "face_id": face_id,
                "name": name,
                "confidence": confidence,
                "timestamp": timestamp
            }
            
            with httpx.Client(timeout=5.0) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                return True
                
        except Exception as e:
            print(f"Erro ao enviar alerta: {str(e)}")
            return False
    
    def send_custom_alert(self, webhook_url: str, payload: Dict) -> bool:
        """Envia um alerta customizado para um webhook específico"""
        try:
            with httpx.Client(timeout=5.0) as client:
                response = client.post(webhook_url, json=payload)
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"Erro ao enviar alerta customizado: {str(e)}")
            return False


# Singleton instance
alert_service = AlertService()

