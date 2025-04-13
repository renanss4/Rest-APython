from database import Base, engine
from models import Item

print("Creating database tables...")

Base.metadata.create_all(engine)

print("Database tables created successfully.")
