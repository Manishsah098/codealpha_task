# CodeAlpha URL Shortener

A simple and efficient URL shortener built with Django and Python.

## 🚀 Features

- **URL Shortening**: Convert long, cumbersome URLs into short, manageable links.
- **Link Management**: View a list of all shortened URLs and their original destinations.
- **Instant Redirection**: Quick and seamless redirection from short links to original URLs.
- **Simple UI**: Easy-to-use interface for shortening and managing links.

## 🛠️ Technology Stack

- **Backend**: [Django](https://www.djangoproject.com/) (Python Framework)
- **Database**: [SQLite](https://www.sqlite.org/) (Default Django development database)
- **Frontend**: HTML, CSS (Django Templates)

## 📋 Prerequisites

- Python 3.x
- Django

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd urlshortener
   ```

2. **Install dependencies** (optional, but recommended to use a virtual environment):
   ```bash
   pip install django
   ```

3. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

The application will be accessible at `http://127.0.0.1:8000/`.

## 📖 Usage Guide

- **Home Page**: Displays a list of all URLs you've shortened.
- **Shorten URL**: Navigate to the "Shorten" page, enter your long URL, and click the button to generate a short link.
- **Redirection**: Access a short link (e.g., `http://127.0.0.1:8000/abc123/`) to be redirected to the original URL.

## 📁 Project Structure

```text
urlshortener/
├── manage.py            # Django management script
├── db.sqlite3           # SQLite database
├── urlshortener/        # Project configuration
│   ├── settings.py      # Django settings
│   └── urls.py          # Main URL routing
└── urlshort/            # Main application app
    ├── models.py        # URL data model
    ├── views.py         # Application logic
    ├── utils.py         # Short URL generation logic
    └── templates/       # HTML templates for the UI
```

## 🤝 Contributing

Contributions are welcome! Pull requests are encouraged for bug fixes, new features, or improvements.

## 📄 License

This project is licensed under the [MIT License](LICENSE).
