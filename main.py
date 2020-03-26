from flask import Flask, render_template
from data import db_session
from data.users import User
from data.news import News
from Forms.registration import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

@app.route("/")
def index():
    session = db_session.create_session()
    news = session.query(News).filter(News.is_private != True)
    return render_template("index.html", news=news)

@app.route('/register', methods=['GET', 'POST'])
def reqister():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        session = db_session.create_session()
        if session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        user = User(
            name=form.name.data,
            email=form.email.data,
            about=form.about.data
        )
        user.set_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


def main():
	db_session.global_init("db/blogs.sqlite")
	#for i in range(346):
	#	addNews(f"News {i}", f"Content news {i}", i+1, False)

	app.run(port=8080, host='127.0.0.1')

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