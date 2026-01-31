# 💰 RacunPlus - Aplikacija za Upravljanje Računima sa AI Analizom

FastAPI aplikacija za praćenje računa, transakcija i AI-powered finansijsku analizu koristeći Google Gemini.

---

## 📋 Šta Radi Aplikacija?

RacunPlus omogućava korisnicima da:
- 👤 **Registruju se i loguju** sa JWT autentifikacijom
- 📄 **Kreiraju i upravljaju računima** (struja, voda, internet, telefon)
- 💳 **Prate transakcije** (plaćanja, uplate)
- 🤖 **Dobiju AI analizu** njihovih rashoda sa preporukama za uštedu

---

## 🛠️ Tehnologije

- **Backend**: FastAPI (Python 3.12)
- **Baza**: PostgreSQL
- **Auth**: JWT tokeni + bcrypt password hashing
- **AI**: Google Gemini API (gemini-2.0-flash-exp)
- **Testing**: pytest
- **ORM**: SQLAlchemy
- **Migrations**: Alembic


## ⚙️ Instalacija i Pokretanje

### 1. Preduslovi
- Python 3.12+
- PostgreSQL
- Google Gemini API Key

### 2. Kloniraj Repo
```powershell
cd C:\Users\User\Documents\fastapi\ProjekatBalsa
```

### 3. Aktiviraj Virtual Environment
```powershell
..\fastapienv\Scripts\Activate.ps1
```

### 4. Instaliraj Pakete
```powershell
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-jose[cryptography] passlib[bcrypt] python-multipart google-generativeai pydantic-settings python-dotenv pytest
```

### 5. Konfiguriši .env Fajl
Kreiraj `.env` fajl u root-u projekta:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/racunplus
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash-exp
```

### 6. Pokreni Migracije
```powershell
alembic upgrade head
```

### 7. Pokreni Server
```powershell
python -m uvicorn RacunPlus.main:app --reload
```
Server ce biti dostupan na: **http://localhost:8000**
