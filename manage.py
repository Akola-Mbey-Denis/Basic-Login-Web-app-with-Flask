from app import create_app
from config import Configuration
from werkzeug.security import check_password_hash
from Model import User,Account,Task,Project,attachment


app = create_app()
 
ctx = app.app_context()
ctx.push()
#samples accounts;
 
# user3=User('mbey1','akoladenis123@gmail.com','cautions')
 
print(User.verify_reset_password_token('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJyZXNldF9wYXNzd29yZCI6NTksImV4cCI6MTU2NDY2MDQ2Mi41NjcxMDR9.IExvwwTJVoWodG_LfPWHIcNpwjQL1YGESnx_06w0y1Y'))
 

 

 
 
 
 
ctx.pop() 


 


 