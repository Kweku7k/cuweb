from flask import Flask,redirect,url_for,render_template,request, send_from_directory, current_app
import os

app=Flask(__name__)
@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('index.html')

app.config['UPLOAD_FOLDER']='Documents'


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

@app.route('/posts')
def posts():
    return render_template('posts.html')

@app.route('/students')
def students():
    return render_template('students.html')

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(port=5000,debug=True)


