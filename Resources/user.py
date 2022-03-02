from flask_restful import Resource, reqparse
from Models.usermodel import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )
    parser.add_argument('password',
        type=str,
        required=True,
        help="This field cannot be left blank"
    )

    def post(self):
        data= UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return{"Message": "Username Already Exists"}, 400

        user= UserModel(**data)
        
        user.save_to_db()

        return{"message": "User created successfully"}, 201

class User(Resource):
    @classmethod
    def get(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'User not found'}, 404
        return  user.json()
    
    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return{'message': 'User does not exist'}, 404
        UserModel.delete_from_db()
        return{'message': 'User successfully deleted'}, 200

