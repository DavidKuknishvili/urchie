from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registration')
def registration():
    return render_template('registration.html')


@app.route('/open')
def open():
    return render_template('open.html')


@app.route('/first')
def first():
    return render_template('first.html')


@app.route('/add')
def add():
    return render_template('add.html')


#just a comment



if __name__ == '__main__':
    app.run(debug=True)
