from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.models import TrainRequest, TrainResponse
from app.services.face_service import face_service

router = APIRouter(prefix="/train", tags=["Training"])


@router.post("", response_model=TrainResponse)
async def train_face(
    file: UploadFile = File(...),
    name: str = Form(...),
    face_id: str = Form(None)
):
    """
    Treina um rosto com uma imagem.
    
    - **file**: Arquivo de imagem (JPG, PNG, etc.)
    - **name**: Nome da pessoa
    - **face_id**: ID opcional (será gerado automaticamente se não fornecido)
    """
    # Valida tipo de arquivo
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser uma imagem")
    
    # Lê os bytes da imagem
    image_bytes = await file.read()
    
    if len(image_bytes) == 0:
        raise HTTPException(status_code=400, detail="Arquivo vazio")
    
    # Treina o rosto
    success, message, face_id_result = face_service.train_face(
        image_bytes, name, face_id
    )
    
    if not success:
        raise HTTPException(status_code=400, detail=message)
    
    return TrainResponse(
        success=True,
        message=message,
        face_id=face_id_result
    )

