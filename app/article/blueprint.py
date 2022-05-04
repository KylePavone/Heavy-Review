from flask import Blueprint, render_template, url_for, request, redirect, flash
from flask_login import current_user
from models import Articles, Themes, User, db, Commentaries
from .forms import CommentForm
from time import sleep

articles = Blueprint('article', __name__, template_folder='templates')



@articles.route('/titles')
def main_articles():
    q = request.args.get('q')

    page = request.args.get('page')
    if page and page.isdigit():
        page = int(page)
    else:
        page = 1

    if q:
        articles = Articles.query.filter(Articles.title.contains(q) | Articles.subtitle.contains(q))
    else:
        articles = Articles.query.order_by(Articles.created.desc())

    pages = articles.paginate(page=page, per_page=2)
    return render_template('article/articles.html', articles=articles, pages=pages)


@articles.route('/<slug>', methods=['GET', 'POST'])
def current_article(slug):
    user = current_user
    article = Articles.query.filter(Articles.slug == slug).first()
    themes = article.themes
    commentaries = article.comments
    if request.method == 'POST':
        if current_user.is_authenticated:
            commentary = request.form['commentary']
            try:
                comm = Commentaries(content=commentary)
                db.session.add(comm)
                article.comments.append(comm)
                user.comments.append(comm)
                db.session.commit()
                #return redirect(url_for('/article.current_article'))
            except:
                print("Something Wrong!")
        else:
            if request.method == 'POST':
                return render_template('article/need_login.html')
    form = CommentForm()
    return render_template('article/current_article.html', themes=themes, article=article,
                           commentaries=commentaries, form=form)


@articles.route('/theme/<slug>')
def associated_articles(slug):
    theme = Themes.query.filter(Themes.slug == slug).first()
    articles = theme.articles.all()
    return render_template('article/associated_articles.html', theme=theme, articles=articles)


@articles.route('/themes')
def themes():
    themes = Themes.query.all()
    return render_template('article/themes.html', themes=themes)


@articles.route('/latest')
def latest():
    articles = Articles.query.order_by(Articles.created.desc())[0:3]
    return render_template('article/latest.html', articles=articles)
