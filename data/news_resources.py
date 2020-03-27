from flask_restful import reqparse, abort, Resource
from data.users import User
from data.news import News
from flask import jsonify

db_session = None

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('user_id', required=True, type=int)


class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify({'news': news.to_dict(
            only=('title', 'content', 'user_id', 'is_private'))})

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': 'OK'})

class NewsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return jsonify({'news': [item.to_dict(
            only=('title', 'content', 'user.name')) for item in news]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = News(title=args['title'],
            content=args['content'], user_id=args['user_id']
        )
        session.add(news)
        session.commit()
        return jsonify({'success': 'OK'})

def abort_if_news_not_found(news_id):
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        if not news:
            abort(404, message=f"News {news_id} not found")

def connect_db(db):
    global db_session
    db_session = db