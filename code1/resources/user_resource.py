from flask_restful import Resource, reqparse

from models.user_model import UserModel


class UserResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='this field cannot be blank')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='this field cannot be blank')

    def post(self):
        data = UserResource.parser.parse_args()

        print("Valdating username for duplicates")
        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that data already exists"}, 400

        print("Creating new username")

        user = UserModel(**data)
        user.save_to_db()

        return {"message": f"User {data['username']} created successfully."}, 201
