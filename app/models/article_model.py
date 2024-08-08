import uuid
import bcrypt
from sqlalchemy import ARRAY, CHAR, DateTime, func
from app.utils.db import db


class Article(db.Model):
    __tablename__ = "article"
    id = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    title = db.Column(db.String(100), unique=True, index=True)
    description = db.Column(ARRAY(db.Text))
    image_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    fk_business_category_id = db.Column(db.Integer, db.ForeignKey('business_category.id'))
    fk_author_id = db.Column(CHAR(36), db.ForeignKey('users.id'))