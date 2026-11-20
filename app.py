import os
from datetime import datetime, timezone
from flask import Flask, jsonify, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-this-before-deployment")

# --- MongoDB Connect - Idhu dhaan pudhusu ---
client = MongoClient(os.getenv("MONGO_URI"))
db = client["thirisha_portfolio"]
messages_collection = db["messages"]

PROJECTS = [
    {
        "number": "01",
        "name": "CareerPath",
        "type": "Career Guidance Web App",
        "description": "A full-stack career guidance platform with personalized recommendations, learning roadmaps and dynamic visual insights.",
        "stack": ["Python", "Flask", "MySQL", "Bootstrap", "REST APIs", "Chart.js"],
        "highlights": ["8-table relational database", "Parameterized queries and indexing", "Password hashing, session authentication and CSRF protection"],
        "icon": "fa-solid fa-route"
    },
    {
        "number": "02",
        "name": "Fitness Tracking",
        "type": "Fitness Tracking Web Application",
        "description": "A responsive dashboard for fitness logging, intake target calculations and habit metrics, backed by relational data storage.",
        "stack": ["HTML5", "CSS3", "Python", "Flask", "SQLite"],
        "highlights": ["Secure user authentication", "Multi-table routine logs", "Responsive CSS Grid and Flexbox layouts"],
        "icon": "fa-solid fa-heart-pulse"
    }
]

@app.route("/")
def home():
    return render_template("index.html")

@app.get("/api/health")
def health():
    return jsonify({"status": "ok", "service": "Thirisha portfolio API"})

@app.get("/api/projects")
def projects():
    return jsonify(PROJECTS)

@app.post("/api/contact")
def contact():
    data = request.get_json(silent=True) or request.form
    name = str(data.get("name", "")).strip()
    email = str(data.get("email", "")).strip()
    subject = str(data.get("subject", "")).strip()
    message = str(data.get("message", "")).strip()

    if not all([name, email, subject, message]):
        return jsonify({"ok": False, "message": "Please complete every field."}), 400
    if len(name) > 80 or len(email) > 120 or len(subject) > 120 or len(message) > 3000:
        return jsonify({"ok": False, "message": "One or more fields are too long."}), 400
    if "@" not in email or "." not in email.rsplit("@", 1)[-1]:
        return jsonify({"ok": False, "message": "Please enter a valid email address."}), 400

    # --- Ippo MongoDB la save aagum ---
    messages_collection.insert_one({
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
        "created_at": datetime.now(timezone.utc).isoformat()
    })
    return jsonify({"ok": True, "message": "Thanks! Your message has been received."}), 201

@app.errorhandler(404)
def not_found(_error):
    return jsonify({"ok": False, "message": "Not found"}), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=os.environ.get("FLASK_DEBUG") == "1")