import random
import string
from datetime import datetime, timedelta
from email.message import EmailMessage
import smtplib
from email.mime.text import MIMEText
from fastapi.responses import JSONResponse
import logging

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
import models
import schemas

logger = logging.getLogger(__name__)
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
    try:
        # Lấy thông tin về người dùng, loại phí và các giao dịch liên quan
        user = db.query(models.User).filter(models.User.id == transaction.owner_id).first()
        fee = db.query(models.Fee).filter(models.Fee.id == transaction.fee_id).first()

        # Kiểm tra xem người dùng và loại phí có tồn tại hay không
        if not user:
            logger.error("User not found")
            return JSONResponse(status_code=400, content={"error": "User not found"})
        if not fee:
            logger.error("Fee not found")
            return JSONResponse(status_code=400, content={"error": "Fee not found"})

        # Kiểm tra số dư của người dùng và số tiền của loại phí
        if user.balance < fee.amount_due or user.balance < transaction.amount or user.balance < fee.amount_due:
            logger.error("Insufficient balance")
            return JSONResponse(status_code=400, content={"error": "Insufficient balance"})

        # Kiểm tra xem khoản phí đã được thanh toán hay chưa
        if fee.is_paid:
            logger.error("Fee already paid")
            return JSONResponse(status_code=400, content={"error": "Fee already paid"})

        # Kiểm tra tính hợp lệ của mã OTP và xác nhận rằng nó chưa hết hạn
        db_otp = db.query(models.OTP).filter(
            models.OTP.user_id == transaction.owner_id,
            models.OTP.otp == otp,
            models.OTP.expiry > datetime.utcnow()
        ).first()
        if not db_otp:
            logger.error("Invalid or expired OTP")
            return JSONResponse(status_code=400, content={"error": "Invalid or expired OTP"})

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

        # Đánh dấu khoản phí đã được thanh toán
        fee.isPaid = True
        db.commit()

        # Gửi email xác nhận giao dịch thành công
        msg = EmailMessage()
        msg.set_content(f"Transaction successfully")

        msg['Subject'] = "Xác nhận giao dịch thành công"
        msg['From'] = "tranleduy08082002@gmail.com"
        msg['To'] = user.email

        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.ehlo()
            smtp.login("tranleduy08082002@gmail.com", "zdievrqhwrvpkitk")
            smtp.send_message(msg)

        return db_transaction
    except Exception as e:
        logger.exception("An unexpected error occurred")
        return JSONResponse(status_code=500, content={"error": "An unexpected error occurred"})



# Hằng số
OTP_EXPIRY_MINUTES = 5

def generate_otp(db: Session, length=6, user_id=None, fee_id=None):
    try:
        # Kiểm tra xem user_id và fee_id có tồn tại không
        if user_id is None or fee_id is None:
            raise ValueError("user_id and fee_id cannot be None")

        # Tạo mã OTP ngẫu nhiên
        otp = ''.join(random.choices(string.digits, k=length))

        # Kiểm tra xem có OTP nào khác đang hoạt động cho cùng một user_id không
        existing_otp_same_user = db.query(models.OTP).filter(
            and_(
                models.OTP.user_id == user_id,
                models.OTP.fee_id == fee_id
            )
        ).first()

        # Kiểm tra xem có OTP nào khác đang hoạt động cho cùng một fee_id không
        existing_otp_different_user_same_fee = db.query(models.OTP).filter(
            and_(
                models.OTP.user_id != user_id,
                models.OTP.expiry > datetime.now(),
                models.OTP.fee_id == fee_id
            )
        ).all()

        # So sánh thời gian tạo mới của OTP với thời gian hết hạn của các OTP đã tìm được
        if any(datetime.now() <= existing.expiry for existing in existing_otp_different_user_same_fee):
            logger.exception("Another transaction is in progress")
            return JSONResponse(status_code=500, content={"error": "Another transaction is in progress"})

        if existing_otp_same_user:
            # Nếu có OTP khác đang hoạt động cho cùng một user_id và fee_id
            if existing_otp_same_user.expiry > datetime.now():
                # Kiểm tra thời gian hết hạn của OTP mới
                otp_expiry = datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
                if otp_expiry > existing_otp_same_user.expiry:
                    # Nếu thời gian hết hạn của OTP mới lớn hơn, ghi đè lên OTP hiện tại
                    existing_otp_same_user.otp = otp
                    existing_otp_same_user.expiry = otp_expiry
                else:
                    # Nếu thời gian hết hạn của OTP mới không lớn hơn, xóa OTP hiện tại
                    db.delete(existing_otp_same_user)
            else:
                # Nếu OTP hiện tại đã hết hạn, ghi đè lên OTP hiện tại
                otp_expiry = datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
                existing_otp_same_user.otp = otp
                existing_otp_same_user.expiry = otp_expiry
        else:
            # Nếu không có OTP nào khác đang hoạt động, tiếp tục tạo và lưu OTP mới
            otp_expiry = datetime.now() + timedelta(minutes=OTP_EXPIRY_MINUTES)
            db_otp = models.OTP(otp=otp, expiry=otp_expiry, user_id=user_id, fee_id=fee_id)
            db.add(db_otp)

        db.commit()

        return otp
    
    except ValueError as ve:
        logger.error(f"Value error occurred: {ve}")
        return JSONResponse(status_code=400, content={"error": str(ve)})
    except SQLAlchemyError as sqle:
        logger.error(f"Database error occurred: {sqle}")
        return JSONResponse(status_code=500, content={"error": "Database error occurred"})
    except Exception as e:
        logger.exception("An unexpected error occurred")
        return JSONResponse(status_code=500, content={"error": "An unexpected error occurred"})
    finally:
        db.close()
    return otp




# Fee
def get_fee(db: Session, fee_id: str):
    return db.query(models.Fee).filter(models.Fee.id == fee_id).first()


def send_otp_email(email: str, otp: str):
    """Gửi mã OTP đến địa chỉ email của người dùng."""
    msg = EmailMessage()
    msg.set_content(f"Your OTP for transaction: {otp}")

    msg['Subject'] = "OTP for Transaction"
    msg['From'] = "tranleduy08082002@gmail.com"
    msg['To'] = email

    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login("tranleduy08082002@gmail.com", "zdievrqhwrvpkitk")
        smtp.send_message(msg)


def update_user_balance(db: Session, user_id: str, new_balance: float):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    user.balance += new_balance
    db.commit()
    db.refresh(user)
    return user

def create_fee(db: Session, fee: schemas.FeeCreate):
    db_fee = models.Fee(**fee.dict())
    db.add(db_fee)
    db.commit()
    db.refresh(db_fee)
    return db_fee

def get_fee_by_student_id(db: Session, student_id: str):
    return db.query(models.Fee).filter(models.Fee.student_id == student_id, models.Fee.is_paid == False).all()

def get_transaction_by_fee(db: Session, fee_id: int):
    return db.query(models.Transaction).filter(models.Fee.id == fee_id).first()





