from flask import Blueprint, render_template, redirect, url_for, flash, session, request
from .models import db, User, Subject, Chapter, Quiz, Question
from .forms import SubjectForm, ChapterForm, QuizForm, QuestionForm
from functools import wraps

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id') or not session.get('is_admin'):
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@admin_required
def admin_dashboard():
    subjects = Subject.query.all()
    chapters = Chapter.query.all()
    quizzes = Quiz.query.all()
    users = User.query.filter_by(is_admin=False).all()
    return render_template('admin/admin_dashboard.html', 
                          subjects=subjects, 
                          chapters=chapters, 
                          quizzes=quizzes, 
                          users=users)

@admin_bp.route('/new-subject', methods=['GET', 'POST'])
@admin_required
def new_subject():
    form = SubjectForm()
    if form.validate_on_submit():
        subject = Subject(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(subject)
        db.session.commit()
        flash('Subject created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/new_subject.html', form=form)

@admin_bp.route('/edit-subject/<int:subject_id>', methods=['GET', 'POST'])
@admin_required
def edit_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    form = SubjectForm(obj=subject)
    if form.validate_on_submit():
        subject.name = form.name.data
        subject.description = form.description.data
        db.session.commit()
        flash('Subject updated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/edit_subject.html', form=form, subject=subject)

@admin_bp.route('/delete-subject/<int:subject_id>')
@admin_required
def delete_subject(subject_id):
    subject = Subject.query.get_or_404(subject_id)
    db.session.delete(subject)
    db.session.commit()
    flash('Subject deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/new-chapter', methods=['GET', 'POST'])
@admin_required
def new_chapter():
    form = ChapterForm()
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        chapter = Chapter(
            name=form.name.data,
            description=form.description.data,
            subject_id=form.subject_id.data
        )
        db.session.add(chapter)
        db.session.commit()
        flash('Chapter created successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/new_chapter.html', form=form)

@admin_bp.route('/edit-chapter/<int:chapter_id>', methods=['GET', 'POST'])
@admin_required
def edit_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    form = ChapterForm(obj=chapter)
    form.subject_id.choices = [(s.id, s.name) for s in Subject.query.all()]
    if form.validate_on_submit():
        chapter.name = form.name.data
        chapter.description = form.description.data
        chapter.subject_id = form.subject_id.data
        db.session.commit()
        flash('Chapter updated successfully!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/edit_chapter.html', form=form, chapter=chapter)

@admin_bp.route('/delete-chapter/<int:chapter_id>')
@admin_required
def delete_chapter(chapter_id):
    chapter = Chapter.query.get_or_404(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    flash('Chapter deleted successfully!', 'success')
    return redirect(url_for('admin.admin_dashboard'))

@admin_bp.route('/quiz-management')
@admin_required
def quiz_management():
    quizzes = Quiz.query.all()
    return render_template('admin/quiz_management.html', quizzes=quizzes)

@admin_bp.route('/new-quiz', methods=['GET', 'POST'])
@admin_required
def new_quiz():
    form = QuizForm()
    form.chapter_id.choices = [(c.id, f"{c.name} ({c.subject.name})") for c in Chapter.query.all()]
    if form.validate_on_submit():
        quiz = Quiz(
            title=form.title.data,
            description=form.description.data,
            chapter_id=form.chapter_id.data,
            time_limit=form.time_limit.data
        )
        db.session.add(quiz)
        db.session.commit()
        flash('Quiz created successfully!', 'success')
        return redirect(url_for('admin.quiz_management'))
    return render_template('admin/new_quiz.html', form=form)

@admin_bp.route('/edit-quiz/<int:quiz_id>', methods=['GET', 'POST'])
@admin_required
def edit_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuizForm(obj=quiz)
    form.chapter_id.choices = [(c.id, f"{c.name} ({c.subject.name})") for c in Chapter.query.all()]
    if form.validate_on_submit():
        quiz.title = form.title.data
        quiz.description = form.description.data
        quiz.chapter_id = form.chapter_id.data
        quiz.time_limit = form.time_limit.data
        db.session.commit()
        flash('Quiz updated successfully!', 'success')
        return redirect(url_for('admin.quiz_management'))
    return render_template('admin/edit_quiz.html', form=form, quiz=quiz)

@admin_bp.route('/delete-quiz/<int:quiz_id>')
@admin_required
def delete_quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    db.session.delete(quiz)
    db.session.commit()
    flash('Quiz deleted successfully!', 'success')
    return redirect(url_for('admin.quiz_management'))

@admin_bp.route('/new-question/<int:quiz_id>', methods=['GET', 'POST'])
@admin_required
def new_question(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    form = QuestionForm()
    if form.validate_on_submit():
        question = Question(
            quiz_id=quiz_id,
            question_text=form.question_text.data,
            option_a=form.option_a.data,
            option_b=form.option_b.data,
            option_c=form.option_c.data,
            option_d=form.option_d.data,
            correct_answer=form.correct_answer.data
        )
        db.session.add(question)
        db.session.commit()
        
        if 'add_another' in request.form:
            flash('Question added successfully! Add another question.', 'success')
            return redirect(url_for('admin.new_question', quiz_id=quiz_id))
        else:
            flash('Question added successfully!', 'success')
            return redirect(url_for('admin.quiz_management'))
    return render_template('admin/new_question.html', form=form, quiz=quiz)

# In your Flask routes (views.py or routes.py)
from flask import render_template, abort
from .models import Quiz  # Ensure the Quiz model is imported

@admin_bp.route('/quiz/<int:quiz_id>/view_questions', methods=['GET', 'POST'])
@admin_required
def view_question(quiz_id):
    # Fetch the quiz and its related questions from the database
    quiz = Quiz.query.get_or_404(quiz_id)
    return render_template('admin/view_question.html', quiz=quiz)



@admin_bp.route('/admin/edit-question/<int:question_id>', methods=['GET', 'POST'])
@admin_required
def edit_question(question_id):
    # Retrieve the question by its ID
    question = Question.query.get_or_404(question_id)
    
    # Initialize the form and bind it with the current question's data
    form = QuestionForm(obj=question)

    if form.validate_on_submit():
        # Update the question's fields based on form data
        question.question_text = form.question_text.data
        question.option_a = form.option_a.data
        question.option_b = form.option_b.data
        question.option_c = form.option_c.data
        question.option_d = form.option_d.data
        question.correct_answer = form.correct_answer.data
        
        # Commit the changes to the database
        db.session.commit()
        
        # Redirect to the view questions page
        return redirect(url_for('admin.view_question', quiz_id=question.quiz.id))
    
    # Render the template and pass the form object
    return render_template('admin/edit_question.html', form=form, question=question)

@admin_bp.route('/delete-question/<int:question_id>')
@admin_required
def delete_question(question_id):
    question = Question.query.get_or_404(question_id)
    quiz_id = question.quiz_id
    db.session.delete(question)
    db.session.commit()
    flash('Question deleted successfully!', 'success')
    return redirect(url_for('admin.edit_quiz', quiz_id=quiz_id))
