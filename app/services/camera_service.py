import cv2
import threading
import time
from typing import Callable, Optional
from datetime import datetime
from app.services.face_service import face_service


class CameraService:
    def __init__(self):
        self.camera = None
        self.is_running = False
        self.thread = None
        self.on_face_recognized: Optional[Callable] = None
        self.camera_index = 0  # Pode ser ajustado via config
        self.frame_skip = 2  # Processa 1 frame a cada N frames (performance)
        self.frame_count = 0
        self.last_recognition_time = {}
        self.recognition_cooldown = 5  # Segundos entre reconhecimentos da mesma pessoa
    
    def set_camera_index(self, index: int):
        """Define qual câmera usar (0 para padrão, 1, 2, etc.)"""
        self.camera_index = index
    
    def set_on_face_recognized_callback(self, callback: Callable):
        """Define callback quando uma face é reconhecida"""
        self.on_face_recognized = callback
    
    def start(self) -> bool:
        """Inicia o serviço de câmera"""
        if self.is_running:
            return False
        
        try:
            self.camera = cv2.VideoCapture(self.camera_index)
            
            if not self.camera.isOpened():
                return False
            
            self.is_running = True
            self.thread = threading.Thread(target=self._camera_loop, daemon=True)
            self.thread.start()
            return True
            
        except Exception as e:
            print(f"Erro ao iniciar câmera: {str(e)}")
            return False
    
    def stop(self):
        """Para o serviço de câmera"""
        self.is_running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        if self.camera:
            self.camera.release()
        self.camera = None
    
    def _camera_loop(self):
        """Loop principal de captura e reconhecimento"""
        while self.is_running:
            try:
                ret, frame = self.camera.read()
                
                if not ret:
                    time.sleep(0.1)
                    continue
                
                self.frame_count += 1
                
                # Processa apenas alguns frames (otimização)
                if self.frame_count % self.frame_skip != 0:
                    continue
                
                # Converte frame para formato que face_recognition espera (RGB)
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Converte para bytes (simulando imagem)
                import io
                from PIL import Image
                pil_image = Image.fromarray(rgb_frame)
                img_bytes = io.BytesIO()
                pil_image.save(img_bytes, format='JPEG')
                image_bytes = img_bytes.getvalue()
                
                # Reconhece faces
                recognized = face_service.recognize_face(image_bytes)
                
                # Processa reconhecimentos
                for face_id, name, confidence in recognized:
                    # Cooldown para evitar spam de notificações
                    current_time = time.time()
                    last_time = self.last_recognition_time.get(face_id, 0)
                    
                    if current_time - last_time >= self.recognition_cooldown:
                        self.last_recognition_time[face_id] = current_time
                        
                        # Chama callback se definido
                        if self.on_face_recognized:
                            try:
                                self.on_face_recognized({
                                    "face_id": face_id,
                                    "name": name,
                                    "confidence": confidence,
                                    "timestamp": datetime.utcnow().isoformat()
                                })
                            except Exception as e:
                                print(f"Erro no callback: {str(e)}")
                
                time.sleep(0.033)  # ~30 FPS
                
            except Exception as e:
                print(f"Erro no loop da câmera: {str(e)}")
                time.sleep(1.0)
    
    def is_active(self) -> bool:
        """Retorna se a câmera está ativa"""
        return self.is_running and self.camera is not None and self.camera.isOpened()


# Singleton instance
camera_service = CameraService()

