from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from controllers.models import init_db
from controllers.auth_controller import auth_bp
from controllers.admin_controller import admin_bp
from controllers.quiz_controller import quiz_bp
import logging
import os
from datetime import timedelta

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_master.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=60)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize database
init_db(app)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(quiz_bp)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Root route
@app.route('/')
def index():
    return render_template('index.html')

# Create upload directory if it doesn't exist
def create_upload_dir():
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

if __name__ == '__main__':
    with app.app_context():
        try:
            # Create upload directory
            create_upload_dir()
            
            # Initialize database and create admin user
            from controllers.models import db, create_admin_if_not_exists
            
            # Drop all tables and recreate them
            db.drop_all()  # This will delete the existing database
            db.create_all()  # This will create a new database with the correct schema
            
            create_admin_if_not_exists()
            logger.info("Database initialized successfully!")
            
        except Exception as e:
            logger.error(f"Error during initialization: {e}")
            raise e
    
    # Run the application
    app.run(debug=True)
