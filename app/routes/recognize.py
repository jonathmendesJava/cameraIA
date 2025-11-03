from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models import RecognizedFace, RecognizeResponse
from app.services.face_service import face_service
from app.services.camera_service import camera_service
from datetime import datetime

router = APIRouter(prefix="/recognize", tags=["Recognition"])


@router.post("/image", response_model=RecognizeResponse)
async def recognize_from_image(file: UploadFile = File(...)):
    """
    Reconhece faces em uma imagem enviada.
    
    - **file**: Arquivo de imagem (JPG, PNG, etc.)
    """
    # Valida tipo de arquivo
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem")
    
    # Lê os bytes da imagem
    image_bytes = await file.read()
    
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Arquivo vazio")
    
    # Reconhece faces
    recognized = face_service.recognize_face(image_bytes)
    
    recognized_faces = [
        RecognizedFace(
            name=name,
            timestamp=datetime.utcnow().isoformat(),
            confidence=confidence,
            face_id=face_id
        )
        for face_id, name, confidence in recognized
    ]
    
    return RecognizeResponse(
        status="completed",
        recognized_faces=recognized_faces
    )


@router.post("/start", response_model=RecognizeResponse)
async def start_recognition():
    """
    Inicia o reconhecimento em tempo real via câmera.
    """
    if camera_service.is_active():
        return RecognizeResponse(
            status="already_active",
            recognized_faces=[]
        )
    
    success = camera_service.start()
    
    if not success:
        raise HTTPException(
            status_code=500,
            detail="Não foi possível iniciar a câmera. Verifique se a câmera está conectada e não está sendo usada por outro aplicativo."
        )
    
    return RecognizeResponse(
        status="active",
        recognized_faces=[]
    )


@router.post("/stop", response_model=RecognizeResponse)
async def stop_recognition():
    """
    Para o reconhecimento em tempo real.
    """
    camera_service.stop()
    return RecognizeResponse(
        status="inactive",
        recognized_faces=[]
    )


@router.get("/stream-status", response_model=RecognizeResponse)
async def get_stream_status():
    """
    Retorna o status atual do reconhecimento em tempo real.
    """
    status = "active" if camera_service.is_active() else "inactive"
    return RecognizeResponse(
        status=status,
        recognized_faces=[]
    )

