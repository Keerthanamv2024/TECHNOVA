# TechNova – IT Company Profile Website

A complete, modern, and responsive IT company profile web application built for college Web Programming coursework using **HTML5, CSS3, Vanilla JavaScript, Python Flask, and SQLite**.

---

## 📌 Project Abstract

**TechNova Solutions** is a responsive corporate web portal for an IT consulting company. The platform showcases core technology services, company milestones, leadership vision, and featured client case studies. Visitors can submit inquiries through a validated interactive contact form. The backend is built with Python Flask and persists submissions into a local SQLite database (`technova.db`) using parameterized SQL queries. An authenticated, session-protected Administrator Dashboard allows company administrators to review, monitor, and manage client inquiries securely, with automatic Jinja2 escaping to prevent Cross-Site Scripting (XSS).

---

## 🛠️ Technology Stack

| Layer | Technology | Details |
| :--- | :--- | :--- |
| **Frontend** | HTML5, CSS3, Vanilla JS | Modern responsive layout, CSS grid/flexbox, custom color theme (Navy Blue, White, Purple Accents), mobile hamburger menu, live validation, and AJAX |
| **Backend** | Python Flask (3.x) | Lightweight WSGI web framework, session cookies, route handlers, server-side data validation |
| **Database** | SQLite3 (`technova.db`) | Embedded relational database, auto-creating table with parameterized SQL queries |
| **Security** | Jinja2 & Session Auth | SQL Injection prevention via parameterized queries, XSS protection via HTML escaping, decorator-based route authentication |

---

## 📁 Directory Structure

```text
TECHNOVA -IT PROFILE/
│
├── app.py                      # Flask backend application, database helper, and routing logic
├── requirements.txt            # Python dependencies (Flask)
├── technova.db                 # SQLite database file (created automatically on startup)
├── README.md                   # Complete documentation and viva guide
├── .gitignore                  # Git exclusions for environments and database cache
│
├── templates/                  # Jinja2 HTML Templates
│   ├── index.html              # Main single-page IT company website
│   ├── admin_login.html        # Secure administrator login page
│   └── admin.html              # Protected administrator dashboard
│
└── static/                     # Static assets
    ├── css/
    │   └── style.css           # Custom modern responsive styling
    └── js/
        └── script.js           # Client-side validation, mobile menu, and AJAX handling
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
Ensure Python 3.8+ is installed on your machine. You can verify this in PowerShell or Terminal:
```powershell
python --version
```

### 2. (Optional but Recommended) Create a Virtual Environment
```powershell
# In the project directory:
python -m venv venv

# Activate on Windows:
venv\Scripts\activate

# Activate on macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```powershell
pip install -r requirements.txt
```

### 4. Run the Flask Server
```powershell
python app.py
```
By default, the server starts locally at:
👉 **`http://127.0.0.1:5000`**

### 5. Open in Your Web Browser
Open your favorite web browser (Chrome, Edge, Firefox) and navigate to:
- **Public Profile Website:** `http://127.0.0.1:5000/`
- **Admin Login Portal:** `http://127.0.0.1:5000/admin/login`

---

## 🔐 Admin Portal Credentials & Configuration

For academic evaluation and demonstration, default credentials are preconfigured safely:

- **Username:** `admin`
- **Password:** `admin123`

### Production / Custom Environment Variables:
You can set custom credentials in your environment without changing code:

**Windows PowerShell:**
```powershell
$env:ADMIN_USERNAME="supervisor"
$env:ADMIN_PASSWORD="MySecurePassword2026!"
python app.py
```

**macOS / Linux / Bash:**
```bash
export ADMIN_USERNAME="supervisor"
export ADMIN_PASSWORD="MySecurePassword2026!"
python app.py
```

---

## 🌐 How the Components Connect

1. **User Action (Frontend):**
   - The user visits `http://127.0.0.1:5000/` and browses company services, portfolio case studies, and mission statements.
   - When filling out the contact form, `static/js/script.js` performs client-side validation to provide immediate feedback if any field is missing or invalid.
2. **Form Submission & API Request:**
   - The form sends a `POST` request to `/contact`.
   - `script.js` uses `fetch()` with JSON payload for instant feedback without full-page reload, while standard HTML form POST is also fully supported as a fallback.
3. **Backend Processing (`app.py`):**
   - Flask intercepts the request, runs server-side validation (ensuring inputs cannot be bypassed by disabling JavaScript), and sanitizes strings.
4. **Database Persistence (`technova.db`):**
   - Flask executes a parameterized query:
     `INSERT INTO enquiries (name, email, subject, message) VALUES (?, ?, ?, ?)`
   - Using `?` placeholders prevents SQL injection vulnerabilities.
5. **Admin Access:**
   - Administrators navigate to `/admin/login`, submit their credentials, and Flask generates a signed session cookie.
   - The `@login_required` decorator ensures unauthenticated visitors are redirected to login.
   - `admin.html` iterates through enquiries from SQLite and displays them with automatic HTML escaping.

---

## 🎓 Viva Voce Questions & Answers

### Q1. What is Flask and why was it chosen for this project instead of Django or Node.js?
**Answer:** Flask is a lightweight Python WSGI micro-framework. Unlike larger frameworks like Django, Flask does not enforce rigid boilerplate or heavy object-relational mappers, making it ideal for learning fundamental web architecture. It provides routing, request handling, templating via Jinja2, and session management while allowing direct, transparent control over SQLite queries.

### Q2. How is SQL Injection prevented when storing contact submissions in SQLite?
**Answer:** SQL Injection is prevented by using **parameterized queries** (prepared statements) with `?` placeholders:
```python
conn.execute("INSERT INTO enquiries (name, email, subject, message) VALUES (?, ?, ?, ?)", (name, email, subject, message))
```
The database driver separates the SQL command from the user-supplied data, ensuring untrusted input is treated strictly as literal values rather than executable SQL commands.

### Q3. Why is both client-side and server-side validation implemented?
**Answer:** 
- **Client-side validation** (in `script.js`) provides immediate feedback to the user, enhancing user experience and reducing unnecessary network traffic.
- **Server-side validation** (in `app.py`) provides critical security, because client-side checks can be bypassed by disabling JavaScript or sending direct HTTP POST requests via tools like cURL or Postman. Server validation ensures data integrity before database insertion.

### Q4. How does Jinja2 prevent Stored Cross-Site Scripting (XSS) in the admin dashboard?
**Answer:** By default, Jinja2 automatically escapes all dynamic expressions rendered with `{{ ... }}`. If a malicious user submits HTML or JavaScript tags (e.g. `<script>alert(1)</script>`) into the contact form, Jinja2 encodes special characters into safe HTML entities (e.g., `&lt;script&gt;`), rendering them harmlessly as plain text on the admin screen rather than executing them in the browser.

### Q5. What is the role of the `@login_required` decorator in Flask?
**Answer:** A Python decorator wraps an existing route function. The `@login_required` decorator checks whether `session.get('admin_logged_in')` evaluates to true before allowing execution of the admin view function. If false, it flashes a warning message and redirects the user to `/admin/login`, protecting sensitive administrative pages from unauthorized direct URL access.
