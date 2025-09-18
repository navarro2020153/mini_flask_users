from flask import Flask
from flask_migrate import Migrate
from models.user import db
from routes.user_routes import user_bp

app = Flask(__name__)

# Configuracion de la base de datos y seguridad
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'supersecretkey'

# Inicializacion de extensiones
db.init_app(app)
migrate = Migrate(app, db)

# Registro de Blueprints
app.register_blueprint(user_bp)

if __name__ == "__main__":
    app.run(debug=True)
