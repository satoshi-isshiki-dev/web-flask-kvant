from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///news.db'
db = SQLAlchemy(app)
api = Api(app)

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    image_url = db.Column(db.String(100), nullable=True)

class NewsList(Resource):
    def get(self):
        news = News.query.all()
        return [{'id': n.id, 'title': n.title, 'content': n.content, 'author': n.author, 'date': n.date, 'image_url': n.image_url} for n in news]

    def post(self):
        data = request.get_json()
        news = News(title=data['title'], content=data['content'], author=data['author'], date=data['date'], image_url=data['image_url'])
        db.session.add(news)
        db.session.commit()
        return {'id': news.id, 'title': news.title, 'content': news.content, 'author': news.author, 'date': news.date, 'image_url': news.image_url}

class NewsItem(Resource):
    def get(self, news_id):
        news = News.query.filter_by(id=news_id).first()
        if news:
            return {'id': news.id, 'title': news.title, 'content': news.content, 'author': news.author, 'date': news.date}
        else:
            return {'error': 'News not found'}, 404

    def put(self, news_id):
        news = News.query.filter_by(id=news_id).first()
        if news:
            data = request.get_json()
            news.title = data['title']
            news.content = data['content']
            news.author = data['author']
            news.date = data['date']
            db.session.commit()
            return {'id': news.id, 'title': news.title, 'content': news.content, 'author': news.author, 'date': news.date}
        else:
            return {'error': 'News not found'}, 404

    def delete(self, news_id):
        news = News.query.filter_by(id=news_id).first()
        if news:
            db.session.delete(news)
            db.session.commit()
            return {'message': 'News deleted'}
        else:
            return {'error': 'News not found'}, 404
        
api.add_resource(NewsList, '/news')
api.add_resource(NewsItem, '/news/<int:news_id>')