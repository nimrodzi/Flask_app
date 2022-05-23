from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from code1.models.item_model import ItemModel


class ItemResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store id"
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name=name)
        if item:
            return item.to_json(), 200
        return {'message': 'Item not found'}, 404

    @jwt_required()
    def post(self, name):
        if ItemModel.find_item_by_name(name=name):
            return {'message': 'item already exist'}, 404
        data = ItemResource.parser.parse_args()
        item = ItemModel(name, **data)
        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500  # internal server error
        return item.to_json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if not item:
            return {'message': 'item does not exist'}, 404

        item.delete_from_db()
        return {'message': 'Item deleted'}, 200

    @jwt_required()
    def put(self, name):
        data = ItemResource.parser.parse_args()
        item = ItemModel.find_item_by_name(name=name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
            item.store_id = data['store_id']

        item.save_to_db()
        return item.to_json()


class ItemListResource(Resource):
    @jwt_required()
    def get(self):
        return {'items': list(map(lambda x: x.to_json(), ItemModel.query.all()))}
