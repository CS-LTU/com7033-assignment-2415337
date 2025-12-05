Healthcare Patient Management System – Final Report (Humanised Version)
1. Introduction

This project focuses on developing a Healthcare Patient Management System using Flask, SQLite, and MongoDB. The aim was to build a secure and easy-to-use web application that can store, manage, and analyse patient information from a stroke-related dataset.

Throughout the development, I worked on user authentication, CRUD operations, data validation, search filters, and an analytics dashboard. The system supports two types of users—Admin and Staff—and provides different access rights depending on their role. The project allowed me to apply real software engineering principles, including secure coding practices, ethical considerations, and professional documentation.

2. System Overview

The system is designed around two major parts:

The authentication and user management system

The patient database and analytics system

2.1 Authentication System (SQLite + SQLAlchemy)

Users can create accounts, log in, and log out securely. Passwords are stored as hashed values, which helps protect user data. The application automatically assigns the first registered account as an Admin, while all later users become Staff by default.

Admin users have full control: they can create, edit, and delete patient data, import datasets, and view the analytics dashboard.

Staff users have limited access—they can view patients and the dashboard, but they cannot delete or import data.

This design follows the principle of least privilege, reducing risks when dealing with healthcare records.

2.2 Patient Data Management (MongoDB)

MongoDB is used to store all patient information. Each entry includes:

Age

Gender

Smoking status

BMI

Average glucose level

Hypertension and heart disease status

Stroke outcome

The system allows:

Adding new patients

Updating existing records

Deleting records (Admin only)

Searching by patient ID, gender, smoking status, and work type

Importing the entire dataset directly from a CSV file

This makes the application suitable for working with larger datasets and for supporting data-driven decision making.

3. Key Features of the System
3.1 User Authentication

The system includes registration, login, and logout. Password hashing ensures that passwords remain protected even if the database is compromised. Role assignment is automatic and ensures a clear separation of responsibilities.

3.2 Role-Based Access Control
Feature	Admin	Staff
View patients	✔	✔
Edit patients	✔	Limited
Delete patients	✔	✖
Import CSV	✔	✖
View dashboard	✔	✔
Manage users	✔	✖
3.3 Patient CRUD System

The CRUD interface allows:

Browsing patient entries with pagination

Searching for patients using multiple criteria

Adding new patient information via forms

Editing existing patient data

Deleting patient records (restricted to Admins)

All forms use validation to prevent incorrect or unsafe inputs.

3.4 Dashboard & Analytics

The dashboard displays visual statistics such as:

Total number of patients

Stroke vs non-stroke distribution

Stroke rate percentage

Gender distribution

Age band distribution

A list of high-risk patients

These charts are implemented using Chart.js, and they provide a clear visual summary of trends in the dataset.

3.5 Dataset Import Tool

The import function:

Clears existing MongoDB data

Loads records from the stroke dataset

Cleans and converts numeric fields like BMI and glucose levels

This makes it easy to refresh or reset the database during development or testing.

4. Technologies Used
Component	Technology
Backend	Flask
User Database	SQLite + SQLAlchemy
Patient Database	MongoDB
Authentication	Flask-Login
Frontend	HTML + Bootstrap
Form Handling	Flask-WTF
Visualisation	Chart.js
Security	Werkzeug password hashing
5. Software Design
5.1 Project Structure
project/
│── app/
│   ├── routes/ (auth, patients, main)
│   ├── templates/
│   ├── models.py
│   ├── forms.py
│   ├── decorators.py
│── static/
│── run.py


This structure keeps the project modular and easier to maintain.

5.2 Security Implementation

Security was a major focus of the project. Measures include:

Password hashing using Werkzeug

CSRF protection on all forms

Access control using decorators

Input validation through WTForms

Session management via Flask-Login

These help protect patient data and ensure secure communication between the user and the server.

6. Dashboard Analytics

The dashboard summarises key patterns in the stroke dataset.

6.1 Stroke Rate

The stroke rate is calculated as:

stroke_rate = (stroke_yes / total) * 100


This gives a quick snapshot of stroke prevalence.

6.2 Age Band Distribution

Patients are grouped into:

0–20

21–40

41–60

61–80

80+

This makes it easier to see how stroke and risk factors vary by age.

6.3 High-Risk Patients

A separate table highlights patients who meet all of the following:

Stroke = 1

Glucose levels above 200

Age above 60

This could help healthcare workers identify cases needing urgent follow-up.

7. Testing and Validation
7.1 Functional Testing

The following features were fully tested:

Registration and login

Staff vs admin permissions

Add/edit/delete patient records

Search and pagination

Dashboard and charts

CSV import

MongoDB connectivity

7.2 Error Handling

The system gracefully handles:

Missing data

Invalid form inputs

Failed database connections

Unauthorized access

These tests ensure a more reliable user experience.

8. Limitations

Some limitations of the current system include:

No password reset or email verification

Staff cannot edit all fields

No export-to-CSV option

Analytics do not include advanced trends or predictions

9. Future Enhancements

Potential improvements could include:

Adding two-factor authentication

Allowing users to export data

Integrating a machine learning model for stroke prediction

Supporting medical notes per patient

Deploying the system online

Adding a mobile-friendly API

10. Conclusion

This project successfully delivers a secure and functional healthcare management system. It demonstrates full CRUD capability, role-based access, data validation, an interactive dashboard, and safe handling of sensitive data.

The application meets the assessment requirements for design, implementation, and professional practice. It also provides a strong foundation for future enhancements and advanced data analytics in healthcare environments.


📦 How to Run the Application (After Downloading ZIP)

Follow these steps exactly to run the project successfully on any Windows machine.

✅ 1. Download the Project

Visit your GitHub repository.

Click Code → Download ZIP

Extract the ZIP file to a folder, for example:

C:\Users\YourName\Desktop\patient-app

✅ 2. Open the Project in VS Code

Open Visual Studio Code

Go to File → Open Folder

Select the extracted patient-app folder.

✅ 3. Create and Activate a Virtual Environment

Open a terminal in VS Code (Terminal → New Terminal) and run:

Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate


If activation is blocked, run this command first:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass


Then activate again:

.\venv\Scripts\activate


You should now see:

(venv) PS C:\Users\...\patient-app>

✅ 4. Install All Required Python Packages

Run:

pip install -r requirements.txt


This installs:

Flask

Flask-Login

Flask-WTF

SQLAlchemy

PyMongo

Werkzeug

WTForms

Chart.js dependencies, etc.

✅ 5. Set Up Databases
SQLite (Automatic)

Nothing to do.
It creates a file app.db automatically on first run.

MongoDB

You must have MongoDB installed and running.

If using MongoDB Atlas (cloud), update this line inside __init__.py:

app.config["MONGO_URI"] = "your MongoDB connection string"

✅ 6. Run the Application

In the same activated virtual environment, run:

python run.py


If successful, you will see:

Running on http://127.0.0.1:5000  (Press CTRL+C to quit)

✅ 7. Open the App in Your Browser

Go to:

👉 http://127.0.0.1:5000
