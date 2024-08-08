import uuid
import bcrypt
from sqlalchemy import ARRAY, CHAR, DateTime, func
from app.utils.db import db


class UserNeeds(db.Model):
    __tablename__ = "user_needs"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    title = db.Column(db.String(100), unique=True, index=True)
    description = db.Column(ARRAY(db.Text))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    is_visible = db.Column(db.Boolean, default=True)
    fk_business_category_id = db.Column(db.Integer, db.ForeignKey('business_category.id'))
    fk_user_id = db.Column(CHAR(36), db.ForeignKey('users.id'))