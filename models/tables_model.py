from database import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class TableModel(db.Model):
    __tablename__ = "tables"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)