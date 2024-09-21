from database import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class UserModel(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), default=1, nullable=False)
    
    role = relationship("RoleModel", back_populates="users")