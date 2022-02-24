from flask import Flask, escape, redirect, request, url_for, render_template, flash
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user, login_required

from watchlist import app,db
from watchlist.models import User,Movie


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))

        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)
            flash('Login success.')
            return redirect(url_for('index'))
        flash('Invalid username or password.')
        return redirect(url_for('login'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Goodbye.')
    return redirect(url_for('index'))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please login first')
            return redirect(url_for('index'))
        # print('form:', request.form)
        title = request.form.get('title')
        year = request.form.get('year')
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('index'))
        mn = Movie(title=title, year=year)
        db.session.add(mn)
        db.session.commit()
        flash('Item created.')
        return redirect(url_for('index'))
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)


@app.route('/movies/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit(id):
    movie = Movie.query.get_or_404(id) 
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) != 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', id=id))
        movie.title = title
        movie.year = year
        db.session.commit()
        flash('Item updated.')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)


@app.route('/movies/<int:id>/delete', methods=['POST'])
@login_required
def delete(id):
    movie = Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    flash('Item deleted.')
    return redirect(url_for('index'))


@app.route('/home')
def hello():
    return 'Welcome to my watchlist.'


@app.route('/user/<name>')
def user_page(name):
    return 'Welcome {}:)'.format(escape(name))


@app.route('/test')
def test_url_for():
    print(url_for('hello'))
    print(url_for('user_page', name='Didi'))
    print(url_for('test_url_for', num=2))
    return 'Test page'


@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        db.session.commit()
        flash('Settings updated.')
        return redirect(url_for('index'))
    return render_template('settings.html')