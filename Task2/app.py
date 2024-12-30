from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('query.html')


@app.route("/search/<q>")
def search(q):
    return render_template('search.html', query = q)

if __name__ == '__main__':
    app.run (debug = True, use_reloader = True)