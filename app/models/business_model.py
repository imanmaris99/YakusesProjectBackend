import uuid
import bcrypt
from sqlalchemy import ARRAY, CHAR, DateTime, func
from app.utils.db import db


class Business(db.Model):
    __tablename__ = "business"
    id = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    name = db.Column(db.String(50), unique=True, index=True)
    description = db.Column(ARRAY(db.Text))
    photo_url = db.Column(db.String(255))
    location = db.Column(db.Text)
    contact = db.Column(CHAR(36))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    fk_business_category_id = db.Column(db.Integer, db.ForeignKey('business_category.id'))
    fk_owner_id = db.Column(CHAR(36), db.ForeignKey('users.id'))
