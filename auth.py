from flask import redirect,render_template,Blueprint,request,url_for,flash
from Email import send_email
from werkzeug.security import generate_password_hash
from flask_login import current_user
from config import Configuration
from Model import User
from app import create_app
 


TEMPLATES_FOLDER='templates/forms'

#This the blueprint for email related routes.
email = Blueprint('email',__name__,template_folder=TEMPLATES_FOLDER)


 
#Forget password GET route
@email.route('/forget-password')
def forget_password():
    return render_template('forgetpassword.html',title='forget Password') 


#Forget password POST route
@email.route('/forget-password',methods=['POST'])
def forget_password_post():
         
        email = request.form.get('email')
        

        user=User.find_user_by_email(email=email)
       
      
        if user:
                token=user.get_reset_password_token(600)
                
                send_email('Pheme Account Reset',
                sender=Configuration.MAIL_DEFAULT_SENDER,recipients=[user.email],
                text_body=render_template('/reset_password.txt',user=user,token=token),
                html_body= render_template('/message.html',title='Email',user=user,token=token))
                return redirect(url_for('admin.login_admin'))
                 
                
        else:
                flash('Wrong email address')
                return redirect(url_for('email.forget_password'))
        

 #Reset user password POST route
@email.route('/new-password',methods=['POST'])
def reset_password():
       password=request.form.get('password')

       confirm_password=request.form.get('confirm_password')
       token=request.form.get('token')
       user=User.verify_reset_password_token(token)
       if user and password== confirm_password:
               user.password=generate_password_hash(password,method="sha256",salt_length=8)
               user.save_data
               flash('Password reset was successful')
      

       return redirect(url_for('admin.login_admin'))


#Reset user password GET  route
@email.route('/new-password/<token>',methods=['GET'])
def reset_password_post(token):
        user = User.verify_reset_password_token(token)
        if user:
                return render_template('newpassword.html',token=token)     
        else:
                flash('Invalid token')
                return redirect(url_for('admin.login_admin'))
 
        return redirect(url_for('email.reset_password'))

 #This route is used  to confirm a user.
 # It checks if a user'email is valid
 # it then checks the confirmation status of the user
 # if the user is not confirmed
 # it sets the confirmed field to true 
 # by performing a database update query
 #        
 
@email.route('/login/<token>',methods=['GET'])
def confirm_user(token):
        user=User.verify_reset_password_token(token)
        print(token)
        print(user)
        if user:
                return redirect(url_for('admin.login_admin',token=token)) 
        else:
                #send user a confirmation email to confirmed account.
                send_email('Pheme Confirmation Email', sender=Configuration.MAIL_DEFAULT_SENDER,recipients=[user.email],
                text_body=render_template('/confirm.txt',title ='Account Confirmation Email',user=user,token=token),
                html_body= render_template('/confirm.html',title='Account Confirmation Email',user=user,token=token))
                flash('Confirmation expired,Another confirmation message has been sent to your email address')
                return redirect(url_for('admin.login_admin'))
                 





    



