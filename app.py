import os
import secrets
import sqlite3
from functools import wraps
from pathlib import Path

from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    abort
)
from werkzeug.security import check_password_hash


# ==========================================
# FLASK CONFIGURATION
# ==========================================

app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-secret-key"
)

BASE_DIR = Path(__file__).resolve().parent

DATABASE = Path(
    os.environ.get(
        "DATABASE_PATH",
        str(BASE_DIR / "portfolio.db")
    )
)

ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "")
ADMIN_PASSWORD_HASH = os.environ.get(
    "ADMIN_PASSWORD_HASH",
    ""
)


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_db():
    DATABASE.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row

    return db


# ==========================================
# INITIALIZE DATABASE
# ==========================================

def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                tech TEXT DEFAULT '',
                github_url TEXT DEFAULT '',
                live_url TEXT DEFAULT '',
                image_url TEXT DEFAULT '',
                featured INTEGER DEFAULT 0
            )
        """)


# ==========================================
# ADD DEFAULT PROJECTS
# ==========================================

def seed_projects():

    projects = [
        (
            "Anomalous User Detection",
            "Detects unusual user activity using machine learning and login behavior analysis.",
            "Python, XGBoost, Flask, Scikit-learn",
            "https://github.com/sakshiipandey/anomalous-user-detection",
            "",
            "",
            0
        ),
        (
            "Zepto Support Assistant",
            "An AI support assistant using RAG to retrieve information from support documents.",
            "Python, RAG, LLMs, ChromaDB",
            "https://github.com/sakshiipandey/zepto-support-assistant",
            "",
            "",
            0
        ),
        (
            "Heart Disease Prediction",
            "A machine learning project for predicting heart disease using health-related features.",
            "Python, Pandas, Machine Learning",
            "https://github.com/sakshiipandey",
            "",
            "",
            0
        ),
        (
            "Plant Disease Detection",
            "Detects plant diseases using image processing and deep learning techniques.",
            "Python, Deep Learning, Image Processing",
            "https://github.com/sakshiipandey",
            "",
            "",
            0
        ),
        (
            "AI Text Summarizer",
            "Summarizes text using natural language processing techniques.",
            "Python, NLP, Transformers",
            "https://github.com/sakshiipandey",
            "",
            "",
            0
        ),
        (
            "Snake Game with Reinforcement Learning",
            "A Snake game project exploring reinforcement learning and reward-based learning.",
            "Python, Reinforcement Learning",
            "https://github.com/sakshiipandey",
            "",
            "",
            0
        )
    ]

    with get_db() as db:

        for project in projects:

            title = project[0]

            existing = db.execute(
                "SELECT id FROM projects WHERE title = ?",
                (title,)
            ).fetchone()

            if not existing:

                db.execute("""
                    INSERT INTO projects (
                        title,
                        description,
                        tech,
                        github_url,
                        live_url,
                        image_url,
                        featured
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, project)


# ==========================================
# CSRF PROTECTION
# ==========================================

def csrf_token():

    if "_csrf_token" not in session:
        session["_csrf_token"] = secrets.token_urlsafe(32)

    return session["_csrf_token"]


app.jinja_env.globals["csrf_token"] = csrf_token


def verify_csrf():

    token = request.form.get("_csrf_token", "")
    saved = session.get("_csrf_token", "")

    if (
        not token
        or not saved
        or not secrets.compare_digest(token, saved)
    ):
        abort(
            400,
            description="Page refresh karke dobara try karo."
        )


# ==========================================
# ADMIN AUTHENTICATION
# ==========================================

def admin_required(function):

    @wraps(function)
    def wrapper(*args, **kwargs):

        if not session.get("is_admin"):
            return redirect(url_for("admin_login"))

        return function(*args, **kwargs)

    return wrapper


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    with get_db() as db:

        projects = db.execute("""
            SELECT *
            FROM projects
            ORDER BY featured DESC, id DESC
        """).fetchall()

    return render_template(
        "index.html",
        projects=projects
    )


# ==========================================
# ADMIN LOGIN
# ==========================================

@app.route("/admin", methods=["GET", "POST"])
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    if session.get("is_admin"):
        return redirect(url_for("admin_dashboard"))

    if request.method == "POST":

        verify_csrf()

        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if not ADMIN_USERNAME or not ADMIN_PASSWORD_HASH:

            flash(
                "Admin credentials configure nahi hain.",
                "error"
            )

        elif (
            secrets.compare_digest(
                username,
                ADMIN_USERNAME
            )
            and check_password_hash(
                ADMIN_PASSWORD_HASH,
                password
            )
        ):

            session.clear()
            session["is_admin"] = True
            session["_csrf_token"] = secrets.token_urlsafe(32)

            return redirect(
                url_for("admin_dashboard")
            )

        else:

            flash(
                "Username ya password galat hai.",
                "error"
            )

    return render_template("admin_login.html")


# ==========================================
# ADMIN DASHBOARD
# ==========================================

@app.route("/admin/dashboard")
@admin_required
def admin_dashboard():

    with get_db() as db:

        projects = db.execute("""
            SELECT *
            FROM projects
            ORDER BY id DESC
        """).fetchall()

    return render_template(
        "admin_dashboard.html",
        projects=projects
    )


# ==========================================
# ADD / UPDATE PROJECT
# ==========================================

@app.route("/admin/project/save", methods=["POST"])
@admin_required
def save_project():

    verify_csrf()

    project_id = request.form.get(
        "project_id",
        ""
    ).strip()

    title = request.form.get(
        "title",
        ""
    ).strip()

    description = request.form.get(
        "description",
        ""
    ).strip()

    tech = request.form.get(
        "tech",
        ""
    ).strip()

    github_url = request.form.get(
        "github_url",
        ""
    ).strip()

    live_url = request.form.get(
        "live_url",
        ""
    ).strip()

    image_url = request.form.get(
        "image_url",
        ""
    ).strip()

    featured = (
        1
        if request.form.get("featured") == "1"
        else 0
    )

    if not title or not description:

        flash(
            "Project name aur description required hain.",
            "error"
        )

        return redirect(
            url_for("admin_dashboard")
        )

    # Validate URLs
    for label, value in [
        ("GitHub", github_url),
        ("Live Demo", live_url),
        ("Image", image_url)
    ]:

        if value and not value.startswith(
            ("https://", "http://")
        ):

            flash(
                f"{label} link valid URL hona chahiye.",
                "error"
            )

            return redirect(
                url_for("admin_dashboard")
            )

    with get_db() as db:

        if project_id:

            db.execute("""
                UPDATE projects
                SET
                    title = ?,
                    description = ?,
                    tech = ?,
                    github_url = ?,
                    live_url = ?,
                    image_url = ?,
                    featured = ?
                WHERE id = ?
            """, (
                title,
                description,
                tech,
                github_url,
                live_url,
                image_url,
                featured,
                project_id
            ))

            flash(
                "Project successfully update ho gaya!",
                "success"
            )

        else:

            db.execute("""
                INSERT INTO projects (
                    title,
                    description,
                    tech,
                    github_url,
                    live_url,
                    image_url,
                    featured
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                title,
                description,
                tech,
                github_url,
                live_url,
                image_url,
                featured
            ))

            flash(
                "New project add ho gaya!",
                "success"
            )

    return redirect(
        url_for("admin_dashboard")
    )


# ==========================================
# DELETE PROJECT
# ==========================================

@app.route(
    "/admin/project/<int:project_id>/delete",
    methods=["POST"]
)
@admin_required
def delete_project(project_id):

    verify_csrf()

    with get_db() as db:

        db.execute(
            "DELETE FROM projects WHERE id = ?",
            (project_id,)
        )

    flash(
        "Project delete ho gaya.",
        "success"
    )

    return redirect(
        url_for("admin_dashboard")
    )


# ==========================================
# ADMIN LOGOUT
# ==========================================

@app.route("/admin/logout", methods=["POST"])
@admin_required
def admin_logout():

    verify_csrf()

    session.clear()

    return redirect(
        url_for("home")
    )


# ==========================================
# ERROR HANDLER
# ==========================================

@app.errorhandler(400)
def bad_request(error):

    return str(error.description), 400


# ==========================================
# START APPLICATION
# ==========================================

init_db()
seed_projects()


if __name__ == "__main__":

    app.run(debug=False)