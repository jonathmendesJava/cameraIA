from fastapi import FastAPI, Request, HTTPException, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import APIKeyHeader
from app.routes import train, recognize, status, alert, faces
from app.services.camera_service import camera_service
from app.services.alert_service import alert_service
from app.database import db
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Face Recognition API",
    description="API para reconhecimento facial em tempo real",
    version="1.0.0"
)

# Configuração CORS (permitir requisições do frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Segurança via API Key
API_KEY = os.getenv("API_KEY", "your-secret-api-key-123")
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def verify_api_key(request: Request, api_key: str = Security(api_key_header)):
    """Verifica se a API key é válida"""
    if not api_key or api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API key inválida ou ausente. Forneça o header 'x-api-key'."
        )
    return api_key


# Inclui rotas
app.include_router(train.router, dependencies=[Security(verify_api_key)])
app.include_router(recognize.router, dependencies=[Security(verify_api_key)])
app.include_router(status.router)  # Status pode ser público ou protegido conforme necessário
app.include_router(alert.router, dependencies=[Security(verify_api_key)])
app.include_router(faces.router, dependencies=[Security(verify_api_key)])


# Callback para quando uma face é reconhecida
def on_face_recognized(data: dict):
    """Callback chamado quando uma face é reconhecida pela câmera"""
    alert_service.send_alert(
        face_id=data["face_id"],
        name=data["name"],
        confidence=data["confidence"],
        timestamp=data["timestamp"]
    )


# Configura callback
camera_service.set_on_face_recognized_callback(on_face_recognized)


@app.on_event("startup")
async def startup_event():
    """Executado quando o servidor inicia"""
    from app.utils import FACE_RECOGNITION_AVAILABLE
    
    print("🚀 Face Recognition API iniciada!")
    
    if not FACE_RECOGNITION_AVAILABLE:
        print("⚠️  AVISO: face-recognition não está instalado!")
        print("   Para instalar:")
        print("   1. Instale CMake: https://cmake.org/download/")
        print("   2. Instale Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/")
        print("   3. Execute: pip install dlib face-recognition==1.3.0")
        print("   OU execute: .\\install-face-recognition.ps1")
    else:
        print("✅ face-recognition disponível!")
    
    print(f"📊 Rostos treinados: {db.get_trained_faces_count()}")


@app.on_event("shutdown")
async def shutdown_event():
    """Executado quando o servidor é encerrado"""
    camera_service.stop()
    print("👋 Face Recognition API encerrada")


@app.get("/")
async def root():
    """Endpoint raiz com informações da API"""
    return {
        "message": "Face Recognition API",
        "version": "1.0.0",
        "docs": "/docs",
        "endpoints": {
            "train": "/train",
            "recognize": "/recognize",
            "status": "/status",
            "alert": "/alert"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

