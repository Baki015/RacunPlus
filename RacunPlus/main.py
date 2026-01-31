from fastapi import FastAPI
from RacunPlus.user.routers import router as user_router
from RacunPlus.bill.routers import router as bill_router
from RacunPlus.transaction.routers import router as transaction_router
from RacunPlus.app.analysis.api.analysis import router as analysis_router

app = FastAPI(title="RacunPlus")

app.include_router(user_router)
app.include_router(bill_router)
app.include_router(transaction_router)
app.include_router(analysis_router)