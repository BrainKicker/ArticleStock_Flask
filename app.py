from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Article (db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	intro = db.Column(db.String(300), nullable=False)
	text = db.Column(db.Text, nullable=False)
	date = db.Column(db.DateTime, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True, default=None)

	def __repr__(self):
		return '<Article %r>' % self.id


class User (db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(), nullable=False)
	password = db.Column(db.String(), nullable=False)

	def __repr__(self):
		return '<User %r>' % self.id


with app.app_context():
	db.create_all()


@app.route('/')
@app.route('/home')
def index():
	return render_template('index.html')


@app.route('/about')
def about():
	return render_template('about.html')


@app.route('/sign-in', methods=['GET', 'POST'])
def sign_in():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		# TODO
		return "TODO"
	else:
		return render_template('sign-in.html')


@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		# TODO
		return "TODO"
	else:
		return render_template('sign-up.html')


@app.route('/articles')
def articles():
	articles = Article.query.order_by(Article.date.desc()).all()
	return render_template('articles.html', articles=articles)


@app.route('/article/<int:article_id>')
def article(article_id):
	article = Article.query.get_or_404(article_id)
	return render_template('article.html', article=article)


@app.route('/article/<int:article_id>/delete')
def article_delete(article_id):
	article = Article.query.get_or_404(article_id)
	try:
		db.session.delete(article)
		db.session.commit()
		return redirect('/articles')
	except:
		return 'При удалении статьи произошла ошибка'


@app.route('/article/<int:article_id>/update', methods=['GET', 'POST'])
def article_update(article_id):
	article = Article.query.get_or_404(article_id)
	if request.method == 'POST':
		article.title = request.form['title']
		article.intro = request.form['intro']
		article.text = request.form['text']
		try:
			db.session.commit()
			return redirect('/articles')
		except:
			return 'При редактировании статьи произошла ошибка'
	else:
		return render_template('update-article.html', article=article)


@app.route('/create-article', methods=['GET', 'POST'])
def create_article():
	if request.method == 'POST':
		title = request.form['title']
		intro = request.form['intro']
		text = request.form['text']
		article = Article(title=title, intro=intro, text=text)
		try:
			db.session.add(article)
			db.session.commit()
			return redirect('/articles')
		except:
			return 'При добавлении статьи произошла ошибка'
	else:
		return render_template('create-article.html')


if __name__ == '__main__':
	app.run(debug=True)