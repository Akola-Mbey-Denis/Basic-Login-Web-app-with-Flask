import os
 
class Configuration(object):
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    SQLALCHEMY_DATABASE_URI="postgresql://denis:1997@localhost:5432/task"
   
    SECRET_KEY='xfqfq1283428o1bbhmasvaggffaf22211xxzxzz'
    DEBUB=False
    TESTING=False
    MAIL_SUPPRESS_SEND = False
    #Mail settings
    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=True
    MAIL_USERNAME='nforticsinterns@gmail.com'
    MAIL_PASSWORD='interns2019'
    MAIL_DEFAULT_SENDER='nforticsinterns@gmail.com'

 