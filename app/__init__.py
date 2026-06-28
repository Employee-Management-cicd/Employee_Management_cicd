from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create the database object — this will be imported by models.py and routes.py
db = SQLAlchemy()

def create_app():
    # Create the Flask application instance
    app = Flask(__name__)

    # Configuration — tell Flask where the database file will be stored
    # The database file employee.db will be created in the project root folder
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employee.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'devops-project-secret-key'

    # Connect the database object to this app
    db.init_app(app)

    # Import and register the routes
    from app.routes import main
    app.register_blueprint(main)

    # Create all database tables if they don't already exist
    with app.app_context():
        db.create_all()

    return app