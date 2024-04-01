from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from .database import SessionLocal, engine

# This code will create the database tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Account Endpoints
@app.get("/accounts/{account_id}", response_model=schemas.Account)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@app.post("/accounts/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    return crud.create_account(db=db, account=account)

@app.put("/accounts/{account_id}", response_model=schemas.Account)
def update_account(account_id: int, account_update: schemas.AccountUpdate, db: Session = Depends(get_db)):
    db_account = crud.update_account(db=db, account_id=account_id, account_update=account_update)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account

@app.delete("/accounts/{account_id}", response_model=schemas.Account)
def delete_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.delete_account(db=db, account_id=account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account


# User Endpoints
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)

@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: str, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud.update_user(db=db, user_id=user_id, user_update=user_update)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# Fee Endpoints
@app.get("/fees/{fee_id}", response_model=schemas.Fee)
def read_fee(fee_id: int, db: Session = Depends(get_db)):
    db_fee = crud.get_fee(db, fee_id)
    if db_fee is None:
        raise HTTPException(status_code=404, detail="Fee not found")
    return db_fee

@app.post("/fees/", response_model=schemas.Fee)
def create_fee(fee: schemas.FeeCreate, db: Session = Depends(get_db)):
    return crud.create_fee(db=db, fee=fee)

@app.put("/fees/{fee_id}", response_model=schemas.Fee)
def update_fee(fee_id: int, fee_update: schemas.FeeUpdate, db: Session = Depends(get_db)):
    db_fee = crud.update_fee(db=db, fee_id=fee_id, fee_update=fee_update)
    if db_fee is None:
        raise HTTPException(status_code=404, detail="Fee not found")
    return db_fee

@app.delete("/fees/{fee_id}", response_model=schemas.Fee)
def delete_fee(fee_id: int, db: Session = Depends(get_db)):
    db_fee = crud.delete_fee(db=db, fee_id=fee_id)
    if db_fee is None:
        raise HTTPException(status_code=404, detail="Fee not found")
    return db_fee


# Transaction Endpoints
@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud.get_transaction(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)

@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(transaction_id: int, transaction_update: schemas.TransactionUpdate, db: Session = Depends(get_db)):
    db_transaction = crud.update_transaction(db=db, transaction_id=transaction_id, transaction_update=transaction_update)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction

@app.delete("/transactions/{transaction_id}", response_model=schemas.Transaction)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud.delete_transaction(db=db, transaction_id=transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction


