from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Employee

# A Blueprint is a way to organize routes — think of it as a group of related pages
main = Blueprint('main', __name__)


# ── HOME PAGE — Show all employees ──────────────────────────────────────────
@main.route('/')
def index():
    # Get all employees from the database, ordered by name
    employees = Employee.query.order_by(Employee.name).all()
    return render_template('index.html', employees=employees)


# ── SEARCH ───────────────────────────────────────────────────────────────────
@main.route('/search')
def search():
    # Get the search term from the URL — e.g. /search?query=John
    query = request.args.get('query', '')
    if query:
        # Search for employees whose name OR department contains the query
        employees = Employee.query.filter(
            Employee.name.ilike(f'%{query}%') |
            Employee.department.ilike(f'%{query}%')
        ).all()
    else:
        employees = Employee.query.all()
    return render_template('index.html', employees=employees, search_query=query)


# ── ADD EMPLOYEE ─────────────────────────────────────────────────────────────
@main.route('/add', methods=['GET', 'POST'])
def add_employee():
    # GET means the user is visiting the page to see the form
    # POST means the user submitted the form with data
    if request.method == 'POST':
        # Read the data the user typed into the form
        name       = request.form['name']
        email      = request.form['email']
        department = request.form['department']
        position   = request.form['position']
        salary     = request.form['salary']

        # Check if an employee with this email already exists
        existing = Employee.query.filter_by(email=email).first()
        if existing:
            flash('An employee with this email already exists.', 'danger')
            return redirect(url_for('main.add_employee'))

        # Create a new Employee object and save it to the database
        new_employee = Employee(
            name=name,
            email=email,
            department=department,
            position=position,
            salary=float(salary)
        )
        db.session.add(new_employee)
        db.session.commit()
        flash(f'Employee {name} added successfully!', 'success')
        return redirect(url_for('main.index'))

    # If GET, just show the empty form
    return render_template('add_employee.html')


# ── EDIT EMPLOYEE ─────────────────────────────────────────────────────────────
@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    # Find the employee by ID — if not found, return 404 error
    employee = Employee.query.get_or_404(id)

    if request.method == 'POST':
        # Update each field with the new values from the form
        employee.name       = request.form['name']
        employee.email      = request.form['email']
        employee.department = request.form['department']
        employee.position   = request.form['position']
        employee.salary     = float(request.form['salary'])
        db.session.commit()
        flash(f'Employee {employee.name} updated successfully!', 'success')
        return redirect(url_for('main.index'))

    # If GET, show the form pre-filled with current employee data
    return render_template('edit_employee.html', employee=employee)


# ── DELETE EMPLOYEE ───────────────────────────────────────────────────────────
@main.route('/delete/<int:id>', methods=['POST'])
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    name = employee.name
    db.session.delete(employee)
    db.session.commit()
    flash(f'Employee {name} deleted.', 'info')
    return redirect(url_for('main.index'))