from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'URCHIE_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urchie.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    first_name = db.Column(db.String, primary_key=True, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    e_mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_image = db.Column(db.LargeBinary, nullable=False)

    def __str__(self):
        return f"{self.first_name},{self.last_name},{self.age},{self.e_mail},{self.password}"
        # return (self.first_name, self.last_name, self.e_mail, self.age, self.password)



@app.route('/')
def home():

    if 'user' in session:
        return render_template('index.html')
    else:
        return render_template('first.html')




@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user' in session:
        return redirect(url_for('home'))
    else:

        if request.method == 'POST':
            e_mail = request.form['email_login']
            password = request.form['password_login']
            users = Users.query.filter_by(e_mail= e_mail).all()


            for each in users:
                if e_mail == str(each).split(',')[3] and password == str(each).split(',')[4]:
                    session['user'] = e_mail
                    return redirect(url_for('home'))
                else:
                    return render_template('login.html')


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

        user = Users(first_name=first_name, last_name=last_name, age=age, e_mail=e_mail, password=password,
                     user_image=user_image.read())
        db.session.add(user)
        db.session.commit()

        session['user'] = e_mail
        return redirect(url_for('home'))

        # print(f"first_name:{first_name}; last_name:{last_name}; age:{age}; e_mail:{e_mail}; password:{password}")

    return render_template('registration.html')


@app.route('/open')
def open():
    return render_template('open.html')

@app.route('/logout')
def logout():

    session.pop('user', None)
    return redirect(url_for('home'))



@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/add')
def add():
    if 'user' in session:
        return render_template('add.html')
    else:
        return redirect(url_for('home'))


# just a comment


if __name__ == '__main__':
    app.run(debug=True)
