from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:lc101@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(1200))

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/")
def index():
    print(db)
    template = jinja_env.get_template('blog.html')
    return template.render()

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

if __name__ == '__main__':
    app.run()