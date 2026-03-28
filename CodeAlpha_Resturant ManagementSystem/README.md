# Restaurant Management System 

Manish Resturant is a sophisticated, full-stack digital platform designed to bridge the gap between customer ordering convenience and backend administrative efficiency. Built with a premium glassmorphism interface and a robust Django REST backend, it streamlines restaurant operations from the dining table to the kitchen.

## 📖 Project Specification

The **Restaurant Management System (RMS)** was built to solve the challenges of traditional restaurant operations. For small to medium-sized teams, managing orders, inventory, and sales data with manual systems leads to errors and bottlenecks. RMS Pro provides a unified solution:

*   **Phase 1: Precision Ordering**: Customers browse a high-performance digital menu and place table-specific orders, eliminating handwritten errors.
*   **Phase 2: Administrative Control**: Real-time sales analytics, daily revenue tracking, and automated inventory threshold alerts help managers work smarter.
*   **Phase 3: Future-Ready Design**: The architecture is built for scalability, supporting future role-based access control (RBAC), multi-branch deployment, and AI-driven forecasting.

## ✨ Core Features

### 🛒 Customer Experience
*   **Interactive Menu**: A stunning glassmorphism grid with item ratings, diet symbols (Veg/Non-Veg), and cuisine tags.
*   **Table-Locked Ordering**: Prevents orders until a table is selected, ensuring operational accuracy.
*   **Real-time Cart**: A reactive ordering system with quantity controls and automatic tax/total calculation.
*   **Menu Search**: Instant filtering of dishes by name or cuisine type.

### 🛡️ Administrative Panel (Live Orders Board)
*   **Order Verification**: Admins can view pending orders and "Verify & Send to Waiter" with one click.
*   **Status Management**: Track orders through `Pending`, `Preparing`, and `Completed` stages.
*   **Inventory Alerts**: Dashboard notifications for items falling below critical stock levels.
*   **Daily Reports**: Instant visibility into total sales and order counts for the day.

## 🛠️ Technology Stack

### Backend
*   **Python 3.10+ / Django**: Core business logic and server.
*   **Django REST Framework (DRF)**: High-performance API architecture.
*   **SQLite**: Reliable relational data storage.
*   **CORS Headers**: Secure cross-origin resource sharing.

### Frontend
*   **HTML5 & CSS3**: Custom glassmorphism design system.
*   **Vanilla JavaScript (ES6+)**: Reactive DOM manipulation and `fetch` API for asynchronous communication.
*   **FontAwesome 6**: Premium iconography.
*   **Google Fonts**: Inter & Outfit typography.

## 🚀 Setup and Installation

### 1-Click Startup (Windows)
Double-click the `run.bat` file in the root directory. This will automatically:
1. Start the Django backend on `http://127.0.0.1:8000/`.
2. Start the Frontend server on `http://localhost:3000/`.

### Manual Startup
**1. Backend:**
```bash
cd backend
venv\Scripts\activate
python manage.py runserver
```
**2. Frontend:**
```bash
cd frontend
python -m http.server 3000
```

## 📡 API Endpoints


| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/menu/` | Retrieve all available menu items |
| `POST` | `/api/orders/` | Submit a new table order |
| `GET` | `/api/orders/all/` | Fetch all orders for administration |
| `PATCH` | `/api/orders/<id>/status/` | Update order state (Preparing/Completed) |
| `GET` | `/api/inventory/alerts/` | Fetch low-stock inventory items |
| `GET` | `/api/reports/daily-sales/` | Daily sales and volume metrics |

## 📁 Project Structure
```text
/
├── backend/                   # Django REST Framework
│   ├── restaurant/            # Core App (Models, Views, Serializers)
│   ├── rms_project/           # Project Configuration
│   └── venv/                  # Virtual Environment
├── frontend/                  # Static Application
│   ├── index.html             # Main Interface
│   ├── style.css              # Premium Stylesheet
│   └── app.js                 # Reative Application Logic
└── run.bat                    # Automation Script
```

## 🤝 Developer Details
*   **Developer Name**: Manish Kumar Sah
*   **GitHub ID**: [Manishsah098](https://github.com/Manishsah098)
*   **Email**: [manishkumarsah.cse2025@citchennai.net](mailto:manishkumarsah.cse2025@citchennai.net)
*   **LinkedIn**: [Manish Kumar Sah](https://www.linkedin.com/in/manish-kumar-sah-2b2a8a2a1/)
#
