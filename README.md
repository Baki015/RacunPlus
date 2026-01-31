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

---

## 📁 Struktura Projekta

```
ProjekatBalsa/
├── RacunPlus/              # Glavni source kod
│   ├── main.py            # Entry point - FastAPI app
│   ├── settings.py        # Konfiguracija (DB, API keys)
│   ├── database.py        # PostgreSQL konekcija
│   ├── security.py        # JWT logika
│   │
│   ├── user/              # Korisnici i autentifikacija
│   │   ├── models.py      # User model
│   │   └── routers.py     # /auth endpoints
│   │
│   ├── bill/              # Računi
│   │   ├── models.py      # Bill model
│   │   └── routers.py     # /bills endpoints
│   │
│   ├── transaction/       # Transakcije
│   │   ├── models.py      # Transaction model
│   │   └── routers.py     # /transactions endpoints
│   │
│   └── app/analysis/      # AI Analiza
│       ├── api/
│       │   └── analysis.py          # /analysis endpoints
│       ├── models/analysis.py       # Analysis model
│       ├── schemas/analysis.py      # Pydantic schemas
│       ├── services/
│       │   ├── analysis.py          # Business logika
│       │   ├── ai_service.py        # Gemini AI pozivi
│       │   └── data_aggregator.py   # Data processing
│       ├── database/analysis.py     # DB queries
│       └── exceptions/analysis.py   # Custom errors
│
├── tests/                  # Testovi
│   ├── test_auth.py       # Auth testovi
│   ├── test_bills.py      # Bill testovi
│   ├── test_transactions.py
│   └── test_analysis.py   # AI analiza testovi
│
├── alembic/               # Database migrations
├── .env                   # Environment varijable
├── alembic.ini           # Alembic config
└── PROJEKAT_OBJASNJENJE.md  # Detaljna dokumentacija
```

---

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

Server će biti dostupan na: **http://localhost:8000**

---

## 🧪 Testiranje

Pokreni sve testove:
```powershell
python -m pytest tests/ -v
```

Testovi pokrivaju:
- ✅ Registraciju i login
- ✅ CRUD operacije za račune
- ✅ CRUD operacije za transakcije
- ✅ AI analizu (monthly i category)
- ✅ JWT autentifikaciju

**Status**: 12/12 testova PASSED ✅

---

## 📡 API Endpoints

### 🔐 Autentifikacija (`/auth`)
```http
POST /auth/register       # Registruj novog korisnika
POST /auth/login          # Login i dobij JWT token
GET  /auth/current-user   # Dobij trenutnog korisnika
```

### 📄 Računi (`/bills`)
```http
POST   /bills/create      # Kreiraj račun
GET    /bills/list        # Lista svih računa
GET    /bills/{id}        # Jedan račun
PUT    /bills/{id}        # Ažuriraj račun
DELETE /bills/{id}        # Obriši račun
```

### 💳 Transakcije (`/transactions`)
```http
POST   /transactions/create      # Kreiraj transakciju
GET    /transactions/list        # Lista svih transakcija
GET    /transactions/{id}        # Jedna transakcija
PUT    /transactions/{id}        # Ažuriraj transakciju
DELETE /transactions/{id}        # Obriši transakciju
```

### 🤖 AI Analiza (`/analysis`)
```http
POST   /analysis/generate        # Generiši AI analizu
GET    /analysis/latest          # Zadnja analiza
GET    /analysis/history         # Historija analiza
GET    /analysis/{id}            # Jedna analiza
DELETE /analysis/{id}            # Obriši analizu
```

---

## 🔑 Kako Koristiti API?

### 1. Registracija
```powershell
$body = @{
    username = "marko"
    email = "marko@example.com"
    password = "pass123"
    first_name = "Marko"
    last_name = "Markovic"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/auth/register" -Method POST -Body $body -ContentType "application/json"
```

### 2. Login
```powershell
$loginData = @{
    username = "marko"
    password = "pass123"
}

$response = Invoke-RestMethod -Uri "http://localhost:8000/auth/login" -Method POST -Body $loginData -ContentType "application/x-www-form-urlencoded"

$token = $response.access_token
```

### 3. Kreiraj Račun
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

$bill = @{
    amount = 150.50
    beneficiary_name = "EPS"
    reference_date = "2026-01-27"
    status = "paid"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/bills/create" -Method POST -Headers $headers -Body $bill -ContentType "application/json"
```

### 4. Generiši AI Analizu
```powershell
$analysis = @{
    analysis_type = "monthly"
    days = 30
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/analysis/generate" -Method POST -Headers $headers -Body $analysis -ContentType "application/json"
```

---

## 🤖 AI Analiza - Tipovi

### 📅 Monthly Analysis
Analizira sve račune za određeni period i vraća:
- Ukupan iznos potrošnje
- Breakdown po provajderima
- AI-generisane preporuke za uštedu

**Primjer zahtjeva:**
```json
{
  "analysis_type": "monthly",
  "days": 30
}
```

### 📊 Category Analysis
Grupiše račune po kategorijama (provajderima) i vraća:
- Procentualni raspored rashoda
- Insights za svaku kategoriju
- Specifične preporuke po kategorijama

**Primjer zahtjeva:**
```json
{
  "analysis_type": "category",
  "days": 30
}
```

**Rate Limiting**: Max 10 analiza po danu po korisniku

---

## 🗄️ Database Schema

### `users` tabela
- `id` (UUID) - Primary key
- `username` (String) - Jedinstveno
- `email` (String) - Jedinstveno
- `password_hash` (String) - Bcrypt hash
- `first_name`, `last_name`
- `created_at`

### `bills` tabela
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key → users
- `amount` (Float)
- `beneficiary_name` (String) - Provajder
- `reference_date` (Date)
- `status` (String) - "paid" ili "unpaid"
- `created_at`, `updated_at`

### `transactions` tabela
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key → users
- `amount` (Float)
- `merchant_name` (String)
- `transaction_date` (Date)
- `status` (String) - "completed" ili "pending"
- `created_at`, `updated_at`

### `analysis` tabela
- `id` (UUID) - Primary key
- `user_id` (UUID) - Foreign key → users
- `analysis_type` (String) - "monthly" ili "category"
- `days` (Integer)
- `result` (JSON) - AI odgovor
- `created_at`

---

## 🔒 Sigurnost

- **JWT Tokeni**: Svaki zahtjev osim `/auth/register` i `/auth/login` zahtijeva Bearer token
- **Password Hashing**: Bcrypt algoritam sa salt-om
- **User Isolation**: Korisnik vidi samo svoje podatke
- **Rate Limiting**: Max 10 AI analiza po danu
- **Environment Variables**: Senzitivne informacije u `.env` fajlu

---

## 📊 HTTP Status Kodovi

| Status | Značenje |
|--------|----------|
| 200 | OK - Uspješan zahtjev |
| 201 | Created - Nova stavka kreirana |
| 401 | Unauthorized - Nema/nevažeći token |
| 403 | Forbidden - Nema pristupa |
| 404 | Not Found - Stavka ne postoji |
| 429 | Too Many Requests - Rate limit |
| 500 | Internal Server Error |

---

## 📚 Dodatna Dokumentacija

Za detaljnije objašnjenje cijele logike projekta, pogledaj:
- **`PROJEKAT_OBJASNJENJE.md`** - Kompletna dokumentacija sa dijagramima i primjerima

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError"
**Rješenje**: Provjeri da li je virtual environment aktiviran
```powershell
..\fastapienv\Scripts\Activate.ps1
```

### Problem: "Connection refused" na bazi
**Rješenje**: Provjeri da li je PostgreSQL pokrenut
```powershell
# Provjeri servis
Get-Service postgresql*
```

### Problem: Testovi ne prolaze
**Rješenje**: Provjeri da li je baza kreirana i migracije pokrenute
```powershell
alembic upgrade head
```

### Problem: Gemini API greška
**Rješenje**: Provjeri `.env` fajl da li je `GEMINI_API_KEY` postavljen

---

## 👨‍💻 Development

### Kreiraj novu migraciju
```powershell
alembic revision --autogenerate -m "Opis promjene"
alembic upgrade head
```

### Pokreni testove sa coverage
```powershell
python -m pytest tests/ --cov=RacunPlus --cov-report=html
```

### Debug mode
```powershell
uvicorn RacunPlus.main:app --reload --log-level debug
```

---

## 📝 Licenca

Privatni projekat - sva prava zadržana.

---

## 🙋 Support

Za pitanja i probleme, pogledaj `PROJEKAT_OBJASNJENJE.md` za detaljnu dokumentaciju.

**Status**: ✅ Fully Functional | 🧪 12/12 Tests Passing | 🤖 AI-Powered
