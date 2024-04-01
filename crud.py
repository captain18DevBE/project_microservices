from sqlalchemy.orm import Session
from . import models, schemas


# Account CRUD
def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(**account.dict())
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_account(db: Session, account_id: int, account_update: schemas.AccountUpdate):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if db_account:
        for attr, value in account_update.dict().items():
            setattr(db_account, attr, value)
        db.commit()
        db.refresh(db_account)
    return db_account

def delete_account(db: Session, account_id: int):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if db_account:
        db.delete(db_account)
        db.commit()
    return db_account

# User CRUD
def get_user(db: Session, user_id: str):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: str, user_update: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for attr, value in user_update.dict().items():
            setattr(db_user, attr, value)
        db.commit()
        db.refresh(db_user)
    return db_user

def delete_user(db: Session, user_id: str):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

# Transaction CRUD
def get_transaction(db: Session, transaction_id: int):
    return db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()

def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(**transaction.dict())
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def update_transaction(db: Session, transaction_id: int, transaction_update: schemas.TransactionUpdate):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction:
        for attr, value in transaction_update.dict().items():
            setattr(db_transaction, attr, value)
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def delete_transaction(db: Session, transaction_id: int):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction:
        db.delete(db_transaction)
        db.commit()
    return db_transaction

# Fee CRUD
def get_fee(db: Session, fee_id: int):
    return db.query(models.Fee).filter(models.Fee.id == fee_id).first()

def create_fee(db: Session, fee: schemas.FeeCreate):
    db_fee = models.Fee(**fee.dict())
    db.add(db_fee)
    db.commit()
    db.refresh(db_fee)
    return db_fee

def update_fee(db: Session, fee_id: int, fee_update: schemas.FeeUpdate):
    db_fee = db.query(models.Fee).filter(models.Fee.id == fee_id).first()
    if db_fee:
        for attr, value in fee_update.dict().items():
            setattr(db_fee, attr, value)
        db.commit()
        db.refresh(db_fee)
    return db_fee

def delete_fee(db: Session, fee_id: int):
    db_fee = db.query(models.Fee).filter(models.Fee.id == fee_id).first()
    if db_fee:
        db.delete(db_fee)
        db.commit()
    return db_fee




