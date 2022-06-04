# db
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# date
from datetime import datetime

# flask
from flask import Flask, redirect, url_for, render_template, request, session

# image
from io import BytesIO
from flask import send_file


app = Flask(__name__)

app.config['SECRET_KEY'] = 'URCHIE_KEY'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urchie.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    e_mail = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    user_image = db.Column(db.LargeBinary, nullable=False)

    def __str__(self):
        return f"{self.id},{self.first_name},{self.last_name},{self.age},{self.e_mail},{self.password}"
        # return (self.first_name, self.last_name, self.e_mail, self.age, self.password)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    author = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False)
    post_image = db.Column(db.LargeBinary, nullable=False)

    def __str__(self):
        return f"{self.id},{self.author},{self.title},{self.description},{self.category},{self.upload_date},{self.post_image}"




class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)
    comment_author_id = db.Column(db.Integer, nullable=False)


    def __str__(self):
        return f"{self.post_id}%${self.comment}%${self.comment_author_id}"




def set_post_data(category):
    con = sqlite3.connect('urchie.sqlite3')
    cursor = con.cursor()
    cursor.execute(f"SELECT id, title,upload_date,category FROM posts where category='{category}'")
    post_info = cursor.fetchall()

    # print(post_info)

    post_list = []

    for each in post_info:
        post_id = each[0]

        title = each[1]

        if len(title) > 315:
            title = title[:315] + '...'

        date = each[2]


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


        image_url = f'/category/image/{post_id}'

        info = (title, post_date, category, image_url,post_id )
        post_list.append(info)


    return post_list


@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' in session:
        if request.method == 'GET':
            category_type = request.args.get('category')
            # post_info = Posts.query.filter_by(category=category).all()
            #
            print(category_type)

            if category_type == 'გართობა':
                return render_template('category.html', info=set_post_data(category_type))
            elif category_type == 'პროგრამირება':
                return render_template('category.html', info=set_post_data(category_type))
            elif category_type == 'მუსიკა':
                return render_template('category.html', info=set_post_data(category_type))
            elif category_type == 'ურთიერთობები':
                return render_template('category.html', info=set_post_data(category_type))
            elif category_type == 'კულინარია':
                return render_template('category.html', info=set_post_data(category_type))
            elif category_type == 'სპორტი':
                return render_template('category.html', info=set_post_data(category_type))
            elif category_type == 'ხელოვნება':
                return render_template('category.html', info=set_post_data(category_type))
            elif category_type == 'მეცნიერება':
                return render_template('category.html', info=set_post_data(category_type))
            elif category_type == 'პოლიტიკა':
                return render_template('category.html', info=set_post_data(category_type))
            elif category_type == 'ზოგადი':
                return redirect(url_for('home'))

        return render_template('index.html', category=category_type)

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
                if e_mail == str(each).split(',')[4] and password == str(each).split(',')[5]:
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


@app.route('/open/<int:id>', methods=['GET', 'POST'])
def open(id):

    if 'user' in session:

        post_obj = Posts.query.filter_by(id=id).all()
        comment_obj = Comments.query.filter_by(post_id=id).all()
        user_obj = Users.query.filter_by(e_mail=str(session['user'])).all()

        comment_list = []


        for each_post in post_obj:
            post_title = str(each_post).split(',')[2]
            post_description = str(each_post).split(',')[3]
            post_category = str(each_post).split(',')[4]
            post_upload_date = str(each_post).split(',')[5]

        for each_user in user_obj:
            user_id = str(each_user).split(',')[0]

        if request.method == 'POST':
            comment = request.form['comment']
            print(comment)

            Comments_obj = Comments(comment=comment, comment_author_id=user_id, post_id=id)
            db.session.add(Comments_obj)
            db.session.commit()
            return redirect(url_for('open',id=id))

        for each_comment in comment_obj:

            comment = str(each_comment).split('%$')[1]
            comment_author_id = str(each_comment).split('%$')[2]
            comment_tuple = (comment, comment_author_id)
            comment_list.append(comment_tuple)

        comment_list.reverse()
        print(comment_list)
        return render_template('open.html', title=post_title, description=post_description, time=post_upload_date, category=post_category, id=id, comments=comment_list)


    return redirect(url_for('home'))





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
            first_name = str(each).split(',')[1]
            last_name = str(each).split(',')[2]
            user_id = str(each).split(',')[0]

        user_name = first_name + " " + last_name

        return render_template('profile.html', user_name=user_name ,user_id=user_id)

    else:
        return redirect(url_for('home'))


@app.route('/profile/image/<id>')
def set_image(id):
    if 'user' in session:
        con = sqlite3.connect('urchie.sqlite3')
        cursor = con.cursor()
        cursor.execute(f"SELECT user_image FROM users where id={id}")
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



@app.route("/category/image/<id>")
def category(id):

    if 'user' in session:

        con = sqlite3.connect('urchie.sqlite3')
        cursor = con.cursor()
        cursor.execute(f"SELECT post_image FROM posts where id={id}")
        result = cursor.fetchone()
        image_bytes = result[0]
        bytes_io = BytesIO(image_bytes)
        return send_file(bytes_io, mimetype='image/jpeg')
    else:
        return redirect(url_for('home'))

@app.route('/search/<keyword>')
def search(keyword):
    return render_template('search.html')

if __name__ == '__main__':
    app.run(debug=True)
