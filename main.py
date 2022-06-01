import sqlite3
from datetime import datetime

from flask import Flask, redirect, url_for, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO
from flask import send_file

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


class Posts(db.Model):
    author = db.Column(db.String, primary_key=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    post_image = db.Column(db.LargeBinary, nullable=False)

    def __str__(self):
        return f"{self.author},{self.title},{self.description},{self.category},{self.upload_date},{self.post_image}"


def set_post_data(category):
    con = sqlite3.connect('urchie.sqlite3')
    cursor = con.cursor()
    cursor.execute(f"SELECT title,upload_date,category FROM posts where category='{category}'")
    post_info = cursor.fetchall()

    # print(post_info)

    post_list = []

    for each in post_info:

        title = each[0]
        # if len(title) > 1:
        #     title = title[0] + '...'
        date = each[1]
        # print(title)
        # print(date)

        post_date_min = datetime.now().minute - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').minute

        post_date_hour = datetime.now().hour - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').hour

        post_date_day = datetime.now().day - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').day

        post_date_month = datetime.now().month - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').month

        post_date_year = datetime.now().year - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').year

        # post_date = str(datetime.now().year - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').year) + 'წლის'

        if post_date_min != 0 and post_date_hour == 0:
            post_date = str(
                datetime.now().minute - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').minute) + ' წუთის'

        elif post_date_hour != 0 and post_date_day == 0:
            post_date = str(
                datetime.now().hour - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').hour) + ' საათის'

        elif post_date_day != 0 and post_date_month == 0:
            post_date = str(
                datetime.now().day - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').day) + ' დღის'

        elif post_date_month != 0 and post_date_year == 0:
            post_date = str(
                datetime.now().month - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').month) + ' თვის'

        else:
            post_date = str(
                datetime.now().year - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').year) + ' წელის'

        # post_date = f'{post_date_min} {post_date_hour} {post_date_day}, {post_date_month}, {post_date_year} '
        info = (title, post_date, category)
        post_list.append(info)


    return post_list


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' in session:
        if request.method == 'POST':
            category = request.form['category']
            # post_info = Posts.query.filter_by(category=category).all()
            #
            # print(post_info)

            # con = sqlite3.connect('urchie.sqlite3')
            # cursor = con.cursor()

            if category == 'გართობა':
                # set_post_data(category)
                return render_template('category.html', info=set_post_data(category))
                # cursor.execute(f"SELECT title,upload_date,category FROM posts where category='{category}'")
                # post_info = cursor.fetchall()
                #
                # # print(post_info)
                #
                # post_list = []
                #
                # for each in post_info:
                #
                #     title = each[0]
                #     # if len(title) > 1:
                #     #     title = title[0] + '...'
                #     date = each[1]
                #     # print(title)
                #     # print(date)
                #
                #     post_date_min = datetime.now().minute - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').minute
                #
                #     post_date_hour = datetime.now().hour - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').hour
                #
                #     post_date_day = datetime.now().day - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').day
                #
                #     post_date_month = datetime.now().month - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').month
                #
                #     post_date_year = datetime.now().year - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').year
                #
                #     # post_date = str(datetime.now().year - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').year) + 'წლის'
                #
                #     if post_date_min != 0 and post_date_hour == 0:
                #         post_date = str(
                #             datetime.now().minute - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').minute) + ' წუთის'
                #
                #     elif post_date_hour != 0 and post_date_day == 0:
                #         post_date = str(
                #             datetime.now().hour - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').hour) + ' საათის'
                #
                #     elif post_date_day != 0 and post_date_month == 0:
                #         post_date = str(
                #             datetime.now().day - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').day) + ' დღის'
                #
                #     elif post_date_month != 0 and post_date_year == 0:
                #         post_date = str(
                #             datetime.now().month - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').month) + ' თვის'
                #
                #     else:
                #         post_date = str(
                #             datetime.now().year - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').year) + ' წელის'
                #
                #     # post_date = f'{post_date_min} {post_date_hour} {post_date_day}, {post_date_month}, {post_date_year} '
                #     info = (title, post_date, category)
                #     post_list.append(info)
                # print(post_list)

                #
                # user_mail = str(session['user'])
                # con = sqlite3.connect('urchie.sqlite3')
                # cursor = con.cursor()
                # cursor.execute(f"SELECT user_image FROM users where e_mail='{user_mail}'")
                # result = cursor.fetchone()
                # image_bytes = result[0]
                # bytes_io = BytesIO(image_bytes)


            elif category == 'პროგრამირება':
                return render_template('category.html', info=set_post_data(category))
            elif category == 'მუსიკა':
                return render_template('category.html', info=set_post_data(category))
            elif category == 'ურთიერთობები':
                return render_template('category.html', info=set_post_data(category))
            elif category == 'კულინარია':
                return render_template('category.html', info=set_post_data(category))
            elif category == 'სპორტი':
                return render_template('category.html', info=set_post_data(category))
            elif category == 'ხელოვნება':
                return render_template('category.html', info=set_post_data(category))
            elif category == 'მეცნიერება':
                return render_template('category.html', info=set_post_data(category))
            elif category == 'პოლიტიკა':
                return render_template('category.html', info=set_post_data(category))
            elif category == 'ზოგადი':
                return render_template('category.html', info=set_post_data(category))

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
            users = Users.query.filter_by(e_mail=e_mail).all()

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
    if 'user' in session:
        user_mail = str(session['user'])

        user_info = Users.query.filter_by(e_mail=user_mail).all()

        for each in user_info:
            first_name = str(each).split(',')[0]
            last_name = str(each).split(',')[1]

        user_name = first_name + " " + last_name

        return render_template('profile.html', user_name=user_name)

    else:
        return redirect(url_for('home'))


@app.route('/profile/image')
def set_image():
    if 'user' in session:
        user_mail = str(session['user'])
        con = sqlite3.connect('urchie.sqlite3')
        cursor = con.cursor()
        cursor.execute(f"SELECT user_image FROM users where e_mail='{user_mail}'")
        result = cursor.fetchone()
        image_bytes = result[0]
        bytes_io = BytesIO(image_bytes)
        return send_file(bytes_io, mimetype='image/jpeg')
    else:
        return redirect(url_for('home'))


@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user' in session:
        if request.method == 'POST':
            title = request.form['add_title']
            description = request.form['add_description']
            category = request.form['add_category']
            post_image = request.files['add_image']
            today_date = datetime.now()

            author = str(session['user'])

            post = Posts(author=author, title=title, description=description, category=category, upload_date=today_date,
                         post_image=post_image.read())
            db.session.add(post)
            db.session.commit()

            return redirect(url_for('home'))
        return render_template('add.html')

    else:
        return redirect(url_for('home'))


# #
# @app.route("/category=<CATEGORY>")
# def category(CATEGORY):
#
#     return render_template('category.html')


if __name__ == '__main__':
    app.run(debug=True)
