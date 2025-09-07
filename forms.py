from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from wtforms.widgets import TextArea

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class TicketForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=200)])
    category = SelectField('Category', choices=[
        ('technical', 'Technical Issue'),
        ('billing', 'Billing'),
        ('general', 'General Inquiry'),
        ('feature_request', 'Feature Request'),
        ('bug_report', 'Bug Report')
    ], validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ], validators=[DataRequired()], default='medium')
    description = TextAreaField('Description', validators=[DataRequired()], widget=TextArea())
    submit = SubmitField('Create Ticket')

class UpdateTicketForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed')
    ], validators=[DataRequired()])
    assigned_to = SelectField('Assign To', coerce=int)
    submit = SubmitField('Update Ticket')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()], widget=TextArea())
    is_internal = BooleanField('Internal Comment (Admin Only)')
    submit = SubmitField('Add Comment')
