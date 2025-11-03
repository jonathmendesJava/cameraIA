from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text, Index, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from datetime import datetime
import os
from typing import Optional, List
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()


class TrainedFace(Base):
    __tablename__ = "trained_faces"
    
    id = Column(Integer, primary_key=True, index=True)
    face_id = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    encoding = Column(Text, nullable=False)  # JSON serialized encoding
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    last_seen = Column(DateTime, nullable=True, index=True)
    
    # Índice composto para buscas frequentes
    __table_args__ = (
        Index('idx_face_id_name', 'face_id', 'name'),
    )


class RecognitionLog(Base):
    __tablename__ = "recognition_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    face_id = Column(String(255), nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    confidence = Column(Float, nullable=False, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Índice composto para consultas por face_id e data
    __table_args__ = (
        Index('idx_face_timestamp', 'face_id', 'timestamp'),
        Index('idx_timestamp', 'timestamp'),
    )


class Database:
    def __init__(self, db_path: Optional[str] = None):
        # Permite configurar o caminho do BD via variável de ambiente
        if db_path is None:
            db_path = os.getenv("DATABASE_PATH", "data/face_recognition.db")
        
        # Garante que o diretório existe
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        
        # Configurações do SQLite otimizadas
        connect_args = {
            "check_same_thread": False,
            "timeout": 30.0,  # Timeout de 30 segundos
        }
        
        # Para uso em memória (útil para testes)
        if db_path == ":memory:":
            self.engine = create_engine(
                "sqlite:///:memory:",
                connect_args=connect_args,
                poolclass=StaticPool,
                echo=os.getenv("DB_ECHO", "false").lower() == "true"
            )
        else:
            # Para arquivo, usa caminho absoluto para evitar problemas
            abs_path = os.path.abspath(db_path)
            self.engine = create_engine(
                f"sqlite:///{abs_path}",
                connect_args=connect_args,
                pool_pre_ping=True,  # Verifica conexões antes de usar
                echo=os.getenv("DB_ECHO", "false").lower() == "true"
            )
        
        # Cria todas as tabelas
        Base.metadata.create_all(bind=self.engine)
        
        # Session factory com scoped_session para thread safety
        self.SessionLocal = scoped_session(
            sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        )
    
    def get_session(self):
        return self.SessionLocal()
    
    def add_trained_face(self, face_id: str, name: str, encoding: str):
        session = self.get_session()
        try:
            face = TrainedFace(
                face_id=face_id,
                name=name,
                encoding=encoding
            )
            session.add(face)
            session.commit()
            return face
        finally:
            session.close()
    
    def get_all_trained_faces(self):
        session = self.get_session()
        try:
            return session.query(TrainedFace).all()
        finally:
            session.close()
    
    def get_trained_face_by_id(self, face_id: str):
        session = self.get_session()
        try:
            return session.query(TrainedFace).filter_by(face_id=face_id).first()
        finally:
            session.close()
    
    def update_last_seen(self, face_id: str):
        session = self.get_session()
        try:
            face = session.query(TrainedFace).filter_by(face_id=face_id).first()
            if face:
                face.last_seen = datetime.utcnow()
                session.commit()
        finally:
            session.close()
    
    def add_recognition_log(self, face_id: str, name: str, confidence: float):
        session = self.get_session()
        try:
            log = RecognitionLog(
                face_id=face_id,
                name=name,
                confidence=confidence
            )
            session.add(log)
            session.commit()
        finally:
            session.close()
    
    def get_trained_faces_count(self):
        session = self.get_session()
        try:
            return session.query(TrainedFace).count()
        finally:
            session.close()
    
    def get_face_by_name(self, name: str):
        """Busca rosto por nome"""
        session = self.get_session()
        try:
            return session.query(TrainedFace).filter_by(name=name).first()
        finally:
            session.close()
    
    def delete_trained_face(self, face_id: str) -> bool:
        """Deleta um rosto treinado"""
        session = self.get_session()
        try:
            face = session.query(TrainedFace).filter_by(face_id=face_id).first()
            if face:
                session.delete(face)
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_recognition_history(
        self,
        face_id: Optional[str] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[RecognitionLog]:
        """Busca histórico de reconhecimentos"""
        session = self.get_session()
        try:
            query = session.query(RecognitionLog)
            if face_id:
                query = query.filter_by(face_id=face_id)
            return query.order_by(RecognitionLog.timestamp.desc()).limit(limit).offset(offset).all()
        finally:
            session.close()
    
    def get_recognition_stats(self, days: int = 7):
        """Estatísticas de reconhecimento dos últimos N dias"""
        session = self.get_session()
        try:
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            # Total de reconhecimentos
            total = session.query(RecognitionLog).filter(
                RecognitionLog.timestamp >= cutoff_date
            ).count()
            
            # Rostos únicos reconhecidos
            unique_faces = session.query(RecognitionLog.face_id).filter(
                RecognitionLog.timestamp >= cutoff_date
            ).distinct().count()
            
            # Confiança média
            avg_confidence = session.query(func.avg(RecognitionLog.confidence)).filter(
                RecognitionLog.timestamp >= cutoff_date
            ).scalar() or 0.0
            
            # Último reconhecimento
            last_log = session.query(RecognitionLog).order_by(
                RecognitionLog.timestamp.desc()
            ).first()
            
            return {
                "total_recognitions": total,
                "unique_faces": unique_faces,
                "avg_confidence": float(avg_confidence) if avg_confidence else 0.0,
                "last_recognition": last_log.timestamp.isoformat() if last_log else None,
                "period_days": days
            }
        finally:
            session.close()
    
    def cleanup_old_logs(self, days: int = 30) -> int:
        """Remove logs antigos (útil para manter o BD limpo)"""
        session = self.get_session()
        try:
            from datetime import timedelta
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            
            deleted = session.query(RecognitionLog).filter(
                RecognitionLog.timestamp < cutoff_date
            ).delete()
            
            session.commit()
            return deleted
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def update_face_name(self, face_id: str, new_name: str) -> bool:
        """Atualiza o nome de um rosto"""
        session = self.get_session()
        try:
            face = session.query(TrainedFace).filter_by(face_id=face_id).first()
            if face:
                face.name = new_name
                session.commit()
                return True
            return False
        finally:
            session.close()
    
    def get_all_faces_with_stats(self):
        """Retorna todos os rostos com estatísticas"""
        session = self.get_session()
        try:
            faces = session.query(TrainedFace).all()
            result = []
            
            for face in faces:
                # Conta reconhecimentos deste rosto
                recognition_count = session.query(RecognitionLog).filter_by(
                    face_id=face.face_id
                ).count()
                
                # Último reconhecimento
                last_recognition = session.query(RecognitionLog).filter_by(
                    face_id=face.face_id
                ).order_by(RecognitionLog.timestamp.desc()).first()
                
                result.append({
                    "face_id": face.face_id,
                    "name": face.name,
                    "created_at": face.created_at.isoformat(),
                    "last_seen": face.last_seen.isoformat() if face.last_seen else None,
                    "recognition_count": recognition_count,
                    "last_recognition_confidence": last_recognition.confidence if last_recognition else None,
                    "last_recognition_time": last_recognition.timestamp.isoformat() if last_recognition else None
                })
            
            return result
        finally:
            session.close()


# Singleton instance
db = Database()

