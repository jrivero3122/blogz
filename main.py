from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:lc101@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    email = db.Column(db.String(40))
    password = db.Column(db.String(20))
    tasks = db.relationship('Blog', backref='owner')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

@app.route("/")
def index():
    blogs = Blog.query.order_by(Blog.id).all()
    template = jinja_env.get_template('blog.html')
    return template.render(blogs = blogs)

@app.route("/newpost", methods=['POST', 'GET'])
def newpost():
    error1=""
    if request.method == 'POST':
        title = request.form['blogTitle']
        body = request.form['blogText']
        if title and body:
            newBlog = Blog(title, body)
            db.session.add(newBlog)
            db.session.commit()
            return redirect('/')
        else:
            error1 = "Please write Title and Text"
    template = jinja_env.get_template('newpost.html')
    return template.render(error1=error1)

@app.route("/blog")
def blog():
    blog = Blog.query.filter_by(id=request.args['id']).first()
    print(blog)
    template = jinja_env.get_template('article.html')
    return template.render(blog = blog)

@app.route("/login", methods=['POST', 'GET'])
def login():
    template = jinja_env.get_template('login.html')
    return template.render()


@app.route("/register", methods=['POST', 'GET'])
def register():
    if request.method == 'GET':
        template = jinja_env.get_template('register.html')
        return template.render()
    else:
        username = request.form['username']
        password = request.form['password']
        verifyPassword = request.form['verifyPassword']
        email = request.form['email']
        # template = jinja_env.get_template('signup.html')
        # return template.render(username = username)
        if username and password and verifyPassword:
            if (len(username)<20 and len(username)>3 and (' ' in username) == False) and (len(password)<20 and len(password)>3 and (' ' in password) == False) and (len(verifyPassword)<20 and len(verifyPassword)>3 and (' ' in verifyPassword) == False):
                if password == verifyPassword:
                    if email:
                        if ((' ' in email) == False) and (len(email)<80 and len(email)>3) and (email.count("@") == 1) and (email.count(".") == 1):
                            newUser = User(username, email, password)
                            db.session.add(newUser)
                            db.session.commit()
                            template = jinja_env.get_template('newpost.html')
                            warning1 = ""
                        else:
                            template = jinja_env.get_template('index.html') 
                            warning1 = "Email not valid"
                    else:    
                        newUser = User(username, email, password)
                        db.session.add(newUser)
                        db.session.commit()
                        template = jinja_env.get_template('newpost.html')
                        warning1 = ""
                else:
                    template = jinja_env.get_template('index.html') 
                    warning1 = "The user's password and password-confirmation do not match"
            else:
                template = jinja_env.get_template('index.html') 
                warning1 = "Username or Password, would be invalid"
        else:
            template = jinja_env.get_template('index.html') 
            warning1 = "Fields empty"
                    
        
        return template.render(name=username, warning1=warning1, email=email)

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    return redirect(url_for('newpost'))


if __name__ == '__main__':
    app.run()