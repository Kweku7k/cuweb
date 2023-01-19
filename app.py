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
    paid = db.Column(db.Boolean, default=True)

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
    paid = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return '<User {}>'.format(self.name)


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
            
                # confirm(newPayment.id)

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
            "appId":"cu",
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
            # route to acc form. Prefill the data with user, phone, email and code.
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

@app.route('/applicantInformation')
def applicantInformation():
    form=ApplicantForm()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
    # check form validation
    # check errors

    return render_template('applicantInformation.html', form=form)


@app.route('/applicantEducation')
def applicantEducation():
    form=ApplicantEducation()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantEducation.html', form=form)


@app.route('/applicantPrograms')
def applicantPrograms():
    form=ApplicantProgram()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantPrograms.html', form=form)

@app.route('/applicantGuardian')
def applicantGuardian():
    form=ApplicantGuardian()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantGuardian.html', form=form)

@app.route('/applicantExam')
def applicantExam():
    form=ApplicantExams()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantExam.html', form=form)

@app.route('/applicantExamresult')
def applicantExamresult():
    form=ApplicantExamresult()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print(form.email.data)
        return redirect(url_for('applicationEducation'))
    # check form validation
    # check errors
    return render_template('applicantExamresult.html', form=form)


@app.route('/applicantcontacts')
def applicantcontacts():
    form=ApplicantContant()
    # check request method
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


