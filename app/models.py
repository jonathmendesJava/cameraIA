from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TrainRequest(BaseModel):
    name: str
    face_id: Optional[str] = None


class TrainResponse(BaseModel):
    success: bool
    message: str
    face_id: str


class RecognizedFace(BaseModel):
    name: str
    timestamp: str
    confidence: float
    face_id: str


class RecognizeResponse(BaseModel):
    status: str
    recognized_faces: List[RecognizedFace] = []


class StatusResponse(BaseModel):
    camera_active: bool
    trained_faces_count: int
    last_recognition: Optional[str] = None
    uptime_seconds: float


class AlertRequest(BaseModel):
    face_id: str
    name: str
    confidence: float
    timestamp: str
    webhook_url: Optional[str] = None

