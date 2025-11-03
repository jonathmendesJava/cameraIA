import json
import numpy as np
from typing import List, Tuple
from PIL import Image
import io

# Tenta importar face_recognition, se não estiver disponível mostra erro claro
try:
    import face_recognition
    FACE_RECOGNITION_AVAILABLE = True
except ImportError:
    FACE_RECOGNITION_AVAILABLE = False
    face_recognition = None


def encode_face_encoding(encoding: np.ndarray) -> str:
    """Converte numpy array encoding para string JSON"""
    return json.dumps(encoding.tolist())


def decode_face_encoding(encoding_str: str) -> np.ndarray:
    """Converte string JSON para numpy array encoding"""
    return np.array(json.loads(encoding_str))


def extract_face_encodings(image_bytes: bytes) -> List[np.ndarray]:
    """Extrai encodings de face de uma imagem"""
    if not FACE_RECOGNITION_AVAILABLE:
        raise ValueError(
            "face-recognition não está instalado. "
            "Por favor, instale CMake e Visual Studio Build Tools, depois execute: "
            "pip install dlib face-recognition==1.3.0"
        )
    
    try:
        # Carrega a imagem
        image = face_recognition.load_image_file(io.BytesIO(image_bytes))
        # Encontra todas as faces na imagem
        face_locations = face_recognition.face_locations(image)
        # Extrai encodings de todas as faces encontradas
        encodings = face_recognition.face_encodings(image, face_locations)
        return encodings
    except Exception as e:
        raise ValueError(f"Erro ao processar imagem: {str(e)}")


def find_matching_face(
    unknown_encoding: np.ndarray,
    known_encodings: List[Tuple[str, str, np.ndarray]],
    tolerance: float = 0.6
) -> Tuple[bool, str, str, float]:
    """
    Compara um encoding desconhecido com encodings conhecidos.
    Retorna: (match, face_id, name, confidence)
    """
    if not FACE_RECOGNITION_AVAILABLE:
        raise RuntimeError(
            "face-recognition não está instalado. "
            "Por favor, instale CMake e Visual Studio Build Tools, depois execute: "
            "pip install dlib face-recognition==1.3.0"
        )
    
    if not known_encodings:
        return False, "", "", 0.0
    
    distances = []
    for face_id, name, encoding in known_encodings:
        # Calcula a distância euclidiana entre os encodings
        distance = face_recognition.face_distance([encoding], unknown_encoding)[0]
        distances.append((distance, face_id, name))
    
    # Encontra o melhor match (menor distância)
    if distances:
        min_distance, face_id, name = min(distances, key=lambda x: x[0])
        # Converte distância para confidence (quanto menor a distância, maior a confidence)
        confidence = max(0.0, 1.0 - min_distance)
        
        # Considera match se a distância for menor que a tolerância
        if min_distance <= tolerance:
            return True, face_id, name, confidence
    
    return False, "", "", 0.0


def generate_face_id(name: str, existing_ids: List[str]) -> str:
    """Gera um ID único para o rosto"""
    base_id = name.lower().replace(" ", "_")
    counter = 1
    face_id = base_id
    
    while face_id in existing_ids:
        face_id = f"{base_id}_{counter:03d}"
        counter += 1
    
    return face_id

