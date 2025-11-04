from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

db = SQLAlchemy(app)

@app.route('/')
def home():
    return {"message": "Flask backend connected to Render PostgreSQL!"}

if __name__ == '__main__':
    app.run(debug=True)
