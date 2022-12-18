from flask import Flask,redirect,url_for,render_template,request

app=Flask(__name__)
@app.route('/home',methods=['GET','POST'])
def home():
    return render_template('index.html')

@app.route('/')
def online():
    return render_template('online.html', title="Online Application Form.")

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


