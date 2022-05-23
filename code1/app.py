from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.item_resource import ItemResource, ItemListResource
from resources.store_resource import StoreResource, StoreListResource
from resources.user_resource import UserResource
from db import db

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True  # To allow flask propagating exception even if debug is set to false on app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'nimrod'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(UserResource, '/register')
api.add_resource(ItemResource, '/item/<string:name>')
api.add_resource(ItemListResource, '/items')
api.add_resource(StoreResource, '/store/<string:name>')
api.add_resource(StoreListResource, '/stores')

if __name__ == '__main__':
    # db.metadata.clear()
    db.init_app(app)
    app.run(debug=True)  # important to mention debug=True
