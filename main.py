from flask import Flask, render_template, redirect
from data import db_session
from data.users import User
from data.news import News
from Forms.registration import RegisterForm
from Forms.login import LoginForm
from flask_login import LoginManager, login_required, login_user, current_user, logout_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
	session = db_session.create_session()
	return session.query(User).get(user_id)

@app.route("/")
def index():
	session = db_session.create_session()
	if current_user.is_authenticated:
		news = session.query(News).filter((News.user == current_user) | (News.is_private != True))
	else:
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

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		session = db_session.create_session()
		user = session.query(User).filter(User.email == form.email.data).first()
		if user and user.check_password(form.password.data):
			login_user(user, remember=form.remember_me.data)
			return redirect("/")
		return render_template('login.html',
							   message="Неправильный логин или пароль",
							   form=form)
	return render_template('login.html', title='Авторизация', form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect("/")

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