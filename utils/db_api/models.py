from utils.db_api.database import db
from sqlalchemy import (Column, Integer, BigInteger, Sequence,
                        String, TIMESTAMP, Boolean, JSON, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy import sql
from sqlalchemy import Column, Integer, String, create_engine


class User(db.Model):
    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String(255))
    nickname = Column(String(255))
    phone = Column(String(255))
    language = Column(String(2))
    accept = Column(Integer)
    sms = Column(Integer)
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Sms(db.Model):
    __tablename__ = "sms"
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"))
    user = relationship("User")
    phone = Column(String(255))
    otp = Column(String(255))
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Gap(db.Model):
    __tablename__ = "gap"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.id"))
    user = relationship("User")
    number_of_members = Column(BigInteger)
    amount = Column(String(255))
    location = Column(String(255))
    link = Column(String(255))
    private = Column(Integer)
    start = Column(String(255))
    period = Column(String(255))
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class RoleOfGap(db.Model):
    __tablename__ = "role_of_gap"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    gap_id = Column(BigInteger, ForeignKey('gap.id'))
    gap = relationship("Gap")
    user_id = Column(BigInteger, ForeignKey("user.id"))
    user = relationship("User")
    get_money = Column(Integer)
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Confirmation(db.Model):
    __tablename__ = "confirmation"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    member_recieve = Column(BigInteger)
    member_get = Column(BigInteger)
    accept = Column(Integer)
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

