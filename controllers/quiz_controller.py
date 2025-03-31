from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from controllers.models import db, User, Quiz, Question, QuizAttempt, Subject, Chapter
from functools import wraps
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__, url_prefix='/quiz')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            flash('Please log in first.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@quiz_bp.route('/dashboard')
@login_required
def user_dashboard():
    user_id = session.get('user_id')
    subjects = Subject.query.all()
    recent_attempts = QuizAttempt.query.filter_by(user_id=user_id).order_by(QuizAttempt.attempt_date.desc()).limit(5).all()
    return render_template('quiz/user_dashboard.html', subjects=subjects, recent_attempts=recent_attempts)

@quiz_bp.route('/scores')
@login_required
def scores():
    user_id = session.get('user_id')
    attempts = QuizAttempt.query.filter_by(user_id=user_id).order_by(QuizAttempt.attempt_date.desc()).all()
    return render_template('quiz/scores.html', attempts=attempts)

@quiz_bp.route('/quiz/<int:quiz_id>')
@login_required
def view_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    user_id = session.get('user_id')
    previous_attempts = QuizAttempt.query.filter_by(user_id=user_id, quiz_id=quiz_id).order_by(QuizAttempt.attempt_date.desc()).all()
    return render_template('quiz/view_quiz.html', quiz=quiz, questions=questions, previous_attempts=previous_attempts)

@quiz_bp.route('/quiz/<int:quiz_id>/start', methods=['GET', 'POST'])
@login_required
def start_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = Question.query.filter_by(quiz_id=quiz_id).all()
    
    if request.method == 'POST':
        score = 0
        for question in questions:
            answer = request.form.get(f'answer_{question.id}')
            if answer and answer.upper() == question.correct_answer:
                score += 1
        
        # Record the attempt
        user_id = session.get('user_id')
        attempt = QuizAttempt(
            user_id=user_id,
            quiz_id=quiz_id,
            score=score,
            total_questions=len(questions),
            attempt_date=datetime.utcnow()
        )
        db.session.add(attempt)
        db.session.commit()
        
        flash(f'Quiz completed! Your score: {score}/{len(questions)}', 'success')
        return redirect(url_for('quiz.scores'))
    
    return render_template('quiz/start_quiz.html', quiz=quiz, questions=questions)

@quiz_bp.route('/summary')
@login_required
def user_summary_chart():
    user_id = session.get('user_id')
    attempts = QuizAttempt.query.filter_by(user_id=user_id).order_by(QuizAttempt.attempt_date).all()
    
    total_attempts = len(attempts)
    if total_attempts > 0:
        scores = [attempt.score / attempt.total_questions * 100 for attempt in attempts]
        average_score = sum(scores) / len(scores)
        highest_score = max(scores)
        lowest_score = min(scores)
        
        # Get data for chart
        dates = [attempt.attempt_date.strftime('%Y-%m-%d') for attempt in attempts[-10:]]
        recent_scores = [attempt.score / attempt.total_questions * 100 for attempt in attempts[-10:]]
    else:
        average_score = highest_score = lowest_score = 0
        dates = []
        recent_scores = []
    
    return render_template('quiz/user_summary_chart.html', 
                          total_attempts=total_attempts,
                          average_score=round(average_score, 2) if total_attempts > 0 else 0,
                          highest_score=round(highest_score, 2) if total_attempts > 0 else 0,
                          lowest_score=round(lowest_score, 2) if total_attempts > 0 else 0,
                          dates=dates,
                          scores=recent_scores)
