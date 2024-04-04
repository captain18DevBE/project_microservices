from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

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

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.get("/user/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.get("/users/email/{email}", response_model=schemas.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.post("/transactions/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    return crud.create_transaction(db=db, transaction=transaction)


@app.post("/send_otp/")
def send_otp(email: str, user_id: str, db: Session = Depends(get_db)):
    # Tạo mã OTP và lưu vào cơ sở dữ liệu
    otp = crud.generate_otp(db=db, user_id=user_id)
    
    # Gửi mã OTP tới email của người dùng
    crud.send_otp_email(email, otp)
    return {"message": "OTP sent successfully"}

@app.post("/update_balance/")
def update_balance(balance: float, user_id: str, db: Session = Depends(get_db)):
    return crud.update_user_balance(db=db, user_id=user_id, new_balance=balance)

@app.post("/fees/", response_model=schemas.Fee)
def create_fee(fee: schemas.FeeCreate, db: Session = Depends(get_db)):
    db_fee = crud.create_fee(db=db, fee=fee)
    return db_fee
