import uuid
import bcrypt
from sqlalchemy import ARRAY, CHAR, DateTime, func
from app.utils.db import db


class Rating(db.Model):
    __tablename__ = "rating"
    id = db.Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()), unique=True, index=True)
    rating_count = db.Column(db.Integer, index=True)
    review_description = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now()) 
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    fk_business_id = db.Column(CHAR(36), db.ForeignKey('business.id'))
    fk_rater_id = db.Column(CHAR(36), db.ForeignKey('users.id'))

    users = db.relationship("User", back_populates="ratings")