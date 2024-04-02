from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey, Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(Integer, primary_key=True)
    content = Column(Text)
    user_name = Column(String(50))
    created_at = Column(Time)
    
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship(
        "User", 
        backref=backref("messages", uselist=False), 
        uselist=False
    )

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'user_name': self.user_name,
            'created_at': self.created_at.strftime("%H:%M") if self.created_at else None
        }
