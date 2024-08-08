import uuid
import bcrypt
from sqlalchemy import ARRAY, CHAR, DateTime, func
from app.utils.db import db


class BusinessCategory(db.Model):
    __tablename__ = "business_category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    name = db.Column(db.String(50), unique=True, index=True)
    describe = db.Column(ARRAY(db.Text), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 