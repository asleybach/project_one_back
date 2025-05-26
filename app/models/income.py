from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, event
from sqlalchemy.orm import relationship
from app.database.database import Base

class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    source = Column(String, nullable=False)  
    amount = Column(Float, nullable=False)  
    observations = Column(String, nullable=True)  
    date = Column(DateTime, default=datetime.utcnow, nullable=False)  
    month = Column(String, nullable=False)  
    
    user = relationship("User", back_populates="incomes")
    
    @property
    def computed_month(self):
        """Propiedad computada para obtener el mes basado en la fecha."""
        return self.date.strftime("%B")

# Evento para calcular y asignar el valor de 'month' antes de insertar o actualizar
@event.listens_for(Income, "before_insert")
@event.listens_for(Income, "before_update")
def set_month(mapper, connection, target):
    """Calcula y asigna el valor del campo 'month' antes de guardar en la base de datos."""
    target.month = target.date.strftime("%B")