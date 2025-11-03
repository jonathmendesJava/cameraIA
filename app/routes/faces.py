from fastapi import APIRouter, HTTPException, Query, Body
from app.database import db
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/faces", tags=["Faces Management"])


class UpdateNameRequest(BaseModel):
    new_name: str


@router.get("")
async def list_all_faces():
    """
    Lista todos os rostos treinados com estatísticas.
    """
    try:
        faces = db.get_all_faces_with_stats()
        return {
            "success": True,
            "count": len(faces),
            "faces": faces
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar rostos: {str(e)}")


@router.get("/{face_id}")
async def get_face_details(face_id: str):
    """
    Obtém detalhes de um rosto específico.
    """
    face = db.get_trained_face_by_id(face_id)
    if not face:
        raise HTTPException(status_code=404, detail="Rosto não encontrado")
    
    # Busca estatísticas
    recognition_count = len(db.get_recognition_history(face_id=face_id))
    last_recognition = db.get_recognition_history(face_id=face_id, limit=1)
    
    return {
        "success": True,
        "face_id": face.face_id,
        "name": face.name,
        "created_at": face.created_at.isoformat(),
        "last_seen": face.last_seen.isoformat() if face.last_seen else None,
        "recognition_count": recognition_count,
        "last_recognition": {
            "timestamp": last_recognition[0].timestamp.isoformat(),
            "confidence": last_recognition[0].confidence
        } if last_recognition else None
    }


@router.delete("/{face_id}")
async def delete_face(face_id: str):
    """
    Remove um rosto treinado.
    """
    success = db.delete_trained_face(face_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rosto não encontrado")
    
    return {
        "success": True,
        "message": f"Rosto {face_id} removido com sucesso"
    }


@router.patch("/{face_id}/name")
async def update_face_name(face_id: str, request: UpdateNameRequest):
    """
    Atualiza o nome de um rosto.
    """
    success = db.update_face_name(face_id, request.new_name)
    if not success:
        raise HTTPException(status_code=404, detail="Rosto não encontrado")
    
    return {
        "success": True,
        "message": f"Nome do rosto {face_id} atualizado para {request.new_name}"
    }


@router.get("/{face_id}/history")
async def get_face_history(
    face_id: str,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """
    Obtém o histórico de reconhecimentos de um rosto.
    """
    # Verifica se o rosto existe
    face = db.get_trained_face_by_id(face_id)
    if not face:
        raise HTTPException(status_code=404, detail="Rosto não encontrado")
    
    history = db.get_recognition_history(face_id=face_id, limit=limit, offset=offset)
    
    return {
        "success": True,
        "face_id": face_id,
        "count": len(history),
        "history": [
            {
                "timestamp": log.timestamp.isoformat(),
                "confidence": log.confidence,
                "name": log.name
            }
            for log in history
        ]
    }


@router.get("/stats/overview")
async def get_overview_stats(days: int = Query(7, ge=1, le=365)):
    """
    Obtém estatísticas gerais do sistema.
    """
    try:
        stats = db.get_recognition_stats(days=days)
        total_faces = db.get_trained_faces_count()
        
        return {
            "success": True,
            "total_trained_faces": total_faces,
            "recognition_stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter estatísticas: {str(e)}")


@router.post("/cleanup")
async def cleanup_old_logs(days: int = 30):
    """
    Remove logs antigos (manutenção do banco de dados).
    """
    try:
        deleted = db.cleanup_old_logs(days=days)
        return {
            "success": True,
            "message": f"Removidos {deleted} logs antigos (mais de {days} dias)",
            "deleted_count": deleted
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao limpar logs: {str(e)}")
