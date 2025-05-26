from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, event
from sqlalchemy.orm import relationship
from app.database.database import Base

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    amount = Column(Float, nullable=False)  
    payment_method = Column(String, nullable=False)  
    category = Column(String, nullable=False)  
    description = Column(String, nullable=True) 
    date = Column(DateTime, default=datetime.utcnow, nullable=False)  
    month = Column(String, nullable=False) 
    user = relationship("User", back_populates="expenses")  

    @property
    def computed_month(self):
        """Propiedad computada para obtener el mes basado en la fecha."""
        return self.date.strftime("%B")

@event.listens_for(Expense, "before_insert")
@event.listens_for(Expense, "before_update")
def set_month(mapper, connection, target):
    """Calcula y asigna el valor del campo 'month' antes de guardar en la base de datos."""
    target.month = target.date.strftime("%B")