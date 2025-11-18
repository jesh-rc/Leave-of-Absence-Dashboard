from flask import Flask, jsonify
from flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, SECRET_KEY
from database import db
import models
from sqlalchemy.exc import SQLAlchemyError

# ---- custom error for invalid input ----
class InvalidUsage(Exception):
    def __init__(self, message, status_code=400, payload=None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.payload = payload or {}

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['SECRET_KEY'] = SECRET_KEY

    db.init_app(app)

    # register blueprints
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
    from utils.validation import ValidationError
    from routes.webservice import ws_bp

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
    

    # -----------------------------
    # ERROR HANDLERS
    # -----------------------------

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

@app.route("/")
def home():
    return {"message": "Flask backend connected to PostgreSQL!"}

if __name__ == "__main__":
    app.run(debug=True)
