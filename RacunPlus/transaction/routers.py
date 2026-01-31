from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from RacunPlus.database import SessionLocal
from RacunPlus.user.routers import get_current_user
from .models import Transaction

router = APIRouter(prefix='/transactions', tags=['transactions'])


class TransactionCreate(BaseModel):
    amount: float
    merchant_name: str
    transaction_date: date
    status: str = 'completed'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post('/create', status_code=201)
def create_transaction(transaction: TransactionCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    new_transaction = Transaction(
        user_id=current_user['id'],
        amount=transaction.amount,
        merchant_name=transaction.merchant_name,
        transaction_date=transaction.transaction_date,
        status=transaction.status
    )
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    
    return {
        'id': str(new_transaction.id),
        'user_id': str(new_transaction.user_id),
        'amount': new_transaction.amount,
        'merchant_name': new_transaction.merchant_name,
        'transaction_date': str(new_transaction.transaction_date),
        'status': new_transaction.status
    }


@router.get('/list')
def list_transactions(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user['id']).all()
    result = []
    for t in transactions:
        result.append({
            'id': str(t.id),
            'user_id': str(t.user_id),
            'amount': t.amount,
            'merchant_name': t.merchant_name,
            'transaction_date': str(t.transaction_date),
            'status': t.status
        })
    return result


@router.get('/{transaction_id}')
def get_transaction(transaction_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(
        (Transaction.id == transaction_id) & (Transaction.user_id == current_user['id'])
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail='Transakcija nije pronađena')
    
    return {
        'id': str(transaction.id),
        'user_id': str(transaction.user_id),
        'amount': transaction.amount,
        'merchant_name': transaction.merchant_name,
        'transaction_date': str(transaction.transaction_date),
        'status': transaction.status
    }


@router.put('/{transaction_id}')
def update_transaction(transaction_id: str, transaction: TransactionCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_transaction = db.query(Transaction).filter(
        (Transaction.id == transaction_id) & (Transaction.user_id == current_user['id'])
    ).first()
    
    if not existing_transaction:
        raise HTTPException(status_code=404, detail='Transakcija nije pronađena')
    
    existing_transaction.amount = transaction.amount
    existing_transaction.merchant_name = transaction.merchant_name
    existing_transaction.transaction_date = transaction.transaction_date
    existing_transaction.status = transaction.status
    
    db.commit()
    db.refresh(existing_transaction)
    
    return {
        'id': str(existing_transaction.id),
        'user_id': str(existing_transaction.user_id),
        'amount': existing_transaction.amount,
        'merchant_name': existing_transaction.merchant_name,
        'transaction_date': str(existing_transaction.transaction_date),
        'status': existing_transaction.status
    }


@router.delete('/{transaction_id}')
def delete_transaction(transaction_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(
        (Transaction.id == transaction_id) & (Transaction.user_id == current_user['id'])
    ).first()
    
    if not transaction:
        raise HTTPException(status_code=404, detail='Transakcija nije pronađena')
    
    db.delete(transaction)
    db.commit()
    
    return {'message': 'Transakcija je obrisana'}

