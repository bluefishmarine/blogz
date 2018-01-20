from flask import Flask, request, redirect, render_template, session,flash
from flask_sqlalchemy import SQLAlchemy
# from models import db, Blog, User

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:werto5678@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = "sjfh576b929%&#fj"

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, user):
        self.title = title
        self.body = body
        self.owner = user

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))
    blogs = db.relationship("Blog", backref="owner")

    def __init__(self,email,password):
        self.email = email
        self.password = password



@app.route('/')
def index():
    return render_template('home.html')

@app.route("/register",methods=['GET',"POST"])
def register(): 
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form['password']
        verify = request.form["passwordv"]    
        existing_user = User.query.filter_by(email=email).first()        
        #todo - validate user data

        if not existing_user:
            new_user = User(email,password)    
            db.session.add(new_user)
            db.session.commit()
            # Remember User
            return redirect("/")
        else:
            #todo - use better response
            return "<h1>Duplicate User</h1>"

    return render_template("register.html")

@app.route("/login", methods=['GET','POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()
        if user and user.password == password: 
            session['email'] = email
            flash("Logged in") 
            return redirect("/")
        else:
            #Why Login failed
            flash("Username or password incorrect", 'error')

    return render_template("login.html")

@app.route("/logout")
def logout():
    del session["email"]
    return redirect("/")


@app.route('/blog', methods = ['GET'])
def blog():
    if request.args:
        id = int(request.args.get("id"))   
        blog = Blog.query.filter_by(id = id).first()
        print (blog)
        return render_template("article.html", blog=blog)

    blogs = Blog.query.all()
    return render_template('blogs.html',blogs = blogs)

@app.route("/new", methods=['GET','POST'])
def new_post():

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        post = Blog(title,body)
        db.session.add(post)
        db.session.commit()
        id = post.id    
        return redirect("/blog?id={0}".format(id))

    return render_template('new.html')

if __name__ == '__main__':
    app.run()