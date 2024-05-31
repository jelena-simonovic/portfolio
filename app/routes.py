from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from forms import LoginForm
from app.models import User, Project, BlogPost


main_routes = Blueprint('main', __name__)

@main_routes.route('/')
def home():
    title = "Hi, I'm Jelena!"
    return render_template('home.html', title=title)

@main_routes.route('/projects')
def projects():
    title = 'My Projects'
    all_projects = Project.query.all()
    return render_template('projects.html', projects=all_projects, title=title)

@main_routes.route('/blog')
def blog():
    title = 'Blog'
    posts = BlogPost.query.order_by(BlogPost.date_posted.desc()).all()
    return render_template('blog.html', posts=posts, title=title)

@main_routes.route('/contact')
def contact():
    title = 'Contact'
    return render_template('contact.html', title=title)

@main_routes.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)

@main_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.login'))

@main_routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')