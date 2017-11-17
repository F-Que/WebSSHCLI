from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, SubmitField
from wtforms.validators import DataRequired


class ConnectToHost(FlaskForm):
    host = StringField('Host', validators=[DataRequired()])
    port = IntegerField('Port', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField('Connect')
