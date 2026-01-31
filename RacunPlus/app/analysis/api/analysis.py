from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from RacunPlus.database import SessionLocal
from RacunPlus.user.routers import get_current_user
from RacunPlus.app.analysis.models.analysis import Analysis
from RacunPlus.app.analysis.schemas.analysis import AnalysisGenerateRequest
from RacunPlus.app.analysis.services.analysis import generate_analysis, analysis_to_response
from RacunPlus.app.analysis.exceptions.analysis import RateLimitExceededError, NoBillsFoundError

router = APIRouter(prefix='/analysis', tags=['analysis'])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@router.post('/generate', status_code=201)
def generate(payload: AnalysisGenerateRequest, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        user_id = current_user['id']
        analysis = generate_analysis(db, user_id, payload.analysis_type, payload.days)
        return {'success': True, 'data': analysis_to_response(analysis)}
    except RateLimitExceededError as e:
        raise HTTPException(status_code=429, detail=str(e))
    except NoBillsFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get('/latest')
def latest(analysis_type: str = None, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user['id']
    query = db.query(Analysis).filter(Analysis.user_id == user_id)
    
    if analysis_type:
        query = query.filter(Analysis.analysis_type == analysis_type)
    
    analysis = query.order_by(Analysis.created_at.desc()).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail='Analiza nije pronađena')
    
    return {'success': True, 'data': analysis_to_response(analysis)}


@router.get('/history')
def history(limit: int = Query(10), offset: int = Query(0), current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user['id']
    
    analyses = db.query(Analysis).filter(
        Analysis.user_id == user_id
    ).order_by(Analysis.created_at.desc()).offset(offset).limit(limit).all()
    
    total = len(analyses)
    
    return {
        'success': True,
        'data': {
            'analyses': [analysis_to_response(a) for a in analyses],
            'total': total,
        },
    }


@router.get('/{analysis_id}')
def get_analysis(analysis_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user['id']
    
    analysis = db.query(Analysis).filter(
        (Analysis.id == analysis_id) & (Analysis.user_id == user_id)
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail='Analiza nije pronađena')
    
    return {'success': True, 'data': analysis_to_response(analysis)}


@router.delete('/{analysis_id}')
def delete_analysis(analysis_id: str, current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = current_user['id']
    
    analysis = db.query(Analysis).filter(
        (Analysis.id == analysis_id) & (Analysis.user_id == user_id)
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail='Analiza nije pronađena')
    
    db.delete(analysis)
    db.commit()
    
    return {'success': True, 'message': 'Analiza je obrisana'}

