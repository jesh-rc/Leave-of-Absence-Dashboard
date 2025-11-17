from flask import Flask
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy is an ORM (Object Relational Mapper) that allows us to interact with the database using Python classes and objects instead of writing raw SQL queries.
from flask_cors import CORS             # CORS (Cross-Origin Resource Sharing) allows our frontend (REACT) to communicate with our backend (Flask) even if they are hosted on different domains.
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from routes.auth import auth_bp
from routes.leave_requests import leave_bp
from routes.employee import employee_bp
from routes.company import company_bp
from routes.department import department_bp
from routes.department_manager import dm_bp
from routes.company_admin import ca_bp
from routes.leave_balance import lb_bp



app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI # Database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS # Disable tracking modifications to save resources

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(leave_bp, url_prefix='/leave_requests')
app.register_blueprint(employee_bp, url_prefix='/employees')
app.register_blueprint(company_bp, url_prefix='/companies')
app.register_blueprint(department_bp, url_prefix='/departments')
app.register_blueprint(dm_bp, url_prefix='/department_managers')
app.register_blueprint(ca_bp, url_prefix='/company_admins')
app.register_blueprint(lb_bp, url_prefix='/leave_balances')


db = SQLAlchemy(app) # Creates the SQLAlchemy object that we will use to interact with the database

@app.route('/') # Whenever a user visits the root URL, this function will be called
def home():
    return {"message": "Flask backend connected to PostgreSQL!"}

if __name__ == '__main__': # If this script is run directly, start the Flask development server. If it is imported as a module, do not start the server.
    app.run(debug=True)
