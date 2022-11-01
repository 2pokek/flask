from flask import Flask, render_template, current_app, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Article

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.sqlite3.db'

db.init_app(app)


@app.route('/')
@app.route('/home')
def index():
    return render_template("user.html")


@app.route('/create')
def create():
    db.create_all()
    return 'all tables created'


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by(Article.date.desc()).all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post(id):
    article = Article.query.get(id)
    return render_template("post.html", article=article)

@app.route('/posts/<int:id>/delete')
def post_delete(id):
    article = Article.query.get_or_404(id)

    try:
        db.session.delete(article)
        db.session.commit()
        return redirect('/posts')
    except:
        return "Error while deleting"
    return render_template("post.html", article=article)


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def post_update(id):
    article= Article.query.get(id)
    if request.method == "POST":
        article.title = request.form['title']
        article.nickname = request.form['nickname']
        article.intro = request.form['intro']
        article.text = request.form['text']


        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Error, try again later'
    else:
        article = Article.query.get(id)
        return render_template("post_update.html", article=article)

@app.route('/create-article', methods=['POST', 'GET'])
def create_artical():
    if request.method == "POST":
        title = request.form['title']
        nickname = request.form['nickname']
        intro = request.form['intro']
        text = request.form['text']

        article = Article(title=title, nickname=nickname, intro=intro, text=text)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Error, try again later'
    else:
        return render_template("create-article.html")


if __name__ == '__main__':
    app.run(debug=True)
