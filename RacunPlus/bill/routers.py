from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from RacunPlus.database import SessionLocal
from RacunPlus.user.routers import get_current_user
from .models import Bill

router = APIRouter(prefix='/bills', tags=['bills'])


class BillCreate(BaseModel):
    amount: float
    beneficiary_name: str
    reference_date: date
    status: str = 'paid'


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.post('/create', status_code=201)
def create_bill(bill: BillCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    new_bill = Bill(
        user_id=current_user['id'],
        amount=bill.amount,
        beneficiary_name=bill.beneficiary_name,
        reference_date=bill.reference_date,
        status=bill.status
    )
    db.add(new_bill)
    db.commit()
    db.refresh(new_bill)
    
    return {
        'id': str(new_bill.id),
        'user_id': str(new_bill.user_id),
        'amount': new_bill.amount,
        'beneficiary_name': new_bill.beneficiary_name,
        'reference_date': str(new_bill.reference_date),
        'status': new_bill.status,
        'created_at': str(new_bill.created_at)
    }


@router.get('/list')
def list_bills(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    bills = db.query(Bill).filter(Bill.user_id == current_user['id']).all()
    result = []
    for b in bills:
        result.append({
            'id': str(b.id),
            'user_id': str(b.user_id),
            'amount': b.amount,
            'beneficiary_name': b.beneficiary_name,
            'reference_date': str(b.reference_date),
            'status': b.status,
            'created_at': str(b.created_at)
        })
    return result


@router.get('/{bill_id}')
def get_bill(bill_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(
        (Bill.id == bill_id) & (Bill.user_id == current_user['id'])
    ).first()
    
    if not bill:
        raise HTTPException(status_code=404, detail='Račun nije pronađen')
    
    return {
        'id': str(bill.id),
        'user_id': str(bill.user_id),
        'amount': bill.amount,
        'beneficiary_name': bill.beneficiary_name,
        'reference_date': str(bill.reference_date),
        'status': bill.status,
        'created_at': str(bill.created_at)
    }


@router.put('/{bill_id}')
def update_bill(bill_id: str, bill: BillCreate, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_bill = db.query(Bill).filter(
        (Bill.id == bill_id) & (Bill.user_id == current_user['id'])
    ).first()
    
    if not existing_bill:
        raise HTTPException(status_code=404, detail='Račun nije pronađen')
    
    existing_bill.amount = bill.amount
    existing_bill.beneficiary_name = bill.beneficiary_name
    existing_bill.reference_date = bill.reference_date
    existing_bill.status = bill.status
    
    db.commit()
    db.refresh(existing_bill)
    
    return {
        'id': str(existing_bill.id),
        'user_id': str(existing_bill.user_id),
        'amount': existing_bill.amount,
        'beneficiary_name': existing_bill.beneficiary_name,
        'reference_date': str(existing_bill.reference_date),
        'status': existing_bill.status,
        'created_at': str(existing_bill.created_at)
    }


@router.delete('/{bill_id}')
def delete_bill(bill_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    bill = db.query(Bill).filter(
        (Bill.id == bill_id) & (Bill.user_id == current_user['id'])
    ).first()
    
    if not bill:
        raise HTTPException(status_code=404, detail='Račun nije pronađen')
    
    db.delete(bill)
    db.commit()
    
    return {'message': 'Račun je obrisan'}

