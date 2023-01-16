from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, RadioField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

class BuyForms(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    network = SelectField('Network', choices=[("MTN","MTN"),("AIRTELTIGO","AIRTELTIGO"),("VODAFONE","VODAFONE")])
    email = StringField('Email', validators=[DataRequired()])
    amount = StringField('Amount', validators=[DataRequired()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    submit = SubmitField('Buy Now')

class LoginForm(FlaskForm):
    code = StringField('Code', validators=[DataRequired()])
    submit = SubmitField('Verify')