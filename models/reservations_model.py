from database import db
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class ReservationModel(db.Model):
    __tablename__ = "reservations"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), nullable=False)
    table_id = db.Column(db.Integer, db.ForeignKey('tables.id'), nullable=False)

    table = relationship("TableModel", back_populates="reservations")