from flask import Flask
from flask_sqlalchemy import SQLAlchemy # SQLAlchemy is an ORM (Object Relational Mapper) that allows us to interact with the database using Python classes and objects instead of writing raw SQL queries.
from flask_cors import CORS             # CORS (Cross-Origin Resource Sharing) allows our frontend (REACT) to communicate with our backend (Flask) even if they are hosted on different domains.
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI # Database connection string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS # Disable tracking modifications to save resources

db = SQLAlchemy(app) # Creates the SQLAlchemy object that we will use to interact with the database

@app.route('/')
def home():
    return {"message": "Flask backend connected to Render PostgreSQL!"}

if __name__ == '__main__':
    app.run(debug=True)
