from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SECRET_KEY'] = 'URCHIE_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urchie.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


class users(db.Model):
    first_name = db.Column(db.String, primary_key=True, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    e_mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_image = db.Column(db.LargeBinary, nullable=False)

    def __str__(self):
        return f"first_name:{self.first_name}; last_name:{self.last_name}; age:{self.age}; e_mail:{self.e_mail}; password:{self.password};"


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        age = request.form['age']
        e_mail = request.form['email']
        password = request.form['password']
        user_image = request.files['image']

        user = users(first_name=first_name, last_name=last_name, age=age, e_mail=e_mail, password=password,
                     user_image=user_image.read())
        db.session.add(user)
        db.session.commit()
        return render_template('index.html')

        print( f"first_name:{first_name}; last_name:{last_name}; age:{age}; e_mail:{e_mail}; password:{password}")

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


# just a comment


if __name__ == '__main__':
    app.run(debug=True)
