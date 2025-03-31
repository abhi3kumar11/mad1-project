from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os

db = SQLAlchemy()

def init_db(app):
    db.init_app(app)

def create_admin_if_not_exists():
    try:
        admin = User.query.filter_by(email='admin@gmail.com').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@gmail.com',
                full_name='Administrator',
                qualification='Admin',
                dob=datetime.strptime('2000-01-01', '%Y-%m-%d'),
                is_admin=True
            )
            admin.set_password('admin_password')
            db.session.add(admin)
            db.session.commit()
            print('Admin user created successfully!')
    except Exception as e:
        print(f"Error creating admin: {e}")
        db.session.rollback()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(100), nullable=True)
    qualification = db.Column(db.String(100), nullable=True)
    dob = db.Column(db.Date, nullable=True)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    quiz_attempts = db.relationship('QuizAttempt', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    chapters = db.relationship('Chapter', backref='subject', lazy=True, cascade='all, delete-orphan')

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    quizzes = db.relationship('Quiz', backref='chapter', lazy=True, cascade='all, delete-orphan')

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'), nullable=False)
    time_limit = db.Column(db.Integer, nullable=False)  # Time limit in minutes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    questions = db.relationship('Question', backref='quiz', lazy=True, cascade='all, delete-orphan')
    attempts = db.relationship('QuizAttempt', backref='quiz', lazy=True)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # A, B, C, or D
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class QuizAttempt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    attempt_date = db.Column(db.DateTime, default=datetime.utcnow)
