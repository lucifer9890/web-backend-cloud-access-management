# ☁️ Cloud Service Access Management System

This FastAPI backend manages access to simulated cloud APIs using subscription plans, permissions, and usage tracking. It demonstrates role-based access control (RBAC), dynamic plan enforcement, and real-time API usage limits.

---

## 🚀 Key Features

- 🔐 Role-Based Access Control (Admin, Customer)
- 📦 Subscription Plan Management
- 🔧 API Access Permissions (with categories)
- 📊 Usage Tracking and Limit Enforcement
- ⚡ FastAPI + SQLAlchemy + SQLite (Async)

---

## 🧪 API Endpoints

Visit the auto-generated docs:

📍 `http://127.0.0.1:8000/docs`

| Endpoint Group         | Description                      |
|------------------------|----------------------------------|
| `/subscription-plans` | Manage API plans & limits        |
| `/api-access`          | Define accessible APIs           |
| `/user-subscriptions`  | Assign/view user plans           |
| `/usage-logs`          | Track API usage                  |

---

## 🧱 Setup Instructions

1. **Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/cloud-access-management.git
cd cloud-access-management
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
.env\Scriptsctivate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
python init_db.py
```

5. **Start the server**
```bash
uvicorn app.main:app --reload
```

---

## 📹 Demo Recording Tips

- Run `uvicorn` and show Swagger UI
- Create a plan, add permissions, assign to a user
- Simulate API usage and show automatic access blocking
- Conclude with usage tracking and reporting

---

## 👥 Team Members

- Hitesh
- [Add more here]

---

## 📄 License

This project is for educational use only.
