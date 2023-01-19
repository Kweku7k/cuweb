from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField, RadioField, DateField, FileField
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
    othername = StringField('Other Name', validators=[DataRequired()])
    nationality = SelectField('Nationality', choices=[("Ghana","Ghana"),("Nigeria","Nigeria")])
    mobile = StringField('Mobile', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    sex = SelectField('Sex', choices=[("Male","Male"),("Female","Female")]) 
    dateofbirth = DateField('Date of Birth', format='%Y-%m-%d')
    campus = SelectField('Campus', choices=[("Kumasi","Kumasi"),("Mataheko","Mataheko"),("Christ Temple","Christ Temple")]) 
    stream = SelectField('Stream', choices=[("Morning","Morning"),("Evening","Evening")]) 
    entrymode = SelectField('Entry Mode', choices=[("Direct","Direct"),("Cohort","Cohort")]) 
    submit = SubmitField('Next')

class ApplicantEducation(FlaskForm):
    school = StringField('School', validators=[DataRequired()])
    start_date = DateField('Start Date', format='%Y-%m-%d')
    end_date = DateField('End Date', format='%Y-%m-%d')
    submit = SubmitField('Next')

class ApplicantExams(FlaskForm):
    examtype = SelectField('Exam Type', choices=[("Wassce","Wassce"),("Nov-Dec","Nov-Dec")])
    indexnumber = StringField('Index Number', validators=[DataRequired()])
    exam_date = DateField('Exam Date', format='%Y-%m-%d')
    submit = SubmitField('Next')

class ApplicantGuardian(FlaskForm):
    guardianrelationship = StringField('Relationship', validators=[DataRequired()])
    guardianname = StringField('Name', validators=[DataRequired()])
    guardianaddress = StringField('Address', validators=[DataRequired()])
    guardianmobile = StringField('Mobile', validators=[DataRequired()])
    guardianemail = StringField('Email', validators=[DataRequired()])
    guardianjob = StringField('Occupation', validators=[DataRequired()])
    submit = SubmitField('Next')

class ApplicantProgram(FlaskForm):
    program = SelectField('Program', choices=[("Computer Science","Computer Science"),("Information Technology","Information Technology")])
    programchoice = SelectField('Program Choice', choices=[("First Choice","First Choice"),("Second Choice","Second Choice")])
    submit = SubmitField('Next')

class ApplicantExamresult(FlaskForm):
    applicantexam = SelectField('Applicant Exam', choices=[("Degree","Degree"),("Diploma","Diploma")])
    subject = SelectField('Subject', choices=[("Dip.Enterprise Management","Dip.Enterprise Management"), ("Dip.Enterprise Management","Dip.Enterprise Management")])
    grade = SelectField('Grade', choices=[("1st Class Upper","1st Class Upper"),("2nd Class Upper","2nd Class Upper")])
    submit = SubmitField('Next')
    
class ApplicantContant(FlaskForm):
    contactrelationship = StringField('Relationship', validators=[DataRequired()])
    contactname = StringField('Name', validators=[DataRequired()])
    contactaddress = StringField('Address', validators=[DataRequired()])
    contactmobile = StringField('Mobile', validators=[DataRequired()])
    contactemail = StringField('Email', validators=[DataRequired()])
    contactjob = StringField('Occupation', validators=[DataRequired()])
    submit = SubmitField('Next')

class ApplicantAttachment(FlaskForm):
    attachmenttype = SelectField('Type', choices=[("Transcript","Transcript")])
    attachmentname = StringField('File Name', validators=[DataRequired()])
    attachmentfile = FileField('Upload file', validators=[DataRequired()])
    submit = SubmitField('Next')

class ApplicantPhoto(FlaskForm):
    photoname = StringField('File Name', validators=[DataRequired()])
    photofile = FileField('Upload file', validators=[DataRequired()])
    submit = SubmitField('Next')

class ApplicantAnswer(FlaskForm):
    applicantanswer = StringField('How did you get to know about Central University', validators=[DataRequired()])
    submit = SubmitField('Next')

class ApplicantRefree(FlaskForm):
    refreesname = StringField('Name', validators=[DataRequired()])
    refreesmobile = StringField('Mobile', validators=[DataRequired()])
    refreesemail = StringField('Email', validators=[DataRequired()])
    refreesjob = StringField('Occupation', validators=[DataRequired()])
    submit = SubmitField('Next')

class ApplicantHall(FlaskForm):
    applicanthall = SelectField('Hall of Affilliation', choices=[("CU Male Hostel","CU Male Hostel"), ("CU Female Hostel","CU Female Hostel")])
    submit = SubmitField('Next')

class ApplicantMiscellaneousInformation(FlaskForm):
    applicantmisinfo = StringField('Number of Children', validators=[DataRequired()])
    submit = SubmitField('Next')