from fastapi import APIRouter
from app.models import StatusResponse
from app.services.camera_service import camera_service
from app.database import db
import time

router = APIRouter(prefix="/status", tags=["Status"])

# Armazena tempo de início para calcular uptime
_start_time = time.time()


@router.get("", response_model=StatusResponse)
async def get_status():
    """
    Retorna o status atual do sistema.
    
    - **camera_active**: Se a câmera está ativa
    - **trained_faces_count**: Quantidade de rostos treinados
    - **last_recognition**: Timestamp do último reconhecimento (se houver)
    - **uptime_seconds**: Tempo em execução do sistema em segundos
    """
    # Busca último reconhecimento do banco
    from app.database import RecognitionLog
    session = db.get_session()
    try:
        last_log = session.query(RecognitionLog).order_by(RecognitionLog.timestamp.desc()).first()
        last_recognition = last_log.timestamp.isoformat() if last_log else None
    finally:
        session.close()
    
    uptime = time.time() - _start_time
    
    return StatusResponse(
        camera_active=camera_service.is_active(),
        trained_faces_count=db.get_trained_faces_count(),
        last_recognition=last_recognition,
        uptime_seconds=uptime
    )

