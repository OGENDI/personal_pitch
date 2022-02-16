from flask import render_template
from . import auth
from flask import render_template,redirect,url_for
from ..models import User
from .forms import RegistrationForm
from .. import db
from flask import flash,request # flash helps us display error messages to the user
from flask_login import login_user, current_user
from .forms import  LoginForm
from flask_login import login_required,logout_user
from ..email import mail_message



@auth.route('/login',methods=['GET','POST'])
def login():
    login_form = LoginForm() # We create an instance of LoginForm
    if login_form.validate_on_submit():
        user = User.query.filter_by(email = login_form.email.data).first()
        if user is not None and user.verify_password(login_form.password.data):
            login_user(user,login_form.remember.data)
            return redirect(request.args.get('next') or url_for('root.index'))

        flash('Invalid username or Password')

    title = "Pitchers login"
    return render_template('auth/login.html',login_form = login_form,title=title)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("root.index"))



@auth.route('/register',methods = ["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        
        mail_message("Welcome to Pitchers Hub","email/welcome_user",user.email,user=user)
        
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html',registration_form = form)
