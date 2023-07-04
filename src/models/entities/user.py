from werkzeug.security import check_password_hash

class User():
    def __init__(self, id, email, password):
       self.id = id
       self.email = email
       self.password = password
    
    @classmethod
    def check_password_hash(self, hashed_password, password):
        return check_password_hash(hashed_password, password)



