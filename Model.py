from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import Column,ForeignKey,String,Integer,TEXT,create_engine,Boolean,DateTime,VARCHAR,update
from sqlalchemy.sql import func
import jwt
from config import Configuration
from time import time,timezone
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask_migrate import Migrate
from sqlalchemy.orm import relationship 

#sqlachemy database instance
db =SQLAlchemy()

#This is the base class for the  the database model classes
class BaseModel(db.Model,UserMixin):
    ''''
    This is the Base model and the inherits from the UserMixin and Model Class
    '''
    __abstract__=True
    @property
    def save_data(self):
        '''
        INPUT: null
        OUTPUT :null
        Task: It commits new data entries to the database 

        '''
        db.create_all(bind='__all__')
        db.session.add(self)
        db.session.commit()
         




    @classmethod
    def return_all_users(cls):
        '''
        Input: none
        Task: fetches all data stored in the database
        output: it returns the data from the database as a json file
        '''
        return list(map(lambda x:x.to_json(),cls.query.all()))
   
    @classmethod
    def return_all_users_raw(cls):
        '''
        Input: none
        Task: fetches all data stored in the database
        output: it returns the data from the database as a json file
        '''
        return cls.query.all()




class User(BaseModel):
    ''''
    This class models the data of a user
    It provide columns to store the 
    user's name, hashed password,date user was created and updated
    the confirmation state of the user
    the account/company the user belongs to

    '''
    __tablename__= 'Users'
    id=db.Column(db.Integer,primary_key=True)
    #username field
    username=db.Column(db.String(200),nullable=False,unique=True) 
    #email field
    email=db.Column(db.String(100),nullable=False,unique=True)
    #password field
    password= db.Column(db.String,nullable=False)
    #status field 'active' or inactive
    status =db.Column(db.VARCHAR(20),nullable=False,default='Active')
    #user confirmation status
    is_confirmed =db.Column(db.Boolean,nullable=True,default=False)

    date_created=db.Column(db.DateTime(timezone=True),default=datetime.utcnow(), nullable=False)
    date_updated=db.Column(db.DateTime(timezone=True), nullable=True)
    #Relationship,every user belong to an account
    account_id=db.Column(db.Integer,ForeignKey('Accounts.id',ondelete='RESTRICT'),default=3)

   
    
    def __init__(self,username,email,password):
        ''' The constructor method  takes the username,email,and password
         '''
        self.username=username
        self.password= generate_password_hash(password,method='sha256',salt_length=8)
        self.email=email
        

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False
    #class getter methods
    @property
    def getConfirmationStatus(self):
        return self.is_confirmed
    

    @classmethod
    def find_user_by_username(cls,username):
        """
        input: a username
        It checks if the user is in the database
        """
        return cls.query.filter_by(username=username).first()

    
    def get_reset_password_token(self,expires_in=600):
        return jwt.encode(
            {
                'reset_password':self.id,'exp':time()+expires_in},
                Configuration.SECRET_KEY,algorithm='HS256').decode('utf-8')


    @staticmethod
    def verify_reset_password_token(token):
        try:
            id=jwt.decode(token,Configuration.SECRET_KEY,algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

        


    

    




    @classmethod
    def find_user_by_email(cls,email):
        '''
        Input: Email address
        It checks if that email already exist in the database
        '''
        return cls.query.filter_by(email=email).first()
 
    

    @classmethod
    def delete_user(cls,username):
        '''
        Deletes the specified user from the database
        '''
        return cls.query.filter_by(username=username).delete()


    @classmethod
    def  return_all_users(cls):
        '''
        It returns a jonsify list of all users in the database
        '''
        def to_json(data):
            return dict(email=data.email,username=data.username, password=data.password,date_created=data.date_created)
        return dict(users=list(map(lambda x: to_json(x), User.query.all())))

    #setter methods for the class
    
    @classmethod
    def set_user_confirmation(cls,email):
        'It sets the confirmation status of  a user'
        user=User.find_user_by_email(email=email)
        if user:
            user.is_confirmed=True
            user.date_updated=datetime.utcnow()
            user.save_data
  
     
#table for account table
class Account(BaseModel,UserMixin):
    __tablename__='Accounts'
    id= db.Column(db.Integer,primary_key=True)
    name=db.Column(db.VARCHAR(100),nullable=False,unique=True)
    date_created=db.Column(db.DateTime( timezone=True),default=datetime.utcnow(),nullable=False)
    date_updated =db.Column(db.DateTime(timezone=True),onupdate=datetime.utcnow(),nullable=True)
     
    def __init__(self,name):
        self.name=name

    @classmethod
    def find_account_by_name(cls,name):
        '''
        Input: account name e.g Nfortics-Ghana,Nfortics-Nigeria
        Task: it searches the database and  returns the  the account if such as account exist
        '''
        return cls.query.filter_by(name=name).first()
    @classmethod
    def  return_all_users(cls):
        '''
        It returns a jonsify list of all accuns in the database
        '''
        def to_json(data):
            return dict( name=data.name)
        return dict(accounts=list(map(lambda x: to_json(x), Account.query.all())))
 


#project database table
class Project(BaseModel,UserMixin):
    __tablename__='Projects'
    id =db.Column(db.Integer,primary_key=True)
    name=db.Column(db.VARCHAR,nullable=False)
    project_creator=db.Column(db.Integer,ForeignKey('Users.id', ondelete='RESTRICT'), nullable=False)#foreign key from the user table
    date_created=db.Column(db.DateTime (timezone=True),default=datetime.utcnow(),nullable=False)
    date_updated=db.Column(db.DateTime(timezone=True),  onupdate=datetime.utcnow,nullable=True)
    
    project_owner=db.Column(db.Integer,ForeignKey('Accounts.id',ondelete='RESTRICT'),nullable=True)#foreign key is  from account table
    
    def __init__(self,project_name):
        self.name= project_name
  
    @classmethod
    def find_project_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def  return_all_users(cls):
        '''
        It returns a jonsify list of all accuns in the database
        '''
        def to_json(data):
            return dict( name=data.name)
        return dict(Project=list(map(lambda x: to_json(x), Project.query.all())))
 



#task clsss
class Task(BaseModel):
    __tablename__='tasks'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.VARCHAR,nullable=False)
    description=db.Column(db.TEXT,nullable=False)
    task_creator=db.Column(db.Integer,ForeignKey('Users.id'),nullable=False)# foreign key from  the user model
    task_assigned =db.Column (db.Integer,ForeignKey('Users.id'),nullable=False) #foreign key from the usermodel
    project_task_belong= db.Column(db.Integer,ForeignKey('Projects.id',ondelete='RESTRICT'),nullable=False) # foreign key from the project model
    date_created=db.Column(db.DateTime (timezone=True),default=datetime.utcnow(),nullable=False)
    date_updated=db.Column(db.DateTime(timezone=True),  onupdate=datetime.utcnow,nullable=True)


    def __init__(self,name,description):
        self.name=name
        self.description=description
    

    @classmethod
    def find_task_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def  return_all_users(cls):
        '''
        It returns a jonsify list of all accuns in the database
        '''
        def to_json(data):
            return dict( name=data.name,description=data.description)
        return dict(Task=list(map(lambda x: to_json(x), Task.query.all())))
 

     


   
#attachment class
class attachment(BaseModel):
    __tablename__='attachment'
    id=db.Column(db.Integer,primary_key=True)
    url= db.Column(db.VARCHAR,nullable=False)
    task_id=db.Column( db.Integer,ForeignKey('tasks.id',ondelete='CASCADE'),nullable=False)#attachment belongs to a task
  



    def __init__(self,url):
            self.url=url
        

    
    @classmethod
    def  return_all_users(cls):
        '''
            It returns a jonsify list of all accuns in the database
            '''
        def to_json(data):
            return dict( url=data.url)
        return dict(attachment=list(map(lambda x: to_json(x), attachment.query.all())))
    