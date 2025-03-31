from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, DateField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    full_name = StringField('Full Name', validators=[DataRequired()])
    qualification = StringField('Qualification', validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])

class ForgotPasswordForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])

class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class SubjectForm(FlaskForm):
    name = StringField('Subject Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])

class ChapterForm(FlaskForm):
    name = StringField('Chapter Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    subject_id = SelectField('Subject', coerce=int, validators=[DataRequired()])

class QuizForm(FlaskForm):
    title = StringField('Quiz Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[Optional()])
    chapter_id = SelectField('Chapter', coerce=int, validators=[DataRequired()])
    time_limit = IntegerField('Time Limit (minutes)', validators=[DataRequired()])


class QuestionForm(FlaskForm):
    question_text = TextAreaField('Question', validators=[DataRequired()])
    option_a = StringField('Option A', validators=[DataRequired()])
    option_b = StringField('Option B', validators=[DataRequired()])
    option_c = StringField('Option C', validators=[DataRequired()])
    option_d = StringField('Option D', validators=[DataRequired()])
    correct_answer = SelectField('Correct Answer', choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')], validators=[DataRequired()])
    submit = SubmitField('Save Question')  # This is the submit button
