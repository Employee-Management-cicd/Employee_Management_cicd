from app import db

class Employee(db.Model):
    # __tablename__ tells SQLAlchemy what to call this table in the database
    __tablename__ = 'employees'

    # Each variable below becomes one column in the database table
    id         = db.Column(db.Integer, primary_key=True)   # Auto-increment ID
    name       = db.Column(db.String(100), nullable=False)  # Cannot be empty
    email      = db.Column(db.String(120), unique=True, nullable=False)  # Must be unique
    department = db.Column(db.String(100), nullable=False)
    position   = db.Column(db.String(100), nullable=False)
    salary     = db.Column(db.Float, nullable=False)

    # This method controls what you see when you print an Employee object
    def __repr__(self):
        return f'<Employee {self.name}>'