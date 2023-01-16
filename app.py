from flask import Flask,redirect,url_for,render_template,request, send_from_directory, current_app, flash
import os
from forms import *
from flask_login import UserMixin, login_user, login_required, LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import httpx
from datetime import datetime
import random
import string

app=Flask(__name__)
baseUrl = "https:online.central.edu.gh"

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

                # response = payWithPresto(newPayment.id)
                # print(response)
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

    prestoUrl = "prestoghana.com/api/pay"
    paymentInfo = {
            "appId":"cu",
            "ref":payment.ref,
            "reference":payment.ref,
            "paymentId":payment.id, 
            "phone":"0"+payment.phone[-9:],
            "amount":payment.amount,
            "total":payment.total,
            "recipient":"payment", #TODO:Change!
            "percentage":"5",
            "callbackUrl":baseUrl+"/confirm/"+str(payment.id),#TODO: UPDATE THIS VALUE
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
                return redirect(url_for('applicationform'))
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

    code = randomLetters(10)

    if payment != None:

        try:
            newuser = User(name = payment.name, code=code, phone=payment.phone, paid=True)
            db.session.add(newuser)
            db.session.commit()
            
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
    return render_template('applicantPrograms.html')

@app.route('/applicantGuardian')
def applicantGuardian():
    return render_template('applicantGuardian.html')

@app.route('/applicantExam')
def applicantExam():
    return render_template('applicantExam.html')

@app.route('/applicantExamresult')
def applicantExamresult():
    return render_template('applicantExamresult.html')

@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/students')
def students():
    return render_template('students.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000, host='0.0.0.0', debug=True)


