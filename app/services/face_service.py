from typing import List, Tuple, Optional
import numpy as np
from app.database import db
from app.utils import (
    extract_face_encodings,
    encode_face_encoding,
    decode_face_encoding,
    find_matching_face,
    generate_face_id
)


class FaceService:
    def __init__(self):
        self._known_faces_cache = None
        self._cache_valid = False
    
    def _load_known_faces(self) -> List[Tuple[str, str, np.ndarray]]:
        """Carrega todos os rostos conhecidos do banco de dados"""
        if self._known_faces_cache and self._cache_valid:
            return self._known_faces_cache
        
        trained_faces = db.get_all_trained_faces()
        known_faces = []
        
        for face in trained_faces:
            encoding = decode_face_encoding(face.encoding)
            known_faces.append((face.face_id, face.name, encoding))
        
        self._known_faces_cache = known_faces
        self._cache_valid = True
        return known_faces
    
    def invalidate_cache(self):
        """Invalida o cache quando novos rostos são treinados"""
        self._cache_valid = False
    
    def train_face(self, image_bytes: bytes, name: str, face_id: Optional[str] = None) -> Tuple[bool, str, str]:
        """
        Treina um rosto com uma imagem.
        Retorna: (success, message, face_id)
        """
        try:
            # Extrai encodings da imagem
            encodings = extract_face_encodings(image_bytes)
            
            if not encodings:
                return False, "Nenhuma face encontrada na imagem", ""
            
            if len(encodings) > 1:
                return False, "Múltiplas faces encontradas. Por favor, envie uma imagem com apenas uma pessoa.", ""
            
            encoding = encodings[0]
            
            # Gera face_id se não fornecido
            if not face_id:
                existing_ids = [f.face_id for f in db.get_all_trained_faces()]
                face_id = generate_face_id(name, existing_ids)
            
            # Verifica se já existe
            existing = db.get_trained_face_by_id(face_id)
            if existing:
                return False, f"Face ID '{face_id}' já existe. Use um ID diferente ou atualize a face existente.", ""
            
            # Salva no banco de dados
            encoding_str = encode_face_encoding(encoding)
            db.add_trained_face(face_id, name, encoding_str)
            
            # Invalida cache
            self.invalidate_cache()
            
            return True, f"Rosto de {name} treinado com sucesso", face_id
            
        except ValueError as e:
            return False, str(e), ""
        except Exception as e:
            return False, f"Erro ao treinar rosto: {str(e)}", ""
    
    def recognize_face(self, image_bytes: bytes, tolerance: float = 0.6) -> List[Tuple[str, str, float]]:
        """
        Reconhece faces em uma imagem.
        Retorna lista de: (face_id, name, confidence)
        """
        try:
            # Extrai encodings da imagem
            encodings = extract_face_encodings(image_bytes)
            
            if not encodings:
                return []
            
            # Carrega rostos conhecidos
            known_faces = self._load_known_faces()
            
            if not known_faces:
                return []
            
            recognized = []
            
            # Compara cada encoding encontrado com os conhecidos
            for encoding in encodings:
                match, face_id, name, confidence = find_matching_face(
                    encoding, known_faces, tolerance
                )
                
                if match:
                    recognized.append((face_id, name, confidence))
                    # Atualiza last_seen
                    db.update_last_seen(face_id)
                    # Adiciona log
                    db.add_recognition_log(face_id, name, confidence)
            
            return recognized
            
        except Exception as e:
            print(f"Erro ao reconhecer rosto: {str(e)}")
            return []


# Singleton instance
face_service = FaceService()

