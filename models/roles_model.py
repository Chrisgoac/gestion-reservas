from database import db
from sqlalchemy.orm import relationship

class RoleModel(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

    users = relationship("UserModel", back_populates="role", cascade="all, delete-orphan")