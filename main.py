from flask import Blueprint,render_template,url_for,request,flash,redirect
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user,login_required,current_user
from Email import mail,send_email
from config import Configuration
from flask_mail import Message
from Model import User


TEMPLATES_FOLDER='templates/forms' 

#Blue print for authenication related routes.
admin=Blueprint('admin',__name__,template_folder=TEMPLATES_FOLDER)

#Template used by admin to login
@admin.route('/')
@admin.route('/login')
def login_admin():
    
    return render_template('login.html',title='Login')


@admin.route('/login',methods=['POST'])
def login_admin_post():
     email=request.form.get('email')
     password=request.form.get('password')
     token =request.form.get('token')
     remember = True if request.form.get('remember') else False
     user=User.find_user_by_email(email=email)
    
     user1=User.verify_reset_password_token(token)
     print(user1)
     if user1:
         user1.is_confirmed=True
         user1.save_data
 
     if user and check_password_hash(user.password,password):
         login_user(user,remember=remember,force=True)
         return redirect(url_for('admin.show_dashboard'))
     else:
         flash('Please check your login details and try again')
         return redirect(url_for('admin.signup_admin'))

     

#Template used by admin to signup
@admin.route('/signup')
def signup_admin():
    return render_template('/signup.html',title='Admin Signup') 

@admin.route('/signup',methods=['POST']) 
def signup_admin_post():
    email = request.form.get('email')
    username = request.form.get('username')
    password=request.form.get('password')
    user=User.find_user_by_email(email=email)
    
    if user:
        flash('Email address already exist')
       
        return redirect(url_for('admin.login_admin'))
    #fetching user data from the login form
    new_user= User(username,email,password)
    new_user.save_data 
    token=new_user.get_reset_password_token(600)
    #send user a confirmation email to confirmed account.
    send_email('Pheme Confirmation Email', sender=Configuration.MAIL_DEFAULT_SENDER,recipients=[new_user.email],
                text_body=render_template('/confirm.txt',title ='Account Confirmation Email',user=new_user,token=token),
                html_body= render_template('/confirm.html',title='Account Confirmation Email',user=new_user,token=token))
    flash('Check your signup mail to confirmation your account!')
    return redirect(url_for('admin.login_admin'))


#Application daashboard route
@admin.route('/dashboard')
@login_required
def show_dashboard():
    return render_template('/dashboard.html',title='Dashboard')


