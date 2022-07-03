from flask_jwt import jwt_required
from flask_restful import Resource

from models.store_model import StoreModel


class StoreResource(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_item_by_name(name=name)
        if store:
            return store.to_json(), 200
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_item_by_name(name=name):
            return {'message': 'item already exist'}, 404
        store = StoreModel(name)
        try:
            store.save_to_db(), 200
        except:
            return {'message': 'An error occurred inserting the item'}, 500  # internal server error
        return store.to_json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_item_by_name(name)
        if not store:
            return {'message': 'item does not exist'}, 404

        store.delete_from_db()
        return {'message': 'Store deleted'}, 200


class StoreListResource(Resource):
    @jwt_required()
    def get(self):
        return {'stores': [store.to_json() for store in StoreModel.find_all()]}
