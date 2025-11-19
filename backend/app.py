import os
from flask import Flask, jsonify, send_from_directory
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from database import db
import models  # ensure models are imported so SQLAlchemy knows them
from sqlalchemy.exc import SQLAlchemyError

# ---------------------------------------------------
# Paths to the built React app
# ---------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_BUILD = os.path.join(BASE_DIR, "..", "frontend", "build")


# ---- custom error for invalid input ----
class InvalidUsage(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}


def create_app():
    # Tell Flask where the built React app lives
    app = Flask(
        __name__,
        static_folder=FRONTEND_BUILD,
        static_url_path="/"
    )

    # ---------------------------------------------------
    # Flask configuration
    # ---------------------------------------------------
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = SECRET_KEY

    db.init_app(app)

    # ---------------------------------------------------
    # Register blueprints (your API routes)
    # ---------------------------------------------------
    from routes.auth import auth_bp
    from routes.leave_requests import leave_bp
    from routes.employee import employee_bp
    from routes.company import company_bp
    from routes.department import department_bp
    from routes.department_manager import dm_bp
    from routes.company_admin import ca_bp
    from routes.leave_balance import lb_bp
    from routes.views import views_bp
    from routes.export_routes import export_bp
    from routes.webservice import ws_bp
    from utils.validation import ValidationError

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(leave_bp, url_prefix="/leave_requests")
    app.register_blueprint(employee_bp, url_prefix="/employees")
    app.register_blueprint(company_bp, url_prefix="/companies")
    app.register_blueprint(department_bp, url_prefix="/departments")
    app.register_blueprint(dm_bp, url_prefix="/department_managers")
    app.register_blueprint(ca_bp, url_prefix="/company_admins")
    app.register_blueprint(lb_bp, url_prefix="/leave_balances")
    app.register_blueprint(views_bp, url_prefix="/views")
    app.register_blueprint(export_bp, url_prefix="/export")
    app.register_blueprint(ws_bp, url_prefix="/webservice")

    # ---------------------------------------------------
    # Error handlers
    # ---------------------------------------------------

    @app.errorhandler(404)
    def handle_404(e):
        return jsonify({
            "error": "Not Found",
            "message": "The requested resource was not found."
        }), 404

    @app.errorhandler(500)
    def handle_500(e):
        return jsonify({
            "error": "Server Error",
            "message": "An unexpected error occurred on the server."
        }), 500

    @app.errorhandler(SQLAlchemyError)
    def handle_db_error(e):
        db.session.rollback()
        return jsonify({
            "error": "Database Error",
            "message": "A database error occurred.",
            "details": str(e.__cause__ or e)
        }), 500

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(err):
        resp = {
            "error": "Invalid Input",
            "message": err.message
        }
        resp.update(err.payload)
        return jsonify(resp), err.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        resp = {
            "error": "Invalid Input",
            "message": err.message,
            "details": err.details
        }
        return jsonify(resp), 400

    return app


# -----------------------------
# GLOBAL APP INSTANCE
# -----------------------------
app = create_app()


# ---------------------------------------------------
# Serve the built React app
# ---------------------------------------------------
@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_react(path):
    """
    Serve the React single-page app from the build folder.
    If the requested file exists (e.g. /static/js/main.js),
    serve that file. Otherwise, serve index.html and let
    React Router handle the route (/login, /admin, etc.).
    """
    # If the path points to an actual file in the build dir, serve it
    full_path = os.path.join(FRONTEND_BUILD, path)
    if path != "" and os.path.exists(full_path):
        return send_from_directory(FRONTEND_BUILD, path)

    # Otherwise, always serve index.html (SPA entry point)
    return send_from_directory(FRONTEND_BUILD, "index.html")


# Optional: simple health-check endpoint if you want JSON
@app.route("/api/health")
def health():
    return {"status": "ok", "message": "Flask + React are running."}


if __name__ == "__main__":
    app.run(debug=True)
