from flask import Flask
from flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from database import db
import models

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

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

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(leave_bp, url_prefix="/leave_requests")
    app.register_blueprint(employee_bp, url_prefix="/employees")
    app.register_blueprint(company_bp, url_prefix="/companies")
    app.register_blueprint(department_bp, url_prefix="/departments")
    app.register_blueprint(dm_bp, url_prefix="/department_managers")
    app.register_blueprint(ca_bp, url_prefix="/company_admins")
    app.register_blueprint(lb_bp, url_prefix="/leave_balances")

    return app

# -----------------------------
# IMPORTANT: GLOBAL APP INSTANCE
# -----------------------------
app = create_app()

@app.route("/")
def home():
    return {"message": "Flask backend connected to PostgreSQL!"}

if __name__ == "__main__":
    app.run(debug=True)
