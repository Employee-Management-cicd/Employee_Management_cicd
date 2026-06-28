import pytest
from app import create_app, db
from app.models import Employee


@pytest.fixture
def app():
    """
    This fixture creates a fresh test app with an in-memory database.
    In-memory means the test database exists only during the test
    and is destroyed after — your real employee.db is never touched.
    """
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    """This fixture gives us a test client to simulate HTTP requests."""
    return app.test_client()


@pytest.fixture
def sample_employee(app):
    """Creates one employee in the test database for tests that need existing data."""
    with app.app_context():
        emp = Employee(
            name='Test Employee',
            email='test@example.com',
            department='Engineering',
            position='Developer',
            salary=50000.0
        )
        db.session.add(emp)
        db.session.commit()
        return emp.id  # Return the ID so tests can reference this employee


# ── TEST 1: Home page loads ───────────────────────────────────────────────────
def test_home_page_loads(client):
    """The home page should return HTTP 200 (success)."""
    response = client.get('/')
    assert response.status_code == 200


# ── TEST 2: Add employee page loads ──────────────────────────────────────────
def test_add_employee_page_loads(client):
    """The add employee form page should load successfully."""
    response = client.get('/add')
    assert response.status_code == 200


# ── TEST 3: Adding an employee works ─────────────────────────────────────────
def test_add_employee(client, app):
    """Submitting the add form with valid data should create a new employee."""
    response = client.post('/add', data={
        'name': 'Sneha Sharma',
        'email': 'sneha@example.com',
        'department': 'DevOps',
        'position': 'Pipeline Engineer',
        'salary': '60000'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Verify the employee was actually saved in the database
    with app.app_context():
        emp = Employee.query.filter_by(email='sneha@example.com').first()
        assert emp is not None
        assert emp.name == 'Sneha Sharma'
        assert emp.department == 'DevOps'


# ── TEST 4: Employee appears on home page ────────────────────────────────────
def test_employee_appears_in_list(client, app):
    """After adding, the employee's name should appear on the home page."""
    with app.app_context():
        emp = Employee(
            name='Raj Kumar',
            email='raj@example.com',
            department='HR',
            position='Manager',
            salary=70000.0
        )
        db.session.add(emp)
        db.session.commit()

    response = client.get('/')
    assert b'Raj Kumar' in response.data


# ── TEST 5: Edit employee works ───────────────────────────────────────────────
def test_edit_employee(client, app, sample_employee):
    """Editing an employee should update their data in the database."""
    response = client.post(f'/edit/{sample_employee}', data={
        'name': 'Updated Name',
        'email': 'test@example.com',
        'department': 'Updated Department',
        'position': 'Senior Developer',
        'salary': '75000'
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        emp = Employee.query.get(sample_employee)
        assert emp.name == 'Updated Name'
        assert emp.salary == 75000.0


# ── TEST 6: Delete employee works ────────────────────────────────────────────
def test_delete_employee(client, app, sample_employee):
    """Deleting an employee should remove them from the database."""
    response = client.post(f'/delete/{sample_employee}', follow_redirects=True)
    assert response.status_code == 200

    with app.app_context():
        emp = Employee.query.get(sample_employee)
        assert emp is None  # Employee should no longer exist


# ── TEST 7: Search works ──────────────────────────────────────────────────────
def test_search_employee(client, app):
    """Searching by name should return matching employees."""
    with app.app_context():
        emp = Employee(
            name='Arjun Patel',
            email='arjun@example.com',
            department='Finance',
            position='Analyst',
            salary=45000.0
        )
        db.session.add(emp)
        db.session.commit()

    response = client.get('/search?query=Arjun')
    assert b'Arjun Patel' in response.data


# ── TEST 8: Duplicate email is rejected ──────────────────────────────────────
def test_duplicate_email_rejected(client, app, sample_employee):
    """Adding an employee with an email that already exists should fail."""
    response = client.post('/add', data={
        'name': 'Another Person',
        'email': 'test@example.com',  # This email is already used by sample_employee
        'department': 'Sales',
        'position': 'Rep',
        'salary': '30000'
    }, follow_redirects=True)

    assert response.status_code == 200

    # Only one employee with this email should exist
    with app.app_context():
        count = Employee.query.filter_by(email='test@example.com').count()
        assert count == 1