# Thirisha S — Developer Portfolio

A responsive, technical portfolio built with HTML, CSS, JavaScript and a Python Flask backend.

## Features
- Responsive dark developer UI with animated sections and mobile navigation
- Technology icons using Devicon and Font Awesome CDN
- Project, experience, education and technical skill sections
- Contact form connected to Flask API and SQLite persistence
- API health endpoint (`/api/health`) and project endpoint (`/api/projects`)
- Basic server-side validation and parameterized SQL insert

## Run locally (Windows PowerShell)

```powershell
cd thirisha_portfolio
py -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000

The SQLite database `portfolio.db` is created automatically when the app starts. Contact form submissions are saved in the `messages` table.

## API endpoints
- `GET /api/health` — backend health status
- `GET /api/projects` — project data in JSON
- `POST /api/contact` — accepts JSON: `name`, `email`, `subject`, `message`

## Before publishing
1. Change `SECRET_KEY` to a long random secret in your hosting environment.
2. Set `FLASK_DEBUG` off (the default).
3. For production, use a persistent database. SQLite is suitable for local testing/small demos; use managed MySQL/PostgreSQL for a deployed portfolio with persistent storage.
4. Deploy with a WSGI server such as Gunicorn (Linux hosting) or the platform's recommended start command.
5. External icon/font CDNs require an internet connection.

## Personal details to verify
The portfolio uses details from the uploaded resumes. Confirm the displayed phone, email, education figures and LinkedIn/GitHub links before publishing.
