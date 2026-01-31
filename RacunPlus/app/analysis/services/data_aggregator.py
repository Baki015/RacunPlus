from datetime import date, timedelta
from typing import List, Tuple, Dict, Any
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from RacunPlus.bill.models import Bill


CATEGORY_MAP = {
    "EPCG": "Electricity",
    "Vodovod": "Water",
    "Telemach": "Internet",
    "Crnogorski Telekom": "Phone",
}


def detect_category(provider: str) -> str:
    return CATEGORY_MAP.get(provider.strip(), "Other")


def fetch_user_bills(
    db: Session,
    user_id: str,
    days: int,
) -> Tuple[List[Dict[str, Any]], date, date]:

    end = date.today()
    start = end - timedelta(days=days)

    bills = db.query(Bill).filter(
        Bill.user_id == user_id,
        Bill.reference_date >= start,
        Bill.reference_date <= end,
    ).all()
    
    bills_data = []
    for bill in bills:
        bills_data.append({
            'id': str(bill.id),
            'user_id': str(bill.user_id),
            'beneficiary_name': bill.beneficiary_name,
            'amount': bill.amount,
            'reference_date': bill.reference_date,
            'status': bill.status,
            'category': detect_category(bill.beneficiary_name)
        })
    
    return bills_data, start, end


def format_bills_for_prompt(bills: List[Dict[str, Any]]) -> str:
    lines = []

    for b in bills:
        provider = b['beneficiary_name']
        category = b['category']
        lines.append(
            f"- {provider} ({category}): €{b['amount']:.2f} ({b['reference_date']})"
        )
    
    return "\n".join(lines)

    return lines
