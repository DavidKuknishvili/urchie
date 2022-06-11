# db
from werkzeug import exceptions
import sqlite3
from flask_sqlalchemy import SQLAlchemy


# date
from datetime import datetime

# flask
from flask import Flask, redirect, url_for, render_template, request, session, flash

# image
from io import BytesIO
from flask import send_file

# password hash
from passlib.hash import sha256_crypt


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
    author_id = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f"{self.id},{self.author},{self.title},{self.description},{self.category},{self.upload_date},{self.post_image},{self.author_id}"




class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)
    comment_author_id = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f"{self.post_id}%${self.comment}%${self.comment_author_id}"


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    post_id = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

    def __str__(self):
        return f"{self.id}%${self.post_id}%${self.user_id}"



def publishing_date(date):
    post_date_min = datetime.now().minute - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').minute

    post_date_hour = datetime.now().hour - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').hour

    post_date_day = datetime.now().day - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').day

    post_date_month = datetime.now().month - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').month

    post_date_year = datetime.now().year - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').year

    # post_date = str(datetime.now().year - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').year) + 'წლის'

    if post_date_year != 0:
        post_date = str(
            abs(datetime.now().year - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').year)) + ' წელის წინ '
    elif post_date_month != 0 and post_date_year == 0:
        post_date = str(
            abs(datetime.now().month - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').month)) + ' თვის წინ'
    elif post_date_day != 0 and post_date_month == 0:
        post_date = str(
            abs(datetime.now().day - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').day)) + ' დღის წინ'
    elif post_date_hour != 0 and post_date_day == 0:
        post_date = str(
            abs(datetime.now().hour - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').hour)) + ' საათის წინ'
    elif post_date_min != 0 and post_date_hour == 0:
        post_date = str(
            abs(datetime.now().minute - datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f').minute)) + ' წუთის წინ'
    else:
        post_date = 'ახლახანს'

    return post_date


def set_post_data(category):


    post_info = Posts.query.filter_by(category=category).all()



    post_list = []

    for each in post_info:
        post_id = each.id

        title = each.title
        author_id = each.author_id


        comment_count=0
        commnet_info = Comments.query.filter_by(post_id= post_id).all()
        for i in commnet_info:
            comment_count += 1

        date = str(each.upload_date)
        post_date = publishing_date(date)


        image_url = f'/category/image/{post_id}'

        info = (title, post_date, comment_count, image_url, post_id, author_id)
        post_list.append(info)
    post_list.reverse()

    return post_list


def popular_posts():
    con = sqlite3.connect('urchie.sqlite3')
    cursor = con.cursor()
    cursor.execute("SELECT title, author_id, id  FROM posts ")
    post = cursor.fetchall()

    popular_posts_list = []

    for each in post:
        title = each[0]
        author_id = each[1]
        id = each[2]
        cursor.execute(f'select count(post_id) from comments where post_id = {id}')
        comment_count = cursor.fetchone()[0]

        post_tuple = (title, author_id, id, comment_count)

        popular_posts_list.append(post_tuple)

    def sorter(elem):
        return elem[3]

    popular_posts_list.sort(key=sorter, reverse=True)

    return popular_posts_list[:4]


def last_post():


    post_info = Posts.query.all()
    ls = []
    for each in post_info:
        id=each.id
        title=each.title
        category=each.category
        upload_date= str(each.upload_date)

        tuplle = (id, title, category, upload_date)
        ls.append(tuplle)

    ls.reverse()
    list_post = ls[0]

    return list_post

def general_posts():


    post_info = Posts.query.all()

    general_post_list = []
    for each in post_info:
        id = each.id
        author_id = each.author_id
        title = each.title
        category = each.category
        date = str(each.upload_date)
        upload_date = publishing_date(date)
        general_tuple = (id, author_id, title, category, upload_date)
        general_post_list.append(general_tuple)
    general_post_list.reverse()

    return general_post_list


def profile_post(id):


    posts = Posts.query.filter_by(author_id=id).all()

    general_post_list = []

    for each in posts:
        id = each.id
        author_id = each.author_id
        title = each.title
        category = each.category
        date = str(each.upload_date)
        upload_date = publishing_date(date)
        general_tuple = (id, author_id, title, category, upload_date)
        general_post_list.append(general_tuple)



    general_post_list.reverse()

    return general_post_list



def favorite_posts(user_id):


    favorite_post = Favorite.query.filter_by(user_id=user_id).all()


    favorite_post_list = []

    for i in favorite_post:


        post = Posts.query.filter_by(id=i.post_id).all()

        comment_count = 0

        for each in post:
            id = each.id
            author_id = each.author_id
            title = each.title
            # date = str(each.upload_date)


            comment_info = Comments.query.filter_by(post_id=id).all()

            for i in comment_info:
                comment_count += 1

            general_tuple = (title, author_id, id, comment_count)
            favorite_post_list.append(general_tuple)

    favorite_post_list.reverse()
    print(favorite_post_list)
    return favorite_post_list



def hash_password(password):
    return sha256_crypt.hash(password)


def verify_password(password, password_hash):
    return sha256_crypt.verify(password, password_hash)






@app.route('/', methods=['GET', 'POST'])
def home():
    if 'user' in session:

        if request.method == 'GET':

            if request.args.get('search') is not None:
                search_sentence = request.args.get('search')
                return redirect(url_for('search', keyword=f'{search_sentence}'))

            category_type = request.args.get('category')
            # post_info = Posts.query.filter_by(category=category).all()
            #
            # print(category_type)

            if category_type == 'გართობა':
                return render_template('category.html', info=set_post_data(category_type), fun_color='category_bn' )
            elif category_type == 'პროგრამირება':
                return render_template('category.html', info=set_post_data(category_type), prog_color='category_bn')
            elif category_type == 'მუსიკა':
                return render_template('category.html', info=set_post_data(category_type), mus_color='category_bn')
            elif category_type == 'ურთიერთობები':
                return render_template('category.html', info=set_post_data(category_type), rel_color='category_bn')
            elif category_type == 'კულინარია':
                return render_template('category.html', info=set_post_data(category_type), cul_color='category_bn')
            elif category_type == 'სპორტი':
                return render_template('category.html', info=set_post_data(category_type), sport_color='category_bn')
            elif category_type == 'ხელოვნება':
                return render_template('category.html', info=set_post_data(category_type), art_color='category_bn')
            elif category_type == 'მეცნიერება':
                return render_template('category.html', info=set_post_data(category_type), science_color='category_bn')
            elif category_type == 'პოლიტიკა':
                return render_template('category.html', info=set_post_data(category_type), pol_color='category_bn')
            elif category_type == 'ზოგადი':
                return redirect(url_for('home'))

        return render_template('index.html', category=category_type, popular_posts=popular_posts(),
                               title=last_post()[1],
                               category_last_post=last_post()[2], upload_date=publishing_date(last_post()[3]),
                               last_post_id=last_post()[0], general_posts=general_posts())

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
            users = Users.query.filter_by(e_mail=e_mail).first()

            if not users:

                return render_template('login.html', mail_error='register_error')
            else:

                print(users.e_mail, users.password)
                if not verify_password(password, users.password) and e_mail == users.e_mail:

                    return render_template('login.html', password_error='register_error')

                else:
                    session['user'] = e_mail
                    return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        first_name = request.form['firstName']
        last_name = request.form['lastName']
        age = request.form['age']
        e_mail = request.form['email']
        password = request.form['password']
        again_password = request.form['again_password']
        user_image = request.files['image']
        users = Users.query.filter_by(e_mail=e_mail).all()
        print(type(user_image))
        if users != []:
            return render_template('registration.html', mail_error='register_error')
        elif password != again_password or len(password) < 8:
            return render_template('registration.html', password_error='register_error')
        elif first_name == "":

            return render_template('registration.html', firstname_error='register_error')
        elif last_name == '':
            return render_template('registration.html', lastname_error='register_error')

        elif len(age) == 0:
            return render_template('registration.html', age_error='register_error')

        elif user_image.filename == '':
            return render_template('registration.html', image_error='img_error')
        else:
            password_hash = hash_password(password)
            user = Users(first_name=first_name, last_name=last_name, age=age, e_mail=e_mail, password=password_hash,
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

        if request.args.get('search') is not None:
            search_sentence = request.args.get('search')
            return redirect(url_for('search', keyword=f'{search_sentence}'))

        post_obj = Posts.query.filter_by(id=id).all()
        comment_obj = Comments.query.filter_by(post_id=id).all()
        user_obj = Users.query.filter_by(e_mail=str(session['user'])).all()

        comment_list = []

        for each_post in post_obj:
            post_title = each_post.title
            post_description = each_post.description
            post_category = each_post.category
            post_upload_date = str(each_post.upload_date)
            date = publishing_date(post_upload_date)

        for each_user in user_obj:
            user_id = each_user.id

        if request.method == 'POST':
            comment = request.form['comment']
            # print(comment)

            if comment != '':
                Comments_obj = Comments(comment=comment, comment_author_id=user_id, post_id=id)
                db.session.add(Comments_obj)
                db.session.commit()
                return redirect(url_for('open', id=id))
            else:
                flash("*რჩევის ველი ცარიელია", "error")

        for each_comment in comment_obj:
            comment = each_comment.comment
            comment_author_id = each_comment.comment_author_id
            comment_tuple = (comment, comment_author_id)
            comment_list.append(comment_tuple)

        comment_list.reverse()
        # print(comment_list)

        post = Favorite.query.filter_by(post_id=id, user_id=user_id).first()
        if not post:
            fill = "#ababab"

        else:
            fill = '#0094FF'

        if request.args.get('save') == 'save':
            post = Favorite.query.filter_by(post_id=id, user_id=user_id).first()
            if not post:
                fill = '#0094FF'
                favorite_obj = Favorite(post_id=id, user_id=user_id)
                db.session.add(favorite_obj)
                db.session.commit()

            else:
                fill = "#ababab"
                Favorite.query.filter_by(post_id=id, user_id=user_id).delete()
                db.session.commit()
            print(id)
            return  redirect(url_for('open', id=id))


        return render_template('open.html', title=post_title, description=post_description, time=date,
                               category=post_category, id=id, comments=comment_list, save_bn_color= fill)

    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' in session:

        if request.args.get('search') is not None:
            search_sentence = request.args.get('search')
            return redirect(url_for('search', keyword=f'{search_sentence}'))

        user_mail = str(session['user'])

        user_info = Users.query.filter_by(e_mail=user_mail).all()

        for each in user_info:
            first_name = each.first_name
            last_name = each.last_name
            user_id = each.id

        user_name = first_name + " " + last_name

        posts = profile_post(user_id)[:3]
        posts_count = "all_post"
        posts_value = "მეტი პოსტის ჩვენება"

        if request.args.get('post_sort') == 'all_post':

            posts = profile_post(user_id)
            posts_count = "less_post"
            posts_value = "ნაკლები პოსტის ჩვენება"
        else:
            posts = profile_post(user_id)[:3]


        return render_template('profile.html', user_name=user_name, user_id=user_id, profile_post=posts, post_count=posts_count, profile_posts=posts_value, favorite=favorite_posts(user_id))

    else:
        return redirect(url_for('home'))


@app.route('/profile/image/<int:id>')
def set_image(id):
    if 'user' in session:

        user_info = Users.query.filter_by(id=id).first()
        image_bytes = user_info.user_image
        bytes_io = BytesIO(image_bytes)
        return send_file(bytes_io, mimetype='image/jpeg')
    else:
        return redirect(url_for('home'))

@app.route('/add', methods=['GET', 'POST'])
def add():
    if 'user' in session:
        if request.args.get('search') is not None:
            search_sentence = request.args.get('search')
            return redirect(url_for('search', keyword=f'{search_sentence}'))

        if request.method == 'POST':
            title = request.form['add_title']
            description = request.form['add_description']
            category = request.form['add_category']
            post_image = request.files['add_image']
            today_date = datetime.now()

            if title == '' or description == '' or category == '' or post_image.filename == '':
                flash('*ყველა ველის შევსება აუცილებელია', 'error')
            else:

                author = str(session['user'])

                author_id = Users.query.filter_by(e_mail=author).first().id

                post = Posts(author=author, title=title, description=description, category=category,
                             upload_date=today_date,
                             post_image=post_image.read(), author_id=author_id)
                db.session.add(post)
                db.session.commit()

                return redirect(url_for('home'))
        return render_template('add.html')

    else:
        return redirect(url_for('home'))

@app.route("/category/image/<int:id>")
def category(id):
    if 'user' in session:


        result = Posts.query.filter_by(id=id).first()
        image_bytes = result.post_image
        bytes_io = BytesIO(image_bytes)
        return send_file(bytes_io, mimetype='image/jpeg')
    else:
        return redirect(url_for('home'))


@app.route('/search/<keyword>', methods=['GET', 'POST'])
def search(keyword):
    if 'user' in session:

        if request.method == 'GET':
            if request.args.get('search') is not None:
                search_sentence = request.args.get('search')
                return redirect(url_for('search', keyword=f'{search_sentence}'))


            search_data_list = []


            search_data = Posts.query.filter(Posts.title.like(f"%{keyword}%")).all()

            for each in search_data:
                title = each.title
                author_id = each.author_id
                id = each.id

                comment_count = 0
                commnet_info = Comments.query.filter_by(post_id=id).all()
                for i in commnet_info:
                    comment_count += 1

                search_tuple = (title, author_id, id, comment_count)

                search_data_list.append(search_tuple)

            return render_template('search.html', search=search_data_list)

        return render_template('search.html')

    return redirect(url_for('home'))



@app.route('/profilePage/<int:id>')
def profile_guest(id):
    if 'user' in session:

        if request.args.get('search') is not None:
            search_sentence = request.args.get('search')
            return redirect(url_for('search', keyword=f'{search_sentence}'))

        user_info = Users.query.filter_by(id=id).all()

        for each in user_info:
            first_name = each.first_name
            last_name = each.last_name
            user_id = each.id

        user_name = first_name + " " + last_name

        return render_template('profile.html', user_name=user_name, user_id=user_id, profile_post=profile_post(id))

    else:
        return redirect(url_for('home'))



@app.route('/settings/<int:id>', methods=['GET','POST'])
def settings(id):
    if 'user' in session:
        email = str(session['user'])
        if Users.query.filter_by(id=id).first().e_mail == email:

            info = Users.query.filter_by(id=id).first()

            if request.args.get('menu') == 'personal-info':
                if request.method == 'POST':
                    firstName = request.form['firstName']
                    lastName = request.form['lastName']
                    user_age = request.form['age']

                    if firstName == '' and lastName == '':

                        info.age = user_age
                        db.session.commit()
                        flash('*ონაცემები შენახულია', 'info')
                    elif lastName == '' and len(str(user_age)) == 0:

                        info.first_name = firstName

                        db.session.commit()
                        flash('*მონაცემები შენახულია', 'info')
                    elif len(str(user_age)) == 0 or firstName == '':

                        info.last_name = lastName
                        db.session.commit()
                        flash('*მონაცემები შენახულია', 'info')

                    elif lastName == '':
                        info.first_name = firstName
                        info.age = user_age
                        db.session.commit()

                        flash('*მონაცემები შენახულია', 'info')
                    elif firstName == '':
                        info.last_name = lastName
                        info.age = user_age
                        db.session.commit()

                        flash('*მონაცემები შენახულია', 'info')
                    elif len(str(user_age)) == 0:
                        info.last_name = lastName
                        info.first_name = firstName
                        db.session.commit()

                        flash('*მონაცემები შენახულია', 'info')
                    else:
                        info.first_name = firstName
                        info.last_name = lastName
                        info.age = user_age
                        db.session.commit()

                        flash('*მონაცემები შენახულია', 'info')

                return render_template('personal_info.html')
            elif request.args.get('menu') == 'security':

                if request.method == 'POST':
                    old_pass = request.form['oldPass']
                    new_pass = request.form['newPass']
                    confirm_pass = request.form['confirmPass']

                    if not sha256_crypt.verify(old_pass, info.password):
                        print(old_pass, info.password)
                        flash('*ძველი პაროლი არ არის სწორე', 'error')
                    elif new_pass != confirm_pass:
                        flash('*ახალი პაროლები არ ემთხვევა ერთმანეთს', 'error')
                    elif new_pass == old_pass:
                        flash('*ახალი და ძველი პაროლები ემთხვევა ერთმანეთს', 'error')
                    else:
                        info.password = hash_password(new_pass)
                        db.session.commit()
                        flash('*მონაცემები წარმატებით შეიცვალა', 'info')

                return render_template('security.html')
            elif request.args.get('menu') == 'appearance':
                if request.method == 'POST':
                    new_profile_pic = request.files['save_img']

                    if new_profile_pic.filename == '':
                        flash("ფოტო არ არის არჩეული", 'error')
                    else:
                        info.user_image = new_profile_pic.read()
                        db.session.commit()
                        flash("პროფილის ფოტო წარმატებით შეიცვალა", 'info')

            elif request.args.get('menu') == 'home':
                return redirect(url_for('home'))

            return render_template('appearance.html')
        else:
            return redirect(url_for('home'))
    else:
        return redirect(url_for('home'))

@app.route('/otherProfile/<int:id>')
def otherProfile(id):
    if 'user' in session:
        mail = str(session['user'])
        info = Users.query.filter_by(e_mail=mail).first()
        if info.id == id:
            return redirect(url_for('profile'))
        else:
            if request.args.get('search') is not None:
                search_sentence = request.args.get('search')
                return redirect(url_for('search', keyword=f'{search_sentence}'))



            user_info = Users.query.filter_by(id=id).all()

            for each in user_info:
                first_name = each.first_name
                last_name = each.last_name
                user_id = each.id

            user_name = first_name + " " + last_name

            posts = profile_post(user_id)[:3]
            posts_count = "all_post"
            posts_value = "მეტი პოსტის ჩვენება"

            if request.args.get('post_sort') == 'all_post':

                posts = profile_post(user_id)
                posts_count = "less_post"
                posts_value = "ნაკლები პოსტის ჩვენება"
            else:
                posts = profile_post(user_id)[:3]


            return render_template('other_profile.html', user_name=user_name, user_id=user_id, profile_post=posts, post_count=posts_count, profile_posts=posts_value)

    else:
        return redirect(url_for('home'))


@app.errorhandler(exceptions.NotFound)
def not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
