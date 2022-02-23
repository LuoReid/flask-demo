from unicodedata import name
from flask import Flask,escape, url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Welcome, Flasker:)<h1>Hello Totoro:)</h1><img src="http://helloflask.com/totoro.gif">'

@app.route('/home')
def hello():
  return 'Welcome to my watchlist.'

@app.route('/user/<name>')
def user_page(name):
  return 'Welcome {}:)'.format(escape(name))

@app.route('/test')
def test_url_for():
  print(url_for('hello'))
  print(url_for('user_page',name='Didi'))
  print(url_for('test_url_for',num=2))
  return 'Test page'

if __name__ == "__main__":
    app.run(debug=True, port=5000)
