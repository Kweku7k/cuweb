from flask import Flask,redirect,url_for,render_template,request, send_from_directory, current_app, flash
import os
from forms import *
from flask_login import UserMixin, login_user, login_required, LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import httpx
from datetime import datetime
import urllib.request, urllib.parse
import csv

import random
import string

app=Flask(__name__)
baseUrl = "http://online.central.edu.gh"
baseIp = "http://45.222.128.225:5000"

app.config['UPLOAD_FOLDER']='Documents'
app.config['SECRET_KEY'] = '5791628basdfsadfa32242sdfsfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "apply"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False,unique=False)
    code = db.Column(db.String,nullable=False,unique=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    phone = db.Column(db.String)
    paid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Payments(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'payments'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable=False,unique=False)
    amount = db.Column(db.String,nullable=False,unique=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    phone = db.Column(db.String)
    network = db.Column(db.String)
    paid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)
    

class ApplicantInformation(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'applicantinformation'

    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.String,nullable=False,unique=False)
    usercode = db.Column(db.String,nullable=False,unique=False)
    surname = db.Column(db.String,nullable=False,unique=False)
    othername = db.Column(db.String,nullable=False,unique=False)
    nationality = db.Column(db.String,nullable=False,unique=False)
    email = db.Column(db.String,nullable=False,unique=False)
    campus = db.Column(db.String,nullable=False,unique=False)
    stream = db.Column(db.String,nullable=False,unique=False)
    date_of_birth = db.Column(db.DateTime)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    phone = db.Column(db.String())
    entry_mode = db.Column(db.String())
    filed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User {}>'.format(self.name)


class Education(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'applicanteducation'

    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.String,nullable=False,unique=False)
    usercode = db.Column(db.String,nullable=False,unique=False)
    school = db.Column(db.String,nullable=False,unique=False)
    start = db.Column(db.DateTime,nullable=False,unique=False)
    endDate = db.Column(db.DateTime,nullable=False,unique=False)
    entry_mode = db.Column(db.String())
    filed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Education {}>'.format(self.school)

class Programs(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'programs'

    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.String,nullable=False,unique=False)
    usercode = db.Column(db.String,nullable=False,unique=False)
    program = db.Column(db.String,nullable=False,unique=False)
    programchoice = db.Column(db.String,nullable=False,unique=False)
    entry_mode = db.Column(db.String())
    filed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Program {}>'.format(self.program)


class Guardian(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'guardian'

    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.String,nullable=False,unique=False)
    usercode = db.Column(db.String,nullable=False,unique=False)
    relationship = db.Column(db.String,nullable=False)
    name = db.Column(db.String,nullable=True)
    address = db.Column(db.String,nullable=True)
    mobile = db.Column(db.String,nullable=True)
    email = db.Column(db.String,nullable=True)
    occupation = db.Column(db.String,nullable=True)
    filed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Guardian {}>'.format(self.program)

class Exam(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'exam'

    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.String,nullable=False,unique=False)
    usercode = db.Column(db.String,nullable=False,unique=False)
    indexNumber = db.Column(db.String)
    exam = db.Column(db.String)
    date = db.Column(db.DateTime)
    filed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Exam {}>'.format(self.program)

class ExamResult(db.Model, UserMixin):
    """Model for user accounts."""
    __tablename__ = 'examResult'

    id = db.Column(db.Integer,primary_key=True)
    userId = db.Column(db.String,nullable=False,unique=False)
    usercode = db.Column(db.String,nullable=False,unique=False)
    indexNumber = db.Column(db.String)
    exam = db.Column(db.String)
    date = db.Column(db.DateTime)
    filed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Exam {}>'.format(self.program)


@login_manager.user_loader
def user_loader(user_id):
    #TODO change here
    return User.query.get(user_id)

@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('index.html')

# def payWithPresto():
#     httpx.get('prestoghana.com/pay')

def sendsms(phone,message, exceptionPath):
    api_key = "aniXLCfDJ2S0F1joBHuM0FcmH" #Remember to put your own API Key here
    message  = message + "\n \nPowered by PrestoGhana"
    params = {"key":api_key,"to":phone,"msg":message,"sender_id":"PrestoSl"}
    url = 'https://apps.mnotify.net/smsapi?'+ urllib.parse.urlencode(params)
    
    try:
        content = urllib.request.urlopen(url).read()
        print (content)
        print (url)
    except Exception as e:
        print("Exception at " + exceptionPath + "from send sms function.")

    return content


@app.route('/readcsv', methods=['GET', 'POST'])
def readcsv():
    with open('Documents/Lecturers.csv', 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        array = []

        for line in csv_file:
            line = line.split(",")
            lec = line[0] + " " + line[2] + " " + line[1]
            dep = line[4]
            print(lec)
            array.append(dep)
        
        array = list(dict.fromkeys(array))
            
        return array

@app.route('/buyforms', methods=['GET', 'POST'])
def buyforms():
    form = BuyForms()
    if request.method == 'POST':
        if form.validate_on_submit():

            try:
                newPayment = Payments(
                    name=form.name.data,
                    amount = form.amount.data,
                    phone=form.phone.data,
                    network=form.network.data
                )

                db.session.add(newPayment)
                db.session.commit()
            
                confirm(newPayment.id)

                response = payWithPresto(newPayment.id)
                print(response)
                return redirect(url_for('apply'))

            except Exception as e:
                print(e)
                print("Exception in /buyforms validation, payment creation")

            flash(f'Please check your email and your sms for the verification code.')
            return redirect(url_for('apply'))

        else:
            print(form.errors)

    return render_template('buyforms.html', form=form)

def payWithPresto(paymentId):

    payment = Payments.query.get_or_404(paymentId)

    prestoUrl = "https://sandbox.prestoghana.com/korba"

    paymentInfo = {
            "appId":"centraluniversity",
            "ref":payment.name,
            "reference":payment.name,
            "paymentId":payment.id, 
            "phone":"0"+payment.phone[-9:],
            "amount":payment.amount,
            "total":payment.amount, #TODO:CHANGE THIS!
            "recipient":"external", #TODO:Change!
            "percentage":"5",
            "callbackUrl":baseIp+"/confirm/"+str(payment.id),#TODO: UPDATE THIS VALUE
            "firstName":payment.name,
            "network":payment.network,
        }
    r = httpx.post(prestoUrl, json=paymentInfo)
    return r.json()

def randomLetters(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))


@app.route('/apply', methods=['GET', 'POST'])
def apply():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit: 
            user = User.query.filter_by(code = form.code.data).first()
            if user != None:
                print(user)
                login_user(user)
                return redirect(url_for('applicantInformation'))
            else:
                flash(f'Oopss, no code was found. please check and try again', "danger")
    else:
        print("asdf")
        flash(f'The verification code has been sent to your email and your sms.', category="success")
    return render_template('verification.html', form=form)

@app.route('/confirm/<transactionId>', methods=['GET', 'POST'])
def confirm(transactionId):
    payment = Payments.query.get_or_404(transactionId)

    try:
        request.args.get("reference")
    except Exception as e:
        print(e)

    code = randomLetters(10).upper()

    if payment != None:

        try:
            newuser = User(name = payment.name, code=code, phone=payment.phone, paid=True)
            db.session.add(newuser)
            db.session.commit()

            message = "Hi "+ payment.name + "\nYou have successfully purchased bought an application form. Your code is: " + code + "\n You can apply here: http://online.central.edu.gh/apply/"+code
            sendsms(payment.phone, message, "Exception sending sms after successful payment of form!")
            
        except Exception as e:
            print("Exception creating user after successful payment!")
            print(e)
            
    print(code)
    flash(f'Code - ' + code, "success")

    return code

@app.route('/applicationform', methods=['GET', 'POST'])
@login_required
def applicationform():
    return current_user.name

@app.route('/')
def online():
    return render_template('online.html', title="Online Application Form.")

@app.route('/downloadOnlineManual', methods=['GET', 'POST'])
def downloadOnlineManual():
    path = os.path.join(current_app.root_path, app.config['UPLOAD_FOLDER'])
    print(path)
    filename = "online_forms_manual.pdf"
    return send_from_directory(path, filename, as_attachment=True)

@app.route('/post')
def post():
    return render_template('post.html')

@app.route('/applicantInformation', methods=['GET', 'POST'])
@login_required
def applicantInformation():
    form=ApplicantForm()
    # save form as session?
    print(current_user.code)

    if request.method=='POST':
        if form.validate_on_submit:
            try:
                newapplicantInformation = ApplicantInformation(
                    surname = form.surname.data,
                    userId = current_user.id,
                    usercode = current_user.code,
                    othername = form.othername.data,
                    nationality = form.nationality.data,
                    email = form.email.data,
                    campus = form.campus.data,
                    stream = form.stream.data,
                    date_of_birth = form.dateofbirth.data,
                    phone = form.mobile.data,
                    entry_mode = form.entrymode.data,
                    filed = True
                ) 

                db.session.add(newapplicantInformation)
                db.session.commit()

            except Exception as e:
                print("e")
                print(e)

            return redirect('applicantEducation')

        else:
            print(form.errors)
            flash(form.errors[0],"danger")
    elif request.method=='GET':

        userdata = ApplicantInformation.query.filter_by(usercode = current_user.code).first()
    
        if userdata:
            if userdata.filed == True:
                form.surname.data = userdata.surname
                form.othername.data = userdata.othername 
                form.nationality.data = userdata.nationality
                form.email.data = userdata.email,
                form.campus.data = userdata.campus,
                form.stream.data = userdata.stream,
                form.dateofbirth.data = userdata.date_of_birth,
                form.mobile.data = userdata.phone,
                form.entrymode.data = userdata.entry_mode
        else:
            pass

    return render_template('applicantInformation.html', form=form)


@app.route('/applicantEducation', methods=['GET', 'POST'])
def applicantEducation():
    form=ApplicantEducation()

    if request.method=='POST':
        if form.validate_on_submit:

            newApplicantEducation = Education(
            userId = current_user.id,
            usercode = current_user.code,
            school = form.school.data,
            start = form.start_date.data,
            endDate = form.end_date.data,
            filed = True
            )    
            db.session.add(newApplicantEducation)
            db.session.commit()        

            return redirect(url_for('applicantPrograms'))
        else:
            print(form.errors)

    if request.method == 'GET':
        userdata = Education.query.filter_by(usercode = current_user.code).first()
        
        # print(userdata.school)
        # print(type(userdata.school))

        if userdata:
            if userdata.filed == True:
                form.school.data = userdata.school,
                #TODO:
                # form.start_date.data = userdata.start,
                # form.end_date.data = userdata.endDate
        else:
            print(form.errors)

    return render_template('applicantEducation.html', form=form)


@app.route('/applicantPrograms', methods=['GET', 'POST'])
def applicantPrograms():
    form=ApplicantProgram()
    if request.method=='POST':
        print("POST FORM!")
        if form.validate_on_submit:
            print(form.program.data)

            newPrograms = Programs(
            userId = current_user.id,
            usercode = current_user.code,
            program = form.program.data,
            programchoice = form.programchoice.data,
            filed = True
            )    

            db.session.add(newPrograms)
            db.session.commit() 
            return redirect(url_for('applicantGuardian'))

        else:
            print(form.errors)
        
        return redirect(url_for('applicantGuardian'))

    if request.method == 'GET':
        print("lol")

    return render_template('applicantPrograms.html', form=form)

@app.route('/applicantGuardian', methods=['GET', 'POST'])
def applicantGuardian():
    form=ApplicantGuardian()

    if request.method=='POST':
        if form.validate_on_submit:
            applicationGuardian = Guardian(
                    userId = current_user.id,
                    usercode = current_user.code,
                    relationship = form.guardianrelationship.data,
                    name = form.guardianname.data,
                    address = form.guardianaddress.data,
                    mobile = form.guardianmobile.data,
                    email = form.guardianemail.data,
                    occupation = form.guardianjob.data,
                    filed = True
                    )
            db.session.add(applicationGuardian)
            db.session.commit()
        else:
            print("Home asdf")
            print(form)

    elif request.method == 'GET':
        userdata = Guardian.query.filter_by(usercode = current_user.code).first()

        if userdata:
            if userdata.filed == True:
                form.guardianrelationship.data = userdata.relationship
                form.guardianname.data = userdata.name
                form.guardianaddress.data = userdata.address
                form.guardianmobile.data = userdata.mobile
                form.guardianemail.data = userdata.email,
                form.guardianjob.data = userdata.occupation

        else:
            pass

        return redirect(url_for('applicantExam'))

    else:
        print("asfd")

    return render_template('applicantGuardian.html', form=form)

@app.route('/applicantExam', methods=['GET', 'POST'])
def applicantExam():
    form=ApplicantExams()

    if request.method=='POST':
        if form.validate_on_submit:
            print("form.exam.data")
            exam = Exam(
                    userId = current_user.id,
                    usercode = current_user.code,
                    exam = form.examtype.data,
                    indexNumber = form.indexnumber.data,
                    date = form.exam_date.data,
                    filed = True)
            db.session.add(exam)
            db.session.commit()
            return redirect(url_for('applicantExamresult'))
    elif request.method == 'GET':
        userdata = Exam.query.filter_by(usercode = current_user.code).first()

        if userdata:
            if userdata.filed == True:
                form.indexnumber.data = userdata.indexNumber
                # form.exam.data = userdata.exam
            
    return render_template('applicantExam.html', form=form)


@app.route('/applicantExamresult')
def applicantExamresult():
    form=ApplicantExamresult()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            ExamResult
            print("formvalidated")
        return redirect(url_for('applicationEducation'))
    elif request.method == 'GET':
        userdata = ExamResult.query.filter_by(usercode = current_user.code).first()

        if userdata:
            if userdata.filed == True:
                pass
    # check form validation
    # check errors
    return render_template('applicantExamresult.html', form=form)


@app.route('/applicantcontacts')
def applicantcontacts():
    form=ApplicantContant()

    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantcontacts.html', form=form)

@app.route('/applicantattachments')
def applicantattachments():
    form=ApplicantAttachment()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantattachments.html', form=form)

@app.route('/applicantphotos')
def applicantphotos():
    form=ApplicantPhoto()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantphotos.html', form=form)


@app.route('/applicantanswers')
def applicantanswers():
    form=ApplicantAnswer()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantanswers.html', form=form)



@app.route('/applicantrefrees')
def applicantrefrees():
    form=ApplicantRefree()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantrefrees.html', form=form)



@app.route('/applicanthalls')
def applicanthalls():
    form=ApplicantHall()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicanthalls.html', form=form)


@app.route('/applicantmisinfos')
def applicantmisinfos():
    form=ApplicantMiscellaneousInformation()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantmisinfos.html', form=form)


@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/students')
def students():
    return render_template('students.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000, host='0.0.0.0', debug=True)


