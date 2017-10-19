from wtforms import Form, StringField, TextAreaField, PasswordField, SelectField, validators
from wtforms.fields.html5 import EmailField

departments = [('CO', 'Computer Engineering'), ('EC', 'Electronics & Communication'), ('CH', 'Chemical Engineering'), ('EE', 'Electrical Engineering'), ('ME', 'Mechanical Engineering')]

class RegisterForm(Form):
        firstName = StringField('First Name', [validators.Length(min=1, max=50)])
        lastName = StringField('Last Name', [validators.Length(min=1, max=50)])
        rollNo = StringField('Roll Number', [validators.Length(7, message='Field must be 7 characters long')])
        dept = SelectField('Department', choices=departments)
        username = StringField('Username', [validators.Length(min=4, max=25)])
        email = EmailField('Email address', [validators.DataRequired(), validators.Email()])
        password = PasswordField('Password', [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords do not match')
            ])
        confirm = PasswordField('Confirm Password')
        

categories = [('Academia', 'Academia'), ('Entertainment', 'Entertainment'), ('Sports', 'Sports'), ('Music', 'Music'), ('Art', 'Art'),('Politics', 'Politics'),('Other','Other')]

class PostForm(Form):
        url = StringField('URL of the article', [validators.Length(min=1, max=200)])       
        cat = SelectField('Category', choices=categories)
        
