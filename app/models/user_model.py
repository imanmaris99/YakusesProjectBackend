import uuid
import bcrypt
from sqlalchemy import ARRAY, CHAR, DateTime, func
from app.utils.db import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    username = db.Column(db.String(100), unique=True, index=True, nullable=False)
    fullname = db.Column(db.String(100), unique=True, index=True, nullable=True)
    about_me = db.Column(ARRAY(db.Text), nullable=True)
    email = db.Column(db.String(100), nullable=False, unique=True, index=True)
    phone = db.Column(db.String(15), nullable=True)
    address= db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    ratings = db.relationship("Rating", back_populates="users", cascade="all, delete-orphan")   

    def as_dict(self):
        return{
            "id": self.id,
            "username": self.username,
            "fullname": self.fullname,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "about_me": self.about_me,
            "role": self.role,
            "created_at": self.created_at.isoformat(),  # ISO format string
            "updated_at": self.updated_at.isoformat() if self.updated_at else None  # ISO format string or None
        }
    
    def set_password(self, password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))