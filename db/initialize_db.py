from db.database import Base, engine
import db.models  # Import models to register with SQLAlchemy

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database tables created successfully!")
