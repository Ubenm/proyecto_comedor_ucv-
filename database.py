from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Configuración de SQLite (o PostgreSQL)
DATABASE_URL = "sqlite:///comedor_ucv.db"
# Para PostgreSQL: postgresql://user:password@localhost/dbname

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()