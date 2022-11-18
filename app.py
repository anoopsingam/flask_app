from flask import Flask

from Utility.Config import load_config
from routes.app_routes import ap
from routes.auth_routes import auth

# Application Factory
app = Flask(__name__)

load_config(app)

# Routes Registry
app.register_blueprint(ap)
app.register_blueprint(auth)

if __name__ == '__main__':
    app.run()
