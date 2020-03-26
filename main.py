from flask import Flask
from data import db_session
from data.users import User
from data.news import News

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route("/")
def index():
    session = db_session.create_session()
    news = session.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)


def main():
	db_session.global_init("db/blogs.sqlite")
	#for i in range(346):
	#	addNews(f"News {i}", f"Content news {i}", i+1, False)

	app.run()

def addUser(name, about, email):
	user = User()
	user.name = name
	user.about = about
	user.email = email
	session = db_session.create_session()
	session.add(user)
	session.commit()

def addNews(title, content, user_id, is_private):
	news = News(title=title, content=content, 
            user_id=user_id, is_private=is_private)
	session = db_session.create_session()
	session.add(news)
	session.commit()


if __name__ == '__main__':
    main()