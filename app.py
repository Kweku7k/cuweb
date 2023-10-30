from flask import Flask,jsonify,redirect,url_for,render_template,request, send_from_directory, current_app, flash
import os

import requests
from forms import *
from flask_login import UserMixin, login_user, login_required, LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import requests
from datetime import datetime
import urllib.request, urllib.parse
import csv
import random
import string
import pprint



app=Flask(__name__)
baseUrl = "https://online.central.edu.gh"
baseIp = "http://45.222.128.225:5000"
prestoBot = "5876869228:AAFk644pEKRBnEhZ6jbG2nXRlj4fsyZEYgg"
prestoUrl = "https://prestoghana.com"
# centralAlertChannel = "-1001976261666"

app.config['UPLOAD_FOLDER']='Documents'
app.config['SECRET_KEY'] = '5791628basdfsadfa32242sdfsfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///test.db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "apply"

db = SQLAlchemy(app)
migrate = Migrate(app, db)

lecturerId = 92
adminStaffId = 93
eventsId = 101

totalNumberOfAdmissionForms = 10

def reportError(e):
    print(e)
    return "Noted!"

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
    firstchoice = db.Column(db.String())
    seconschoice = db.Column(db.String())
    thirdchoice = db.Column(db.String())
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


baseWpUrl = "https://webcms.central.edu.gh"
wpUrl = baseWpUrl+"/wp-json/wp/v2"

def sendTelegram(params):
    try:
        url = "https://api.telegram.org/bot"+prestoBot+"/sendMessage?chat_id="+centralAlertChannel+"&text=" + urllib.parse.quote(params)
        content = urllib.request.urlopen(url).read()
        app.logger.info(content)
        return content
    except Exception as e:
        app.logger.info(e)
        return e

# @app.errorhandler(404)
# def not_found_error(error):
#     sendTelegram(str(error) + "\n" + str(request.url) + "\n" + str(current_user))
#     return render_template('error.html', code="404", message="You are either misspelling the URL or requesting a page that's no longer here."), 404


@app.errorhandler(500)
def internal_server_error(error):
    sendTelegram(str(error) + "\n" + str(request.url) + "\n" + str(current_user))
    return render_template('error.html', code="500", message="There has been an internal error. Our engineers are on it, please check and try again later."), 500

# @app.errorhandler(500)
# def not_found_error(error):
#     sendTelegram(str(error) + "\n" + str(request.url) + "\n" + str(current_user))
#     return render_template('error.html', code=error, message="You are either misspelling the URL or requesting a page that's no longer here."), 500

# @app.errorhandler(503)
# def not_found_error(error):
#     sendTelegram(str(error) + "\n" + str(request.url) + "\n" + str(current_user))
#     return render_template('error.html', code=error, message="You are either misspelling the URL or requesting a page that's no longer here."), 503


@login_manager.user_loader
def user_loader(user_id):
    #TODO change here
    return User.query.get_or_404(user_id)

@app.route('/',methods=['GET','POST'])
def home():
    form = ContactForm()
    gallery = wpgallery(5)
    supportGallery = wpgallery(6)
    events = getEvents()[0]
    print("------------------events------------------")
    print(events)

    print("gallery")
    print(gallery)

    if request.method == 'POST':
        if form.validate_on_submit():
            print("firing form")
            try:
                message = "From: " + form.name.data + "\nPhone: " + form.number.data + "\nEmail: " + form.email.data + "\nMessage: " + form.message.data
                print("message")
                print(message)
                prestoUrl
                r = requests.get(prestoUrl+'/sendPrestoMail?recipient=info@central.edu.gh&subject='+form.name.data+'&message='+message)
                print(r.url)
                flash('Hi, ' + form.name.data +' your message has been submitted successfully.','success')
            except Exception as e:
                print(e)
                print("Unable to send emails!")
                flash('Oops, there was an error sending your email, please check and try again.','fail')
            # return render_template('index.html',hideNav=True, form=form)
            return redirect(url_for('home'))
        else:
            print(form.errors)

    return render_template('index.html',hideNav=False, form=form, gallery=gallery, events=events, supportGallery=supportGallery)

# def payWithPresto():
#     requests.get('prestoghana.com/pay')

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
    r = requests.post(prestoUrl, json=paymentInfo)
    return r.json()

def randomLetters(y):
       return ''.join(random.choice(string.ascii_letters) for x in range(y))


admissionMap = {
    1:{
        'current':'applicantInformation',
        'previousUrl':'applicantInformation',
        'nextUrl':'applicantPrograms',
        'next':'Applicant Programs',
        'description':'Please be very discriptive and fill the form accordingly so we have a clear picture of who you are',
        'title':'Personal Information',
        'percentage': (1/totalNumberOfAdmissionForms)*100
    },
    2:{
        'current':'applicantInformation',
        'previous':'Applicant Information',
        'previousUrl':'applicantInformation',
        'nextUrl':'applicantEducation',
        'next':'ApplicantEducation',
        'description':'Please select your program choices',
        # 'description':'Please include your schools and the years in which you comleted.',
        'title':'Program Choices',
        'percentage': (2/totalNumberOfAdmissionForms)*100
    },
    3:{
        'previous':'Program Choices',
        'previousUrl':'applicantPrograms',
        'nextUrl':'applicantEmployment', #TODO!
        'current':'applicantEducation',
        'next':'Employment',
        'description':'Please fill the form containing the data ',
        'title':'Applicant Education',
        'percentage': (3/totalNumberOfAdmissionForms)*100
    },
    4:{
        'title':'Applicant Employment',
        'previous':'Prog',
        'previousUrl':'applicantPrograms',
        'nextUrl':'applicantEmployment', #TODO!
        'current':'applicantEducation',
        'next':'Employment',
        'description':'Please fill the form containing the data ',
        'percentage': (3/totalNumberOfAdmissionForms)*100
    }
    
}


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
        # flash(f'The verification code has been sent to your email and your sms.', category="success")
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

@app.route('/online')
def online():
    return render_template('online.html', hideNav = True, title="Online Application Form.")

@app.route('/404')
def error():
    return not_found_error(404)

@app.route('/chapel')
def chapel():
    return render_template('chapel.html')

# @app.route('/about')
# def about():
#     response = requests.get(wpUrl+"/categories?parent=4")
#     print("all categories with parent category 4")
#     print(response)
#     print("-----------------")
#     posts = requests.get(wpUrl+"/posts?categories=4")
#     posts = posts.json()
#     print("posts")
#     allposts = []
#     for p in posts:
#         categories = p["categories"]
#         categories.remove(4)
#         allposts.append({"id":str(categories[0]),
#                         "content":p["content"]["rendered"]
#                         })

#     print("allposts")
#     print(allposts)

#     tags = response.json()

#     alltags=[]
#     for t in tags:
#         alltags.append({"id":t["id"], "name":t["name"]})
#     print(alltags)
#     return render_template('about.html', tags = alltags, posts=allposts)

# @app.route('/aboutapi')
# def aboutapi():
#     # getByCategory=About
#     posts = requests.get(wpUrl+"/posts?categories=4")
#     posts = posts.json()
#     print("posts")
#     allposts = []
#     for p in posts:
#         categories = p["categories"]
#         categories.remove(4)
#         allposts.append({"id":str(categories[0]),
#                          "title":p["title"]["rendered"],
#                         "content":p["content"]["rendered"]
#                         })

#     print("allposts")
#     print(allposts)
#         # remove 4

#     # print(posts)
#     # storeArticlesBy
#     # print(response.json())
#     return allposts

    # return render_template('about.html' posts=allposts)

@app.route('/cu')
def cu():
    return render_template('cu.html')


# @app.route('/admission')
# def admission():
#     return render_template('admission.html')

def getImageUrl(id):
    print(id)
    try:
        url=baseWpUrl+"/?rest_route=/wp/v2/media/"+str(id)
        r=requests.get(url)
        print(r)
        image = r.json()["guid"]["rendered"]
    except Exception as e:
        print(e)
        image = "https://banner2.cleanpng.com/20190216/fox/kisspng-central-university-ghana-technology-university-col-school-of-theology-amp-missions-central-univer-5c67c799ec2858.1783459915503051779673.jpg"
    return image

def fetch(url, params):
    try:
        url=baseWpUrl+"/wp-json/wp/v2/posts"+str(id)
        r=requests.get(url)
        print(r)
        image = r.json()["guid"]["rendered"]
    except Exception as e:
        print(e)
        image = "https://banner2.cleanpng.com/20190216/fox/kisspng-central-university-ghana-technology-university-col-school-of-theology-amp-missions-central-univer-5c67c799ec2858.1783459915503051779673.jpg"
    return image

@app.route('/news')
def news():
    page = request.args.get("page","1")
    print("page")
    print(page)
    # Get URL
    id = 24
    per_page=30
    url=baseWpUrl+"/wp-json/wp/v2/posts?page="+str(page)+"&categories="+str(id)+"&per_page="+str(per_page)
    # url = "http://45.222.128.105/wp-json/wp/v2/posts?categories="+str(id)
    r=requests.get(url)
    response= r.json()
    print("response.headers")
    print(r.headers)
    totalPages = (r.headers["x-wp-totalpages"])
    news = []
    for i in response:
        article = {}
        article["id"] = i["id"]
        article["image"] = getImageUrl(i["featured_media"])
        article["title"] = i["title"]["rendered"]
        news.append(article)
    print(news)
    return render_template('news.html', news=news, totalPages=totalPages, page=page, per_page=per_page)


@app.route('/lecturers')
def lecturers():
    page = request.args.get("page","1")
    print("page")
    print(page)
    # Get URL
    id = lecturerId
    per_page=10
    url=baseWpUrl+"/wp-json/wp/v2/posts?page="+str(page)+"&categories="+str(id)+"&per_page="+str(per_page)
    # url = "http://45.222.128.105/wp-json/wp/v2/posts?categories="+str(id)
    r=requests.get(url)
    response= r.json()
    print("response.headers")
    print(r.headers)
    totalPages = (r.headers.get("x-wp-totalpages"))
    news = []
    for i in response:
        article = {}
        article["id"] = i["id"]
        article["image"] = getImageUrl(i["featured_media"])
        article["title"] = i["title"]["rendered"]
        news.append(article)
    print(news)
    return render_template('news.html', news=news, totalPages=totalPages, page=page, per_page=per_page)


def getCategoryInformation(categoryId):
    url = wpUrl+"/categories/"+str(categoryId)
    print(url)
    response = requests.get(url).json()
    print("------getCategoryData------")
    pprint.pprint(response)
    print("------endGetCategoryData------")
    return response

@app.route('/lecturers/<string:department>')
def lecturersByDepartment(department):
    page = request.args.get("page","1")
    print("page")
    print(page)
    # Get URL
    id = lecturerId
    per_page=10
    url=baseWpUrl+"/wp-json/wp/v2/posts?page="+str(page)+"&parent="+str(id)+"&categories="+str(department)+"&per_page="+str(per_page)
    r=requests.get(url)
    response= r.json()
    pprint.pprint("-------------")
    pprint.pprint(response)
    pprint.pprint("-------------")
    print("response.headers")
    print(r.headers)
    totalPages = (r.headers.get("x-wp-totalpages"))
    news = []
    for i in response:
        # if find_in_array(i["categories"], id) and find_in_array(i["categories"], department):
        if find_in_array(i["categories"], id):
            article = {}
            article["id"] = i["id"]
            article["image"] = getImageUrl(i["featured_media"])
            article["title"] = i["title"]["rendered"]
            news.append(article)
    print(news)

    category = getCategoryInformation(department)
    categoryTitle = category["name"]

    return render_template('news.html', news=news, totalPages=totalPages, page=page, per_page=per_page, title=categoryTitle)


@app.route('/events')
def events_view():
    news = getEvents()
    return render_template('news.html', news=news , totalPages=1, page=1, per_page=10, title="Upcoming Events")


def getEvents():
    # Get URL
    url=baseWpUrl+"/wp-json/wp/v2/posts?categories="+str(eventsId)
    # url = "http://45.222.128.105/wp-json/wp/v2/posts?categories="+str(id)
    r=requests.get(url)
    response= r.json()
    pprint.pprint(response)
    events = []
    for i in response:
        article = {}
        article["id"] = i["id"]
        article["image"] = getImageUrl(i["featured_media"])
        article["title"] = i["title"]["rendered"]
        # article["title"] = i["title"]
        events.append(article)
    print(events)
    return events


@app.route('/gallery')
def gallery():
    # Get URL
    id = 24
    url=baseWpUrl+"/wp-json/wp/v2/posts?categories="+str(id)
    # url = "http://45.222.128.105/wp-json/wp/v2/posts?categories="+str(id)
    r=requests.get(url)
    response= r.json()
    news = []
    for i in response:
        article = {}
        article["id"] = i["id"]
        article["image"] = getImageUrl(i["featured_media"])
        article["title"] = i["title"]["rendered"]
        # article["title"] = i["title"]
        news.append(article)
    print(news)
    return render_template('gallery.html', gallery=gallery)

# @app.route('/maintenance', methods=['GET', 'POST'])
# def maintenance():
#     form = ContactForm()

#     if request.method == 'POST':
#         if form.validate_on_submit():
#             print("firing form")
#             # requests.post('prestoghana.com/sendMail')
#             flash('Your message has been submitted successfully.','success')
#         else:
#             print(form.errors) 
            
#     return render_template('maintenance.html',hideNav=True, form=form)

@app.route('/wppost/<string:id>')
def wppost(id):
    # Get URL
    url=baseWpUrl+"/?rest_route=/wp/v2/posts/"+id
    r=requests.get(url)
    content= r.json()["content"]["rendered"]
    print(content[0])
    return jsonify({'rendered_content': r.json()})

@app.route('/wppostbyslug/<string:slug>')
def wppostbyslug(slug):
    # Get URL
    url=wpUrl+"/posts/"+slug
    r=requests.get("https://webcms.central.edu.gh/wp-json/wp/v2/posts?slug="+slug)
    content=r.json()[0]["content"]["rendered"]
    print(content[0])
    return jsonify({'rendered_content': r.json()})

@app.route('/wpgallery/<string:id>')
def wpgallery(id):
    images = []
    # url=baseWpUrl+"/?rest_route=/wp/v2/media?author="+id
    url = wpUrl+"/media?author="+str(id)
    r= requests.get(url)

    response = r.json()
    
    # find length
    noOfImages = len(response)
    print(noOfImages)

    for i, index in enumerate(response):
        content= r.json()[i]["guid"]["rendered"]
        images.append(content)

    print(images)

    return images   



# FindPostByCategoryId
# url = wpUrl+"posts?categories=63"

@app.route('/schoolpage/<string:slug>', methods=['GET', 'POST'])
def schoolpage(slug):

    print("Logging articles by slug - " + slug)
    
    wppost = '/wppostbyslug/'+str(slug)
    post = wppostbyslug(slug).json

    print("Response:")
    pprint.pprint(post) #This prints the post in json format.

    # Returning School Image.
    imageUlr = getImageUrl(post["rendered_content"][0]["featured_media"]) 
    print(imageUlr)

    # Getting sub departments
    print("Getting Sub Departments")
    departments = []
    
    # find category by name
    print("Finding Category By Name")
    url = wpUrl+"/categories?slug="+str(slug)
    subdepartments = requests.get(url).json()
    
    lecturers = []
    adminStaff = []

    if subdepartments != []:
        try:
            print("SubDepartments Found:")
            pprint.pprint(subdepartments[0]["id"])
        except Exception as e:
            print(e)

        # categoryId = subdepartments
        if subdepartments != None:
            categoryId = subdepartments[0]["id"]

            print("Category Id: " + str(categoryId))

            allPosts = returnPostsUnderCategoryId(categoryId)
            # filter by respective category ids?
            print("------- POSTS BY ID ---------")
            pprint.pprint(allPosts)


            for p in allPosts:
                if p["id"] == post["rendered_content"][0]["id"]:
                    pass
                elif find_in_array(p["categories"], lecturerId):
                    lecturers.append(p)
                elif find_in_array(p["categories"], adminStaffId):
                    adminStaff.append(p)
                else:   
                    departments.append(p)

    # 
        print("------LECTURERS-------")
        pprint.pprint(lecturers)
    
    else:
        return "Not found."


    print("CategoryId: " + str(categoryId))

    return render_template('schoolpage.html', url=wppost, image=imageUlr, departments=departments, adminStaff=adminStaff, lecturers=lecturers, categoryId=str(categoryId))


def find_in_array(arr, target_char):
    for i in arr:
        if target_char == i:
            return True
    return False

    # return any(target_char in item for item in arr)

@app.route('/expand/<string:id>')
def expand(id):
    # Get URL
    # url=baseWpUrl+"/?rest_route=/wp/v2/posts/"+id
    wppost = '/wppost/'+str(id)
    return render_template('expand.html', url=wppost)



@app.route('/staff')
def staff():
    return render_template('staff.html')

@app.route('/privacypolicy', methods=['GET', 'POST'])
def privacypolicy():
    return render_template('privacypolicy.html')

@app.route('/school', methods=['GET', 'POST'])
def school():
    return render_template('school.html')


@app.route('/admissions', methods=['GET', 'POST'])
def admissions():
    return render_template('admissions.html')

@app.route('/alumni')
def alumni():
    return render_template('alumni.html')


def returnPostsUnderCategoryId(id):
    per_page = 100
    print("Fetching Posts Under Category: " + str(id))
    posts = requests.get(wpUrl+"/posts?categories="+str(id)+"&per_page="+str(per_page))
    posts = posts.json()

    pprint.pprint(posts)

    allposts = []
    for p in posts:
        print(p)
        print(p.get("featured_media"))

        # TODO: Remove currently opened post

        allposts.append({
            "id":p["id"],
            "categories":p["categories"],
            "title":p["title"]["rendered"],
            "image":getImageUrl(p["featured_media"])
        })

    return allposts





def returnTags(id, categoryName):
    response = requests.get(wpUrl+"/categories?parent="+str(id))
    print("Returning categories under parent category "+str(id) + str(categoryName))
    print(response)
    print("-----------------")
    posts = requests.get(wpUrl+"/posts?categories="+str(id))
    posts = posts.json()
    print("posts")
    allposts = []
    for p in posts:
        categories = p["categories"]
        categories.remove(id)
        allposts.append({"id":str(categories[0]),"title":p["title"]["rendered"],"content":p["content"]["rendered"]})

    alltags=[]
    tags = response.json()

    for t in tags:
        alltags.append({"id":t["id"], "name":t["name"]})
    print(alltags)

    return {"tags":alltags, "posts":allposts}

@app.route('/library')
def library():
    id = 17
    alltags = returnTags(id, "library")["tags"]
    allposts = returnTags(id, "library")["posts"]
    print("allposts being returned")
    print(allposts)
    startingPoint = alltags[0]["id"]
    return render_template('library.html',tags=alltags, id=startingPoint, allposts=allposts)

@app.route('/about')
def about():
    id = 2
    alltags = returnTags(id, "library")["tags"]
    allposts = returnTags(id, "library")["posts"]
    print("allposts being returned")
    print(allposts)
    startingPoint = alltags[0]["id"]
    return render_template('library-dynamic.html',id=startingPoint,tags=alltags, allposts=allposts)


@app.route('/admission')
def admission():
    id=4
    alltags = returnTags(id, "library")["tags"]
    allposts = returnTags(id, "library")["posts"]
    print("allposts being returned")
    print(allposts)
    startingPoint = alltags[0]["id"]
    return render_template('library-dynamic.html',id=startingPoint,tags=alltags, allposts=allposts)


@app.route('/international')
def international():
    id=15
    alltags = returnTags(id, "library")["tags"]
    allposts = returnTags(id, "library")["posts"]
    print("allposts being returned")
    print(allposts)
    startingPoint = alltags[0]["id"]
    return render_template('library-dynamic.html',id=startingPoint,tags=alltags, allposts=allposts)

@app.route('/cirp')
def cirp():
    id=102
    alltags = returnTags(id, "cirp")["tags"]
    allposts = returnTags(id, "cirp")["posts"]
    print("allposts being returned")
    print(allposts)
    startingPoint = alltags[0]["id"]
    return render_template('library-dynamic.html',id=startingPoint,tags=alltags, allposts=allposts)


@app.route('/schools')
def schools():
    id=60
    alltags = returnTags(id, "schools")["tags"]
    allposts = returnTags(id, "schools")["posts"]
    print("allposts being returned")
    print(allposts)
    startingPoint = alltags[0]["id"]
    return render_template('library-dynamic.html',id=startingPoint,tags=alltags, allposts=allposts)


@app.route('/chaplaincy')
def chaplaincy():
    id=6
    alltags = returnTags(id, "library")["tags"]
    allposts = returnTags(id, "library")["posts"]
    print("allposts being returned")
    print(allposts)
    startingPoint = alltags[0]["id"]
    return render_template('library-dynamic.html',id=startingPoint,tags=alltags, allposts=allposts)


@app.route('/research')
def research():
    id=69
    alltags = returnTags(id, "research")["tags"]
    allposts = returnTags(id, "research")["posts"]
    print("allposts being returned")
    print(allposts)
    startingPoint = alltags[0]["id"]
    return render_template('library-dynamic.html',id=startingPoint,tags=alltags, allposts=allposts)


@app.route('/corporate')
def corporate():
    id=70
    alltags = returnTags(id, "corporate")["tags"]
    allposts = returnTags(id, "corporate")["posts"]
    print("allposts being returned")
    print(allposts)
    startingPoint = alltags[0]["id"]
    return render_template('library-dynamic.html',id=startingPoint,tags=alltags, allposts=allposts)


# @app.route('/libraryapi')
# def libraryapi():
#     id = 19
#     allposts = returnTags(id, "library")["posts"]

    # # getByCategory=About
    # posts = requests.get(wpUrl+"/posts?categories=19")
    # posts = posts.json()
    # print("posts")
    # allposts = []
    # for p in posts:
    #     categories = p["categories"]
    #     categories.remove(19)
    #     allposts.append({"id":str(categories[0]),
    #                      "title":p["title"]["rendered"],
    #                     "content":p["content"]["rendered"]
    #                     })

    # print("allposts")
    # print(allposts)
        # remove 4

    # print(posts)
    # storeArticlesBy
    # print(response.json())
    # return allposts

    # return render_template('about.html' posts=allposts)


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
    formId = 1
    form=ApplicantForm()
    print(current_user.code)

    userdata = ApplicantInformation.query.filter_by(usercode = current_user.code).first()

    if request.method=='POST':
        if form.validate_on_submit():
            if userdata is not None:
                try:
                    userdata.surname = form.surname.data
                    userdata.userId = current_user.id
                    userdata.usercode = current_user.code
                    userdata.othername = form.othername.data
                    userdata.nationality = form.nationality.data
                    userdata.email = form.email.data
                    userdata.campus = form.campus.data
                    userdata.stream = form.stream.data
                    userdata.date_of_birth = form.dateofbirth.data
                    userdata.phone = form.mobile.data
                    userdata.picture = form.firebaseLink.data
                    userdata.entry_mode = form.entrymode.data
                    userdata.filed = True

                    db.session.commit()
                    return redirect(url_for('applicantPrograms'))

                except Exception as e:
                    print("e")
                    print(e)

            else:
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

                return redirect('applicantPrograms')

        else:
            print(form.errors)
            flash(form.errors.values[0],"danger")
    elif request.method=='GET':

    
        if userdata:
            if userdata.filed == True:
                form.surname.data = userdata.surname
                form.othername.data = userdata.othername 
                form.nationality.data = userdata.nationality
                form.email.data = userdata.email
                form.campus.data = userdata.campus
                form.stream.data = userdata.stream
                form.dateofbirth.data = userdata.date_of_birth
                form.mobile.data = userdata.phone
                form.entrymode.data = userdata.entry_mode
        else:
            pass

    percentage = (formId/totalNumberOfAdmissionForms)*100
    print(percentage)
    return render_template('admissions/applicantInformation.html', metadata=admissionMap[formId],form=form, userdata=userdata)


@app.route('/deleteEducation/<string:id>', methods=['GET', 'POST'])
def deleteEducation(id):
    education = Education.query.get_or_404(id)
    if education is not None:
        try:
            db.session.delete(education)
            db.session.commit()
            flash(f'{education.school} has been deleted')
        except Exception as e:
            print(e)
    return redirect(url_for('applicantEducation'))

@app.route('/applicantEducation', methods=['GET', 'POST'])
def applicantEducation():
    formId=3
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

            flash(f'{newApplicantEducation.school} has been added')
            return redirect(url_for('applicantEducation'))
        else:
            print(form.errors)

    if request.method == 'GET':
        userdata = Education.query.filter_by(usercode = current_user.code).all()
        print(userdata)

    formtitle='Education History'
    formdescription='Include your school history. This is a broad entry. Please be as thorough as possible.'
    percentage = (formId/totalNumberOfAdmissionForms)*100
    print(percentage)
    return render_template('admissions/applicantEducation.html', metadata=admissionMap[formId], userdata=userdata, form=form)

@app.route('/applicantPrograms', methods=['GET', 'POST'])
def applicantPrograms():
    formId=2
    form=ApplicantProgram()
    programs = Programs.query.filter_by(usercode=current_user.code).first()
    # check to see if there is already an entry with this id
    # if not create 3 entries: 1, 2 3
    # this form will be edit only

    if request.method=='POST':
        print("POST FORM!")
        if form.validate_on_submit():
            if programs is not None: 
                try:
                    programs.userId = current_user.id,
                    programs.usercode = current_user.code,
                    programs.program = form.program.data,
                    programs.firstchoice = form.firstchoice.data,
                    programs.secondchoice = form.secondchoice.data,
                    programs.thirdchoice = form.thirdchoice.data,
                    programs.filed = True

                    db.session.commit()
                except Exception as e:
                    reportError(e)

            else:
                print(form.program.data)

                try:
                    newPrograms = Programs(
                    userId = current_user.id,
                    usercode = current_user.code,
                    program = form.program.data,
                    programchoice = form.programchoice.data,
                    firstchoice = form.firstchoice.data,
                    secondchoice = form.secondchoice.data,
                    thirdchoice = form.thirdchoice.data,
                    filed = True
                    )    

                    db.session.add(newPrograms)
                    db.session.commit() 
                except Exception as e:
                    reportError(e)

                return redirect(url_for('applicantEducation'))
        else:
            print(form.errors)
        
        return redirect(url_for('applicantEducation'))

    if request.method == 'GET':
        print("lol")

    formtitle='Education History'
    formdescription='Include your school history. This is a broad entry. Please be as thorough as possible.'
    percentage = (formId/totalNumberOfAdmissionForms)*100
    print(percentage)
    return render_template('admissions/applicantPrograms.html', metadata=admissionMap[formId], form=form)

@app.route('/applicantGuardian', methods=['GET', 'POST'])
def applicantGuardian():
    formId=4
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

    formtitle='Education History'
    formdescription='Include your school history. This is a broad entry. Please be as thorough as possible.'
    percentage = (formId/totalNumberOfAdmissionForms)*100
    print(percentage)
    return render_template('/admissions/applicantGuardian.html', form=form, formtitle=formtitle, formdescription=formdescription, percentage=percentage )

@app.route('/applicantEmployment', methods=['GET', 'POST'])
def applicantEmployment():
    return "Done"

@app.route('/applicantExam', methods=['GET', 'POST'])
def applicantExam():
    formId=3
    form=ApplicantExams()

    if request.method=='POST':
        if form.validate_on_submit:
            print("form.exam.data")

            try:
                exam = Exam(
                    userId = current_user.id,
                    usercode = current_user.code,
                    exam = form.examtype.data,
                    indexNumber = form.indexnumber.data,
                    date = form.exam_date.data,
                    filed = True)
                db.session.add(exam)
                db.session.commit()
                flash(f'{exam.exam} has been added successfully.')
                return redirect(url_for('applicantExam'))

            except Exception as e:
                reportError(e)

        else:
            print(form.errors)
            reportError(form.errors)

    elif request.method == 'GET':
        userdata = Exam.query.filter_by(usercode = current_user.code).all()

        if userdata:
            pass
                # form.exam.data = userdata.exam

    percentage = (formId/totalNumberOfAdmissionForms)*100
    print(percentage)   
    return render_template('admissions/applicantExam.html', form=form, metadata=admissionMap[formId], userdata=userdata)

@app.route('/deleteApplicantExam/<string:id>', methods=['GET', 'POST'])
@login_required
def deleteApplicantExam(id):
    exam = Exam.query.get_or_404(id)
    if exam is not None:
        try:
            db.session.delete(exam)
            db.session.commit()
            flash(f'{exam.school} has been deleted')
        except Exception as e:
            print(e)
    return redirect(url_for('applicantExam'))


@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/applicantExamresult', methods=['GET', 'POST'])
def applicantExamresult():
    formId=6
    form=ApplicantExamresult()
    # check request method
    if request.method=='POST':
        print("postrequest")
        if form.validate_on_submit:
            # ExamResult
            print("formvalidated")
            return redirect(url_for('applicantcontacts'))
        else:
            print(form.errors)
    elif request.method == 'GET':
        print("getrequest")
        userdata = ExamResult.query.filter_by(usercode = current_user.code).first()

        if userdata:
            if userdata.filed == True:
                pass
    # check form validation
    # check errors
    return render_template('applicantExamresult.html', form=form)


@app.route('/applicantcontacts', methods=["GET", "POST"])
def applicantcontacts():
    formId=7
    form=ApplicantContant()

    if request.method=='POST':
        if form.validate_on_submit:
            print(form.contactemail.data)
        else:
            print(form.errors)
        return redirect(url_for('applicantattachments'))

    # check form validation
    # check errors
    return render_template('applicantcontacts.html', form=form)

@app.route('/applicantattachments', methods=['GET', 'POST'])
def applicantattachments():
    formId=8
    form=ApplicantAttachment()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            # print(form.email.data)
            return redirect(url_for('applicantphotos'))
    # check form validation
    # check errors
    return render_template('applicantattachments.html', form=form, userdata={'name':'None','picture':'lol'})

@app.route('/applicantphotos', methods=['GET', 'POST'])
def applicantphotos():
    formId=9
    form=ApplicantPhoto()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            # print(form.email.data)
            return redirect(url_for('applicantanswers'))
    # check form validation
    # check errors
    return render_template('applicantphotos.html', form=form)


@app.route('/applicantanswers', methods=['GET', 'POST'])
def applicantanswers():
    formId=10
    form=ApplicantAnswer()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print("form.email.data")
            return redirect(url_for('applicantrefrees'))
    # check form validation
    # check errors
    return render_template('applicantanswers.html', form=form)

@app.route('/applicantrefrees', methods=['GET', 'POST'])
def applicantrefrees():
    formId=11
    form=ApplicantRefree()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print("form.email.data")
            return redirect(url_for('applicanthalls'))
    # check form validation
    # check errors
    return render_template('applicantrefrees.html', form=form)



@app.route('/applicanthalls', methods=['GET', 'POST'])
def applicanthalls():
    formId=12
    form=ApplicantHall()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print("form.email.data")
            return redirect(url_for('applicantmisinfos'))
    # check form validation
    # check errors
    return render_template('applicanthalls.html', form=form)


@app.route('/applicantmisinfos', methods=['GET', 'POST'])
def applicantmisinfos():
    formId=13
    form=ApplicantMiscellaneousInformation()
    # check request method
    if request.method=='POST':
        if form.validate_on_submit:
            print("form.email.data")
            return "summary"
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
    app.run(port=4000, host='0.0.0.0', debug=True)


