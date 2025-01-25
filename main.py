from app.models.base import Base, engine

Base.metadata.drop_all(bind=engine)
# Create all tables
Base.metadata.create_all(bind=engine)