from utils.db_api.database import db
from sqlalchemy import *
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String


class User(db.Model):
    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True, unique=True, autoincrement=True)
    user_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String(255))
    nickname = Column(String(255))
    phone = Column(String(255))
    language = Column(String(2))
    accept = Column(Integer)
    complain = Column(Integer, default=0)
    subscribe = Column(Integer, default=1)
    end_date = Column(String(255))
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class SubscribeUsers(db.Model):
    __tablename__ = "subscribe_users"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"), unique=False)
    user = relationship("User")
    amount = Column(String(255))
    start_date = Column(String(255))
    end_date = Column(String(255))
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Group(db.Model):
    __tablename__ = "group"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey("user.user_id"))
    user = relationship("User")
    name = Column(String(255), unique=True)
    number_of_members = Column(BigInteger)
    amount = Column(String(255))
    location = Column(String(255))
    link = Column(String(255))
    private = Column(Integer)
    start_date = Column(String(255))
    start = Column(BigInteger, default=0)
    period = Column(BigInteger)
    token = Column(String(255))
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Member(db.Model):
    __tablename__ = "member"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    id_queue = Column(BigInteger, autoincrement=True, unique=False)
    group_id = Column(BigInteger, ForeignKey('group.id'), unique=False)
    group = relationship("Group")
    member = Column(BigInteger, ForeignKey("user.user_id"), unique=False)
    user = relationship("User")
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class Confirmation(db.Model):
    __tablename__ = "confirmation"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    group_id = Column(BigInteger)
    member_recieve = Column(BigInteger)
    member_get = Column(BigInteger)
    accept = Column(Integer)
    date = Column(String(255))
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())


class UserInGroup(db.Model):
    __tablename__ = "user_in_group"
    user_id = Column(BigInteger, ForeignKey("user.user_id"), primary_key=True, unique=True)
    user = relationship("User")
    group_id = Column(BigInteger, ForeignKey('group.id'), unique=False)
    group = relationship("Group")
    date_created = Column(TIMESTAMP, server_default=db.func.current_timestamp())
    date_updated = Column(TIMESTAMP, server_default=db.func.current_timestamp(),
                          onupdate=db.func.current_timestamp())

