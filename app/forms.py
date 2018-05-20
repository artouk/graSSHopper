from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class NewHost(FlaskForm):
    creator_id = IntegerField()
    org_id = IntegerField()
    host = StringField('Host', validators=[DataRequired()])
    address = StringField('Address', validators=[DataRequired()])
    description = TextAreaField('Description')
    sysuser = StringField('System User')
    port = IntegerField('Port', default=22)
    submit = SubmitField('Save')
