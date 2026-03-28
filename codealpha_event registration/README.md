# EventHub -  Event Registration System

EventHub is a modern, full-stack event management platform built with Django and React. It features a stunning glassmorphism UI, secure token-based authentication, and a seamless registration experience.

![UI Preview](C:/Users/Lenovo/.gemini/antigravity/brain/ce6c73fa-2e56-4c49-ba92-c130d7a70cd8/new_ui_verification_1774716374403.png)

## 🚀 Features

-   **Premium UI/UX**: Modern glassmorphism design with animated mesh-gradient backgrounds and smooth Framer Motion transitions.
-   **Full Authentication**: Secure Signup and Login system using Django Token Authentication.
-   **Event Discovery**: Explore a curated list of 14+ high-quality events ranging from tech conferences to music festivals.
-   **One-Click Registration**: Register for events instantly with real-time feedback and duplicate check.
-   **User Profile**: Dedicated profile page to view account details and track all your registered events.
-   **Responsive Design**: Optimized for both desktop and mobile viewing.

## 🛠️ Tech Stack

-   **Backend**: Django, Django REST Framework (DRF)
-   **Frontend**: React, Vite, Framer Motion, Lucide React, Axios
-   **Database**: SQLite (Development)
-   **Authentication**: Token-based Auth (`rest_framework.authtoken`)

## 📋 Prerequisites

-   Python 3.8+
-   Node.js 16+
-   npm or yarn

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd codealpha_event-registration
```

### 2. Backend Setup (Django)
```bash
# Install dependencies
pip install django djangorestframework django-cors-headers

# Apply migrations
python manage.py migrate

# Seed initial data (Includes 14+ events and admin user)
python seed_data.py

# Start the backend server
python manage.py runserver 8000
```
*Backend API will be running at `http://localhost:8000/api/`*

### 3. Frontend Setup (React)
```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev -- --port 3000
```
*Frontend will be running at `http://localhost:3000/`*

## 🧪 Admin Credentials
- **Username**: `admin`
- **Password**: `admin123`

## 📄 License
This project is part of the CodeAlpha internship task.

---
Built with ❤️ by Antigravity AI
