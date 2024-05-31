from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from forms import LoginForm, BlogPostForm, ProjectForm
from app.models import User, Project, BlogPost
from extensions import db

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

@main_routes.route('/dashboard/add_blog_post', methods=['GET', 'POST'])
def add_blog_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        title = request.form.get('title')
        content = request.form.get('content')

        new_blog_post = BlogPost(title=title, content=content)

        db.session.add(new_blog_post)
        db.session.commit()

        flash('Blog post added successfully!', 'success')
        return redirect(url_for('main.blog'))

    # Render the form template
    return render_template('add_blog_post.html', form=form) 

@main_routes.route('/dashboard/add_project', methods=['GET', 'POST'])
def add_project():
    form = ProjectForm()
    if form.validate_on_submit():
        title = request.form.get('title')
        description = request.form.get('description')
        technologies = request.form.get('technologies')
        link = request.form.get('link')

        new_project = Project(title=title, description=description, technologies=technologies, link=link)

        db.session.add(new_project)
        db.session.commit()

        flash('Blog post added successfully!', 'success')
        return redirect(url_for('main.projects'))

    # Render the form template
    flash('Error', 'success')
    return render_template('add_project.html', form=form) 
