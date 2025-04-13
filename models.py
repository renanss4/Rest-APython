from database import Base
from sqlalchemy import String, Boolean, Integer, Column, Text

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text)
    price = Column(Integer, nullable=False)
    on_offer = Column(Boolean, default=False)

    def __repr__(self):
        return f"Item(id={self.id}, name={self.name}, description={self.description}, price={self.price}, on_offer={self.on_offer})"
    