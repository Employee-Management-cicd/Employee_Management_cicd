from app import create_app

# Create the application using the factory function in app/__init__.py
app = create_app()

if __name__ == '__main__':
    # debug=True means Flask will show detailed error messages
    # and automatically restart when you save changes
    app.run(debug=True, host='0.0.0.0', port=5000)