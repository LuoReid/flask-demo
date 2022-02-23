
from flask import Flask, escape, url_for, render_template

app = Flask(__name__)

name = 'Grey Li'
movies = [
    {'title': 'My Neighbor Totoro', 'year': '1988'},
    {'title': 'Dead Poets Society', 'year': '1989'},
    {'title': 'A Perfect World', 'year': '1993'},
    {'title': 'WALL-E', 'year': '2008'},
]


@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)


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


if __name__ == "__main__":
    app.run(debug=True, port=5000)
