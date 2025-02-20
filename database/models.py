from sqlalchemy import Column, Integer, String
from database.database import Base
from werkzeug.security import generate_password_hash

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    rol = Column(String(20), default="estudiante")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

# Crear tablas al inicio (ejecutar una vez)
if __name__ == "__main__":
    from database.database import engine
    Base.metadata.create_all(bind=engine)