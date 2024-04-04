from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    full_name = Column(String)
    phone_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    balance = Column(Float, default=0.0)
    
    transactions = relationship("Transaction", back_populates="owner")
    account = relationship("Account", back_populates="user")
    otp = relationship("OTP", back_populates="user")



class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)

    amount = Column(Float)

    owner_id = Column(String, ForeignKey("users.id"))
    owner = relationship("User", back_populates="transactions")

    fee_id = Column(Integer, ForeignKey("fees.id"))
    fee = relationship("Fee", back_populates="transactions", foreign_keys=[fee_id])


class Fee(Base):
    __tablename__ = "fees"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(String)
    student_name = Column(String)
    fee_type = Column(String)
    amount_due = Column(Float)

    transactions = relationship("Transaction", back_populates="fee")



class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    user_id = Column(String, ForeignKey("users.id"))
    user = relationship("User", back_populates="account")

class OTP(Base):
    __tablename__ = "otp"

    id = Column(Integer, primary_key=True, index=True)
    otp = Column(String, index=True)
    expiry = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.id"))

    # Liên kết với bảng User
    user = relationship("User", back_populates="otp")
