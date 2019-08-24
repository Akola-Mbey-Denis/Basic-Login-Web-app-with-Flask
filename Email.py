from flask_mail import Mail,Message
mail = Mail()
 #Template used by the admin to reset password
# send forget_password email 
def send_email(subject, sender, recipients,html_body,text_body):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html=html_body
    mail.send(msg)
