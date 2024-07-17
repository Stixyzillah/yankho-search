from flask import render_template, url_for, flash, redirect, request
from flask_login import login_user, current_user, logout_user, login_required
from . import db
from .models import User, Contact
from .forms import RegistrationForm, LoginForm, ContactForm

@app.route('/')
@app.route('/home')
def home():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_admin:
        flash('You do not have access to this page', 'danger')
        return redirect(url_for('home'))
    users = User.query.all()
    contacts = Contact.query.all()
    return render_template('dashboard.html', title='Dashboard', users=users, contacts=contacts)

@app.route('/add_contact', methods=['GET', 'POST'])
@login_required
def add_contact():
    form = ContactForm()
    if form.validate_on_submit():
        contact = Contact(
            name=form.name.data, business=form.business.data, address=form.address.data,
            region=form.region.data, district=form.district.data, services=form.services.data,
            map_url=form.map_url.data, image_url=form.image_url.data, owner=current_user
        )
        db.session.add(contact)
        db.session.commit()
        flash('Your contact has been added!', 'success')
        return redirect(url_for('home'))
    return render_template('add_contact.html', title='Add Contact', form=form)

@app.route('/search')
def search():
    region = request.args.get('region')
    district = request.args.get('district')
    service = request.args.get('service')
    query = Contact.query
    if region:
        query = query.filter_by(region=region)
    if district:
        query = query.filter_by(district=district)
    if service:
        query = query.filter(Contact.services.like(f'%{service}%'))
    contacts = query.all()
    return render_template('search.html', title='Search Results', contacts=contacts)
