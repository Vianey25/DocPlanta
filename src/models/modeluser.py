from .entities.user import User

class ModelUser():
    @classmethod
    def login(self,db,user):
        try:
            cursor=db.connection.cursor()
            sql = """SELECT id, email ,password From user WHERE email = '{}' """.format(user.email)
            cursor.execute(sql)
            row = cursor.fetchone()
            if row  != None:
                user = User(row[0],row[1],User.check_password(row[2],user.password))
                return user
            else:
                return None
        except Exception as ex:
          raise Exception(ex)
       