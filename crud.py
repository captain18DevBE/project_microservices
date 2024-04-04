import random
import string
from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText

from sqlalchemy.orm import Session
import models
import schemas


# User 
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_transaction(db: Session, transaction: schemas.TransactionCreate, otp: str):
    # Lấy thông tin về người dùng, loại phí và các giao dịch liên quan
    user = db.query(models.User).filter(models.User.id == transaction.owner_id).first()
    fee = db.query(models.Fee).filter(models.Fee.id == transaction.fee_id).first()

    # Kiểm tra xem người dùng và loại phí có tồn tại hay không
    if not user:
        raise ValueError("User not found")
    if not fee:
        raise ValueError("Fee not found")

    # Kiểm tra số dư của người dùng và số tiền của loại phí
    if user.balance < fee.amount_due or user.balance < transaction.amount:
        raise ValueError("Insufficient balance")

    # Kiểm tra xem khoản phí đã được thanh toán hay chưa
    fee_transactions = db.query(models.Transaction).filter(models.Transaction.fee_id == transaction.fee_id).all()
    if fee_transactions:
        raise ValueError("Fee already paid")

    # Kiểm tra xem OTP có tồn tại và hợp lệ không
    db_otp = db.query(models.OTP).filter(
        models.OTP.user_id == transaction.owner_id,
        models.OTP.otp == otp,
        models.OTP.expiry > datetime.utcnow()
    ).first()
    if not db_otp:
        raise ValueError("Invalid or expired OTP")

    # Đánh dấu mã OTP đã được sử dụng
    db.delete(db_otp)
    db.commit()

    # Tạo giao dịch mới
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()

    # Trừ số tiền tương ứng từ số dư của người dùng
    user.balance -= fee.amount_due
    db.commit()

    # Cập nhật lại số dư của người dùng trong database
    db.refresh(user)

    return db_transaction


# Hằng số
OTP_EXPIRY_MINUTES = 5

def generate_otp(db: Session, length=6, user_id=None):
    """Tạo mã OTP ngẫu nhiên và lưu vào cơ sở dữ liệu."""
    # Kiểm tra xem user_id có tồn tại không
    if user_id is None:
        raise ValueError("user_id cannot be None")

    # Tạo mã OTP ngẫu nhiên
    otp = ''.join(random.choices(string.digits, k=length))
    
    try:
        otp_expiry = datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
        db_otp = models.OTP(otp=otp, expiry=otp_expiry, user_id=user_id)
        db.add(db_otp)
        db.commit()
    except Exception as e:
        db.rollback()  # Hoàn tác thay đổi trong trường hợp có lỗi
        raise e
    finally:
        db.close()
    
    return otp

def send_otp_email(email: str, otp: str):
    """Gửi mã OTP đến địa chỉ email của người dùng."""
    msg = EmailMessage()
    msg.set_content(f"Your OTP for transaction: {otp}")

    msg['Subject'] = "OTP for Transaction"
    msg['From'] = "anhquan12052003@gmail.com"
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login("anhquan12052003@gmail.com", "Quan12052003")
        smtp.send_message(msg)


