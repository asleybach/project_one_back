from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base

class Income(Base):
    __tablename__ = "incomes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  
    source = Column(String, nullable=False)  
    amount = Column(Float, nullable=False)  
    category = Column(String, nullable=False)  
    observations = Column(String, nullable=True)  
    date = Column(DateTime, default=datetime.utcnow, nullable=False)  
    
    user = relationship("User", back_populates="incomes")
    
    @property
    def month(self):
        return self.date.strftime("%B")  