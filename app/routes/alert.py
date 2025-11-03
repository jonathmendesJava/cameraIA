from fastapi import APIRouter, HTTPException
from app.models import AlertRequest
from app.services.alert_service import alert_service

router = APIRouter(prefix="/alert", tags=["Alert"])


@router.post("", response_model=dict)
async def send_alert(request: AlertRequest):
    """
    Envia um alerta manualmente.
    
    Útil para testar integração com webhooks ou quando o frontend
    quiser acionar notificações manualmente.
    """
    success = alert_service.send_alert(
        face_id=request.face_id,
        name=request.name,
        confidence=request.confidence,
        timestamp=request.timestamp,
        webhook_url=request.webhook_url
    )
    
    return {
        "success": success,
        "message": "Alerta enviado com sucesso" if success else "Falha ao enviar alerta"
    }


@router.post("/webhook", response_model=dict)
async def set_webhook_url(webhook_url: str):
    """
    Define o webhook URL padrão para alertas.
    
    - **webhook_url**: URL do webhook para receber notificações
    """
    alert_service.default_webhook_url = webhook_url
    return {
        "success": True,
        "message": f"Webhook URL definido: {webhook_url}"
    }

