📘 Healthcare Patient Management System

A full-stack web application designed to manage, analyse, and visualise healthcare patient data (stroke dataset).
Built using Flask, MongoDB, SQLite, Chart.js, and Bootstrap.

🔍 Features
✅ User Authentication (SQLite + SQLAlchemy)

Secure registration & login (password hashing).

Role-based access control:

Admin → full CRUD + delete + user management + dashboard.

Staff → limited access (view/edit only, no delete).

✅ Patient Management (MongoDB)

Create, read, update, delete patient records.

Search and filter patients.

Paginated patient list.

CSV dataset import with automatic cleaning.

✅ Analytics Dashboard

Visual insights using Chart.js:

Total patients

Stroke vs Non-Stroke

Stroke Rate (%)

Patients by Gender

Patients by Age Band

High-Risk Stroke Patients table

✅ Security Features

Password hashing (Werkzeug).

CSRF protection.

Input validation (WTForms).

Protected routes using Flask-Login.

📁 Project Structure
project/
│── app/
│   ├── routes/
│   │    ├── auth.py
│   │    ├── patients.py
│   │    ├── main.py
│   ├── templates/
│   ├── models.py
│   ├── decorators.py
│   ├── forms.py
│── static/
│── healthcare-dataset-stroke-data.csv
│── run.py
│── README.md
│── requirements.txt

⚙️ Installation Guide
1️⃣ Clone the repository
git clone https://github.com/<your-username>/patient-app.git
cd patient-app

2️⃣ Create virtual environment
python -m venv venv

3️⃣ Activate environment

PowerShell

.\venv\Scripts\Activate.ps1


CMD

venv\Scripts\activate.bat


Git Bash

source venv/Scripts/activate

4️⃣ Install dependencies
pip install -r requirements.txt

5️⃣ Run the app
python run.py

🛢 Database Information
SQLite

Used for:

User accounts

Roles (admin/staff)

MongoDB

Used for:

Patient records

Analytics queries

📊 Dashboard Analytics

The dashboard displays:

Total Patients

Stroke Cases

Stroke Rate (%)

Stroke vs No-Stroke (Donut Chart)

Gender Distribution (Bar Chart)

Age Band Distribution (Bar Chart)

High-Risk Stroke Patients (Table)

🔐 Security Implementation

Password hashing using generate_password_hash()

CSRF protection via Flask-WTF

Role-based decorators (admin_required)

Safe database queries

Secure session management

🧪 Testing

Manual UI testing

Login/logout validation

MongoDB connection handling

CSV import verification

Error handling for missing dataset

📈 Future Improvements

Password reset system

Two-factor authentication

API endpoints for mobile app integration

Export analytics as PDF/CSV

More advanced charts and filters

👨‍💻 Author

2415337 (Mohammad Rahaman)
COM7033 Software Engineering – Patient Management System
