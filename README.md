# WorkSphere — Enterprise HR & Workforce Management Platform
> **Tagline**: *"One Platform for Every Workforce"*

[![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-5.0.3-green)](https://www.djangoproject.com/)
[![Architecture](https://img.shields.io/badge/Architecture-Django%20MVT-orange)](https://docs.djangoproject.com/)
[![License](https://img.shields.io/badge/License-Proprietary-red)](#)
[![Status](https://img.shields.io/badge/Build-Passing-brightgreen)](#)

---

## 📖 Overview

**WorkSphere** is a complete, production-grade enterprise Human Resource and Workforce Management Platform (HRMS) engineered to manage multi-tenant organizations, 13-role RBAC security, recruitment ATS, employee lifecycle, biometric attendance, rotational shift rostering, leave quotas, payroll execution, benefits administration, expense claims, corporate travel, 360-degree performance appraisals, training LMS, IT hardware assets, documents vault, and real-time executive analytics.

---

## 🚀 Key Modules & Capabilities

- **Multi-Tenant Foundation & 13 RBAC Roles**: Super Admin, Org Admin, HR Manager, Recruiter, Payroll Manager, Finance Manager, Dept Manager, Team Lead, Employee, Training Manager, IT/Asset Manager, Support Agent.
- **Talent & Recruitment (ATS)**: Visual Kanban pipeline, candidate scoring, interview schedules, scorecard rubrics, and digital offer letters.
- **Onboarding & Offboarding**: Automated role-based onboarding checklists and 5-department exit clearance workflows.
- **Attendance & Timesheets**: Live punch desk with IP capture, automatic work hour calculations, half-day detection, and regularization approvals.
- **Shifts & Rostering**: 24/7 rotational shift schedules (DuPont, 2-2-3 Pitman, Panama) and peer shift swap requests.
- **Leave Management & Holidays**: Annual leave quotas (PTO, Sick, Casual), live balance deduction engine, and multi-day approval queues.
- **Financial & Payroll Processing**: Configurable salary bands (L1–L6), automated monthly payroll execution, statutory deductions, bank masking, and printable payslips.
- **Benefits Administration**: Comprehensive plans (Health PPO, 401k match, wellness) and employee enrollment portal.
- **Expenses & Corporate Travel**: Itemized expense claim receipt attachments, GSA per-diem rules, and travel requisitions with PNR generation.
- **Performance & OKRs**: 360-degree appraisal reviews, 9-Box talent matrix, and strategic OKR goal tracking.
- **Training LMS Academy**: Course catalog, lesson modules, self-enrollment, and certificate generation.
- **IT Hardware & Asset Governance**: Asset tagging (`AST-MBP-9001`), serial numbers, warranty tracking, and allocation lifecycles.
- **Corporate Documents Vault**: Granular permission-based document repository for policies, codes of conduct, and NDAs.
- **HR & IT Helpdesk**: Multi-category support desk with SLA countdowns and discussion threads.
- **Executive Analytics & Reports**: Interactive Chart.js workforce dashboards, payroll run-rate metrics, and scheduled reports.

---

## 🛠️ Tech Stack & Dependencies

- **Backend Framework**: Python 3.10+ / Django 5.0.3
- **Database**: SQLite (`db.sqlite3` default) / PostgreSQL compatible
- **Async Workers & Tasks**: Celery 5.3.6 & Redis
- **Frontend / UI**: Django Templates (MVT), HTML5, CSS3 Custom Design System Tokens, Vanilla JavaScript, Chart.js, FontAwesome 6
- **Testing & Quality**: Django Test Framework, Pytest, Coverage

---

## ⚙️ Installation & Setup

### Prerequisites
- Python 3.10, 3.11, or 3.12
- Git
- Pip / Virtualenv

### Step 1: Clone Repository
```bash
git clone https://github.com/Bhola-11/Employee-Management.git
cd Employee-Management
```

### Step 2: Create & Activate Virtual Environment
```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏗️ Build & Database Initialization

### Apply Database Migrations
```bash
python manage.py migrate
```

### Seed Master Enterprise Demo Data
```bash
python manage.py seed_hrms_data
```

---

## ▶️ Running the Application

### Option A: Standard Django Development Server
```bash
python manage.py runserver
```
Navigate to `http://127.0.0.1:8000/` in your browser.

### Option B: Standalone Python Entry Point
```bash
python main.py
```
or
```bash
python app.py
```

### Option C: Celery Background Worker
```bash
celery -A worksphere worker -l info
```

---

## 🐳 Docker Deployment

### Using Docker Compose
```bash
# Build and run containers
docker-compose up --build -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f
```

---

## 🧪 Running Automated Tests

```bash
# Run all unit and integration test suites
python manage.py test

# Run tests with Pytest
pytest
```

---

## 🔐 Default Enterprise Demo Accounts

| Role | Email | Password |
| :--- | :--- | :--- |
| **Super Admin** | `superadmin@worksphere.io` | `WorkSphere@2026!` |
| **Org Admin** | `orgadmin@worksphere.io` | `WorkSphere@2026!` |
| **HR Manager** | `hrmanager@worksphere.io` | `WorkSphere@2026!` |
| **Payroll Manager** | `payroll@worksphere.io` | `WorkSphere@2026!` |
| **Finance Manager** | `finance@worksphere.io` | `WorkSphere@2026!` |
| **Recruiter** | `recruiter@worksphere.io` | `WorkSphere@2026!` |
| **Employee** | `employee@worksphere.io` | `WorkSphere@2026!` |

---

## 📄 License & Proprietary Notice

Copyright © 2026 WorkSphere Global Enterprises Inc. All Rights Reserved.  
This software contains proprietary, trade-secret intellectual property. Unauthorized copying, distribution, or decompilation is strictly prohibited.
