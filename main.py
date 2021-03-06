from flask import Flask, request, redirect, render_template, session,flash
from flask_sqlalchemy import SQLAlchemy
from validator import Validator
from hash import make_pw_hash, check_pw_hash


app = Flask(__name__)

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:werto5678@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
# db = SQLAlchemy(app)
app.secret_key = "sjfh576b929%&#fj"

from models import db, Blog, User, Comment


@app.route('/')
def index():
    users = User.query.all()
    return render_template('home.html',users=users)

@app.route("/register",methods=['GET',"POST"])
def register(): 
    validator = Validator()
    if request.method == 'POST':
        name = request.form["name"]
        password = request.form['password']
        verify = request.form["passwordv"]    
        existing_user = User.query.filter_by(email=name).first()        
        #todo - validate user data
        validator.validate_input(name,password,verify)
        if validator.errors["contains_error"]:
            return render_template("register.html", name=name, errors=validator.errors)


        if not existing_user:
            new_user = User(name,make_pw_hash(password))    
            db.session.add(new_user)
            db.session.commit()
            # Remember User
            session['name'] = name
            session['id'] = new_user.id
            return redirect("/new")
        else:
            #todo - use better response
            flash("User already exists")
            return redirect("/register")

    return render_template("register.html",errors=validator.errors)

@app.before_request
def require_login():
    not_allowed_routes = ['new','addComment','edit']
    if request.endpoint in not_allowed_routes and "name" not in session:
        return redirect('/login')
    if request.endpoint in not_allowed_routes:
        if request.args and request.args.get('id'):
            id = request.args.get('id')
            blog_user = (Blog.query.filter_by(id = id).first()).owner.email
            if not(blog_user == session['name']):
                return ("You do not have permission to do that")
              
        

@app.route("/login", methods=['GET','POST'])
def login():

    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = User.query.filter_by(email = name).first()
        if user and user.password == make_pw_hash(password): 
            session['name'] = name
            session['id'] = user.id
            flash("Logged in") 
            return redirect("/new")
        else:
            #Why Login failed
            flash("Username or password incorrect", 'error')
            return redirect("/login")

    return render_template("login.html")

@app.route("/logout")
def logout():
    del session["name"]
    del session['id'] 
    return redirect("/blog")


@app.route('/blog', methods = ['GET'])
def blog():
    if request.args:
        if request.args.get("id"):
            id = int(request.args.get("id"))   
            blog = Blog.query.filter_by(id = id).first()
            comments = Comment.query.filter_by(blog_id = id).all()
            return render_template("article.html", blog=blog,comments = comments)
        userID = int(request.args.get("user"))
        user = User.query.filter_by(id = userID).first()
        blogs = Blog.query.filter_by(user_id = userID,active=True).all()
        return render_template("userposts.html", blogs=blogs, user=user)     
    blogs = Blog.query.filter_by(active=True).all()
    return render_template('blogs.html',blogs = blogs)

@app.route('/edit', methods = ['GET','POST'])
def edit():
    name = session['name']
    user = User.query.filter_by(email = name).first()
    blog_id = request.args.get('id')
    blog = Blog.query.filter_by(id = blog_id).first()
    if request.method == 'POST':
        blogID = request.form['blogid']
        blog = Blog.query.filter_by(id = blogID).first()
        title = request.form['title']
        body = request.form['body']
        blog.title = title
        blog.body = body
        db.session.commit()   
        return redirect("/blog?id={0}".format(blogID))
    return render_template('edit.html',blog=blog)

@app.route('/deletePost', methods = ['POST'])
def deletePost():
    name = session['name']
    user = User.query.filter_by(email = name).first()
    blog_id = request.form['blogid']
    blog = Blog.query.filter_by(id = blog_id).first()
    blog.active = False
    db.session.commit()
    return redirect("/blog?user={0}".format(user.id))

@app.route('/addComment', methods = ['POST'])
def addComment():
    name = session['name']
    user = User.query.filter_by(email = name).first()
    blog_id = request.form['blogid']
    blog = Blog.query.filter_by(id = blog_id).first()
    content = request.form['body']
    newComment = Comment(content,user,blog)
    db.session.add(newComment)
    db.session.commit()
    return redirect("/blog?id={0}".format(blog_id))

@app.route("/new", methods=['GET','POST'])
def new_post():

    name = session['name']
    user = User.query.filter_by(email = name).first()

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        post = Blog(title,body,user)
        db.session.add(post)
        db.session.commit()
        id = post.id    
        return redirect("/blog?id={0}".format(id))

    return render_template('new.html')


if __name__ == '__main__':
    app.run()