import datetime
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///test.db', echo=True)
Base = declarative_base()


class Nickname(Base):
    __tablename__ = "nicknames"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __repr__(self):
        return "<Nickname: {}>".format(self.name)


class Report(Base):
    """"""
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime(timezone=True), default=func.now())
    comment = Column(String)
    incident_date = Column(String)
    incident_type = Column(String)
    game_type = Column(String)
    priority = Column(String)
    status = Column(String)
    resolution = Column(String)
    comment_soc = Column(String)
    service_login = Column(String)
    username = Column(String)
    ticket = Column(String)
    
    nickname_id = Column(Integer, ForeignKey("nicknames.id"))
    nickname = relationship("Nickname", backref=backref(
        "reports", order_by=id))


# create tables
class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    created_date = Column(DateTime(timezone=True), default=func.now())
    username = Column(String)
    pass_hash = Column(String)
    email = Column(String)
    role = Column(String)
    about = Column(String)
    
Base.metadata.create_all(engine)
