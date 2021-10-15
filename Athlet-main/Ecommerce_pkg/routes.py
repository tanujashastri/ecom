from flask_login.mixins import UserMixin
from Ecommerce_pkg import app, db, bcrypt
from Ecommerce_pkg.forms import RegistrationForm, LoginForm ,UpdateAccountForm
from flask import render_template ,url_for ,flash , redirect , request, session
from Ecommerce_pkg.models import User
from flask_login import login_user, current_user , logout_user , login_required

# pep8

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/product")
def product():
    return render_template('product.html')

@app.route("/singleproduct")
def singleproduct():
    return render_template('singleproduct.html')


@app.route("/register",methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}','succes')
        return redirect(url_for('login'))
    return render_template('register.html',title = 'Register', form = form)


@app.route("/login",methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            print(next_page)
            return redirect(next_page) if next_page else redirect(url_for('home')) 
    return render_template('login.html',title = 'Login', form = form)


@app.route('/index',methods=['GET','POST'])
def index():
    return render_template('index.html')


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.usernsessioname = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('account details updated succesfully')
        return redirect(url_for('account'))
    elif request.method =='GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    # image_file = url_for('static',filename = 'images/featured/' + current_user)
    return render_template('account.html', form = form)