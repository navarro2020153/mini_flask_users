import os

class config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"

    #conexion a MySql
    SQALCHEMY_DATABASE_URI = "mysql+pymysql://root@localhost/app_db"


    #codigo para desactivar notificaciones innesesarias de SQLALCHEMY   
    SQLALCHEMY_TRACK_MODIFICATIONS = False