class Config():
    SECRET_KEY = 'docplanta'

class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '1234'
    MYSQL_DB = 'docplant' 


config={
    'development':DevelopmentConfig
}