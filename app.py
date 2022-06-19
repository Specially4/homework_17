from flask import Flask

from api1 import blueprint as api1

from setup_db import db

app = Flask(__name__)
app.register_blueprint(api1)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['RESTX_JSON'] = {'ensure_ascii': False, 'indent': 3}

app.app_context().push()

db.init_app(app)


if __name__ == '__main__':
    app.run(debug=True)
