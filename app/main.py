from app import app, db
from article.blueprint import articles
import view


app.register_blueprint(articles, url_prefix='/main')


if __name__ == '__main__':
    app.run()
