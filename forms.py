from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, RadioField, DateField
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

class ApplicantForm(FlaskForm):
    prefix = SelectField('Prefix', choices=[("Mr","Mr"),("Mrs","Mrs",),("Miss","Miss")])
    surname = StringField('Surname', validators=[DataRequired()])
    othername = StringField('Othername', validators=[DataRequired()])
    nationality = SelectField('Nationality', choices=[("Ghana","Ghana"),("Nigeria","Nigeria")])
    mobile = StringField('Mobile', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[("Male","Male"),("Female","Female")]) 
    dateofbirth = DateField('Dateofbirth', format='%Y-%m-%d')
    campus = SelectField('Campus', choices=[("Kumasi","Kumasi"),("Mataheko","Mataheko"),("Christ Temple","Christ Temple")]) 
    stream = SelectField('Stream', choices=[("Morning","Morning"),("Evening","Evening")]) 
    entrymode = SelectField('Entrymode', choices=[("Direct","Direct"),("Cohort","Cohort")]) 
    submit = SubmitField('Next')

class ApplicantEducation(FlaskForm):
    school = StringField('School', validators=[DataRequired()])
    start_date = DateField('Startdate', format='%Y-%m-%d')
    end_date = DateField('Enddate', format='%Y-%m-%d')
    submit = SubmitField('Next')
