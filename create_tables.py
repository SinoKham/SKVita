from app.database import Base, engine
import app.db_models

Base.metadata.create_all(bind=engine)
print("Таблицы созданы!")