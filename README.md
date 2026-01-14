
# MECS Backend (Django REST API)

Backend service untuk **Manufacturing Execution Control System (MECS)**  
Dibangun menggunakan **Django + Django REST Framework** dengan autentikasi **JWT**.

---

## 🧱 Tech Stack

- Python 3.11+
- Django 5.x
- Django REST Framework
- PostgreSQL
- Simple JWT
- Django CORS Headers

---

## 📂 Project Structure

```text
mecs/
├── mecs/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/      # user, employee, operator, auth
│   ├── master/        # master data (machine, part, parameter, capacity, reject, problem)
│   ├── core/          # scheduling, production, operation, report
│   └── common/        # shared utilities (optional)
├── manage.py
└── requirements.txt
````

---

## ⚙️ Environment Setup

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Environment Variables

Buat file `.env` di root project:

```env
DEBUG=True
SECRET_KEY=your-secret-key

DB_NAME=mecs
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

CORS_ALLOWED_ORIGINS=http://localhost:3000
```

---

### 4️⃣ Database Migration

```bash
python manage.py makemigrations
python manage.py migrate
```

---

### 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

---

### 6️⃣ Run Development Server

```bash
python manage.py runserver
```

API tersedia di:

```
http://localhost:8000/api/
```

---

## 🔐 Authentication (JWT)

Menggunakan **Simple JWT**

### Login

```
POST /api/auth/login/
```

Body:

```json
{
  "username": "admin",
  "password": "password"
}
```

Response:

```json
{
  "access": "jwt-access-token",
  "refresh": "jwt-refresh-token"
}
```

### Refresh Token

```
POST /api/auth/refresh/
```

---

### Authorization Header

Gunakan token di setiap request API:

```
Authorization: Bearer <access_token>
```

---

## 🧩 Core Modules

### Accounts

* Users
* Employees
* Operators
* Groups & Permissions

### Master

* Parts
* Machines
* Production Parameters
* Production Capacity (auto-calculated)
* Reject Category
* Problem Category

### Core

* Daily Production
* Schedule
* Production
* Production Operation
* Reject & Problem Logs

---

## 🧠 Production Parameter & Capacity Logic

* **ProductionParameter** → input manual
* **ProductionCapacity** → hasil perhitungan otomatis
* Capacity **tidak boleh diinput manual**
* Dibuat / diupdate otomatis saat parameter create / update

---

## 📌 API Convention

| Method | Endpoint                                 | Description                 |
| ------ | ---------------------------------------- | --------------------------- |
| GET    | `/api/masters/parameters/`               | List parameter              |
| POST   | `/api/masters/parameters/`               | Create parameter + capacity |
| PUT    | `/api/masters/parameters/{id}/`          | Update parameter + capacity |
| GET    | `/api/masters/parameters/{id}/capacity/` | Read capacity (readonly)    |
| DELETE | `/api/masters/parameters/{id}/`          | Delete parameter            |

---

## 🔒 Permissions (Groups)

Permissions dikontrol via **Django Groups**:

* admin
* ppc
* operator
* leader
* supervisor

Digunakan melalui custom DRF permissions.

---

## 📷 Media Files

Media (photo, reject image, dll):

```python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

Pastikan di `urls.py`:

```python
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

---

## 🧪 Testing

```bash
python manage.py test
```

---

## 🛠 Common Issues

* ❌ 401 Unauthorized → token expired / missing
* ❌ 403 Forbidden → group permission tidak sesuai
* ❌ Capacity error → cycle_time = 0 / cavity = 0
* ❌ CORS error → cek `CORS_ALLOWED_ORIGINS`

---

## 📎 Notes

* Backend ini **API-only**
* Frontend disiapkan untuk:

  * Next.js
  * React Native

---

## 👤 Maintainer

**MECS Development Team**
Backend by Django REST Framework
