from wtforms import Form, StringField, TextAreaField, PasswordField, validators

class RegisterForm(Form):
        firstName = StringField('First Name', [validators.Length(min=1, max=50)])
        lastName = StringField('Last Name', [validators.Length(min=1, max=50)])
        rollNo = StringField('Roll Number', [validators.Length(7, message='Field must be 7 characters long')])
        username = StringField('Username', [validators.Length(min=4, max=25)])
        email = StringField('Email', [validators.Length(min=6, max=50)])
        password = PasswordField('Password', [
            validators.DataRequired(),
            validators.EqualTo('confirm', message='Passwords do not match')
            ])
        confirm = PasswordField('Confirm Password')
